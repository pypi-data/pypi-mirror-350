import openai
import numpy as np

from nsj_embedding_search.enums import MergeChunksMode


class EmbeddingUtil:

    def get_embedding(self, text: str, embedding_model: str):
        resposta = openai.embeddings.create(model=embedding_model, input=[text])
        return resposta.data[0].embedding

    def cosine_similarity(self, embedding1, embedding2):
        a = embedding1
        b = embedding2

        if not isinstance(embedding1, np.ndarray):
            a = np.array(embedding1)
        if not isinstance(embedding2, np.ndarray):
            b = np.array(embedding2)

        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def reduce_embedding_dimensions(self, x):
        x = x[:256]
        x = np.array(x)
        if x.ndim == 1:
            norm = np.linalg.norm(x)
            if norm == 0:
                return x.tolist()
            result = x / norm
            return result.tolist()
        else:
            norm = np.linalg.norm(x, 2, axis=1, keepdims=True)
            result = np.where(norm == 0, x, x / norm)
            return result.tolist()

    def calc_norma(self, vetor):
        return np.linalg.norm(vetor)

    def normalizar_embedding(self, vetor):
        if not isinstance(vetor, np.ndarray):
            vetor = np.array(vetor)

        norma = np.linalg.norm(vetor)
        if norma == 0:
            return vetor.tolist()  # Evita divisão por zero

        return (vetor / norma).tolist()

    def normalizar_embeddings(self, vetores):
        # Converte para ndarray se não for
        vetores = np.asarray(vetores, dtype=float)

        # Calcula a norma para cada vetor (ao longo do eixo 1)
        normas = np.linalg.norm(vetores, axis=1, keepdims=True)

        # Evita divisão por zero substituindo normas zero por 1 (não altera o vetor original)
        normas[normas == 0] = 1.0

        # Divide cada vetor pela sua norma
        return vetores / normas

    def combine_embeddings(self, embeddings: list[list[float]], mode: MergeChunksMode):

        # Converting to numpy array
        embeddings = np.array(embeddings)

        # Applying the selected merge mode
        if mode == MergeChunksMode.AVERAGE:
            return np.mean(embeddings, axis=0, keepdims=True).tolist()
        elif mode == MergeChunksMode.MAX:
            return np.max(embeddings, axis=0, keepdims=True).tolist()
        elif mode == MergeChunksMode.MIN:
            return np.min(embeddings, axis=0, keepdims=True).tolist()
        else:
            raise ValueError(f"Unknown merge mode: {mode}")
