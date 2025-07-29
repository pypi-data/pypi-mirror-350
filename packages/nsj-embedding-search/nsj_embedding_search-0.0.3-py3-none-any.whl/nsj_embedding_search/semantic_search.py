import numpy as np
import uuid

from sortedcontainers import SortedList

from nsj_embedding_search.dao import DAO
from nsj_embedding_search.embedding_util import EmbeddingUtil
from nsj_embedding_search.enums import IndexMode, MergeChunksMode
from nsj_embedding_search.search_result import ChunkResult, SearchResult
from nsj_embedding_search.settings import (
    CHUNCK_SIZE,
    OPENAI_EMBEDDING_MODEL,
    OPENAI_EMBEDDING_MODEL_LIMIT,
)
from nsj_embedding_search.text_utils import TextUtils


class SemanticSearch:
    def __init__(
        self,
        dbconn,
        index_table: str,
        aditional_search_filters: callable = None,
        index_mode: IndexMode = IndexMode.CHUNCKED,
        store_index_merge_chunks_mode: MergeChunksMode = MergeChunksMode.AVERAGE,
    ):
        self._dbconn = dbconn
        self._index_table = index_table
        self._aditional_search_filters = aditional_search_filters
        self._index_mode = index_mode
        self._store_index_merge_chunks_mode = store_index_merge_chunks_mode

        self._dao = DAO(
            dbconn=self._dbconn,
            index_table=index_table,
        )
        self._text_utils = TextUtils()
        self._embedding_util = EmbeddingUtil()

    def search(
        self,
        query: str,
        limit_results: int = 5,
        metadata: dict = None,
        query_embedding_mode: IndexMode = IndexMode.CHUNCKED,
        query_merge_chuncks_mode: MergeChunksMode = MergeChunksMode.AVERAGE,
        index_merge_chuncks_mode: MergeChunksMode = None,
        similarity_merge_chunks_mode: MergeChunksMode = MergeChunksMode.AVERAGE,
        similarity_threshold: float = 0.5,
    ) -> list[SearchResult]:

        # Embedding query
        embeddings, chuncks = self._embedding_value(
            query_embedding_mode,
            query,
            (query_merge_chuncks_mode is not None),
            query_merge_chuncks_mode,
        )

        # Updating metadata (with custumized code)
        if self._aditional_search_filters is not None:
            metadata2 = self._aditional_search_filters(
                self._index_table,
                self._index_mode,
                self._store_index_merge_chunks_mode,
                query,
                limit_results,
                metadata,
                query_embedding_mode,
                query_merge_chuncks_mode,
                index_merge_chuncks_mode,
                chuncks,
                embeddings,
            )

            if metadata2 is not None:
                metadata = metadata2

        # Retrieving, paginated, and calculating similarities
        results: SortedList[SearchResult] = SortedList(key=lambda x: x.score)

        limit_query_results = 1000
        aux_group = []
        aux_content = ""

        while True:
            qtd, index = self._dao.get_list(metadata)

            for item in index:
                aux_group.append(item)
                aux_content += item["content"]

                ## If ends the group, or broken index
                if (
                    item["chunck_number"] == item["total_chunks"]
                    or aux_group[-1]["external_id"] != item["external_id"]
                ):
                    ### Reseting aux vars
                    group = aux_group
                    aux_group = []

                    content = aux_content
                    aux_content = ""

                    ### Combining group embeddings if needed
                    group_embeddings = [group_item["embedding"] for group_item in group]
                    if index_merge_chuncks_mode is not None:
                        group_embeddings = self._embedding_util.combine_embeddings(
                            embeddings=group_embeddings,
                            mode=index_merge_chuncks_mode,
                        )

                    ### Calculating similarity
                    similarities = []
                    for query_emb in embeddings:
                        for group_emb in group_embeddings:
                            similarity = self._embedding_util.cosine_similarity(
                                query_emb,
                                group_emb,
                            )
                            similarities.append(similarity)

                    ### Calculating group similarity
                    if similarity_merge_chunks_mode is None:
                        similarity_merge_chunks_mode = MergeChunksMode.AVERAGE

                    similarity = self.combine_similarities(
                        similarities,
                        similarity_merge_chunks_mode,
                    )

                    if similarity < similarity_threshold:
                        continue

                    ### Creating search result
                    result = SearchResult()
                    result.external_id = group[0]["external_id"]
                    result.title = group[0]["title"]
                    result.content = content
                    result.reference = group[0]["reference"]
                    result.metadata = group[0]["metadata"]
                    result.score = similarity
                    result.created_at = group[0]["created_at"]
                    result.updated_at = group[0]["updated_at"]
                    result.combined_embedding = group_embeddings[0]
                    result.chunks = []

                    for i, group_item in enumerate(group):
                        chunk_result = ChunkResult()
                        chunk_result.embedding = group_item["embedding"]
                        chunk_result.content = group_item["content"]

                        if i < len(similarities):
                            chunk_result.score = similarities[i]
                        else:
                            chunk_result.score = similarities[-1]

                        result.chunks.append(chunk_result)

                    results.add(result)

            ## If results list has the max results length, discard wich has the lower similarity
            if len(results) > limit_query_results:
                results.pop(0)

            ## If current page length lower than max page size
            if qtd < limit_query_results:
                break

        # Returning results
        return list(reversed(list(results)))

    def combine_similarities(self, similarities: list[float], mode: MergeChunksMode):

        # Converting to numpy array
        similarities = np.array(similarities)

        # Applying the selected merge mode
        if mode == MergeChunksMode.AVERAGE:
            return np.mean(similarities, axis=0, keepdims=True).tolist()[0]
        elif mode == MergeChunksMode.MAX:
            return np.max(similarities, axis=0, keepdims=True).tolist()[0]
        elif mode == MergeChunksMode.MIN:
            return np.min(similarities, axis=0, keepdims=True).tolist()[0]
        else:
            raise ValueError(f"Unknown merge mode: {mode}")

    def index(
        self,
        external_id: uuid.UUID,
        title: str,
        content: str,
        reference: dict[str, any],
        metadata: dict[str, any],
    ):
        # Embedding content
        embeddings, chuncks = self._embedding_value(
            self._index_mode,
            content,
            (self._index_mode == IndexMode.COMPLETE),
            self._store_index_merge_chunks_mode,
        )

        # Inserting into database
        for i, emb in enumerate(embeddings):
            self._dao.insert(
                external_id=external_id,
                title=title,
                embedding=emb,
                content=(
                    chuncks[i] if self._index_mode == IndexMode.CHUNCKED else content
                ),
                reference=reference,
                metadata=metadata,
                chunck_number=i + 1,
                total_chunks=len(chuncks),
            )

    def _embedding_value(
        self,
        index_mode: IndexMode,
        value: str,
        combine_embeddings: bool,
        merge_chunks_mode: MergeChunksMode,
    ):
        # Resolving chunck_size
        if index_mode == IndexMode.CHUNCKED:
            chunck_size = CHUNCK_SIZE
        else:
            chunck_size = OPENAI_EMBEDDING_MODEL_LIMIT

        # Splitting text into chunks
        _, chuncks = self._text_utils.slip_text(value, chunck_size)

        # Embedding and normalizing
        embeddings = []
        for chunck in chuncks:
            emb = self._embedding_util.get_embedding(
                text=chunck,
                embedding_model=OPENAI_EMBEDDING_MODEL,
            )
            emb = self._embedding_util.reduce_embedding_dimensions(emb)

            embeddings.append(emb)

        # Combining embeddings if needed
        if combine_embeddings:
            embeddings = self._embedding_util.combine_embeddings(
                embeddings=embeddings,
                mode=merge_chunks_mode,
            )

        return (embeddings, chuncks)

    def remove(
        self,
        external_id: uuid.UUID,
    ):
        self._dao.delete(
            external_id=external_id,
        )
