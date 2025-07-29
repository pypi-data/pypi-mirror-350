import datetime
import uuid


class ChunkResult:
    embedding: list[float] = None
    score: float = None
    content: str = None


class SearchResult:
    external_id: uuid.UUID = None
    title: str = None
    content: str = None
    reference: dict[str, any] = None
    metadata: dict[str, any] = None
    score: float = None
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None
    combined_embedding: list[float] = None
    chunks: list[ChunkResult] = None
