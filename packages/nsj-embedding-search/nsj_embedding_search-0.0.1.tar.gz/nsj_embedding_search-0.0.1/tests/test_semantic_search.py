# test_semantic_search.py
import uuid
from types import SimpleNamespace

import pytest
import numpy as np

from nsj_embedding_search.semantic_search import SemanticSearch
from nsj_embedding_search.enums import IndexMode, MergeChunksMode


# ---------------------------------------------------------------------------
# Fixtures e dublês de teste (mocks)
# ---------------------------------------------------------------------------


class DummyDAO:
    """DAO minimalista que devolve sempre a mesma página e depois nada,
    permitindo que o loop interno de `search` seja encerrado."""

    def __init__(self):
        self._first_call = True

    def list(self, metadata):
        if self._first_call:
            self._first_call = False
            return [
                {
                    "external_id": "0d1a8427-0330-4ac3-8d70-1df7abbce9b8",
                    "title": "Documento Teste",
                    "content": "chunk-1",
                    "reference": {},
                    "metadata": {},
                    "embedding": [1, 0],
                    "chunck_number": 1,
                    "total_chunks": 2,
                    "created_at": "2025-01-01",
                    "updated_at": "2025-01-01",
                },
                {
                    "external_id": "4caf7fda-7a3c-47ca-8191-7f1d92f618e6",
                    "title": "Documento Teste",
                    "content": "chunk-2",
                    "reference": {},
                    "metadata": {},
                    "embedding": [1, 0],
                    "chunck_number": 2,
                    "total_chunks": 2,
                    "created_at": "2025-01-01",
                    "updated_at": "2025-01-01",
                },
            ]
        # Segunda chamada devolve lista vazia → encerra o loop while
        return []

    # Os demais métodos não são usados nos testes abaixo
    def insert(self, *_, **__): ...
    def delete(self, *_, **__): ...


@pytest.fixture
def semantic_search(monkeypatch):
    """Instância do SemanticSearch com dependências ‘mockadas’."""
    ss = SemanticSearch(dbconn=None, index_table="idx_test")

    # Substitui o DAO real pelo dummy
    monkeypatch.setattr(ss, "_dao", DummyDAO())

    # Evita chamadas reais ao modelo de embedding
    monkeypatch.setattr(
        ss,
        "_embedding_value",
        lambda *_, **__: ([[0.5, 0.5]], ["query chunk"]),
    )
    monkeypatch.setattr(
        ss._embedding_util,
        "cosine_similarity",
        lambda a, b: [0.9],  # devolve lista para casar com .tolist()[0]
    )
    monkeypatch.setattr(
        ss._embedding_util,
        "combine_embeddings",
        lambda embeddings, mode: embeddings,
    )
    return ss


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "mode, vals, expected",
    [
        (MergeChunksMode.AVERAGE, [[0.2], [0.6]], 0.4),
        (MergeChunksMode.MAX, [[0.2], [0.6]], 0.6),
        (MergeChunksMode.MIN, [[0.2], [0.6]], 0.2),
    ],
)
def test_combine_similarities_ok(mode, vals, expected):
    ss = SemanticSearch(dbconn=None, index_table="idx")
    assert pytest.approx(ss.combine_similarities(vals, mode)) == expected


def test_combine_similarities_unknown_mode():
    ss = SemanticSearch(dbconn=None, index_table="idx")
    with pytest.raises(ValueError):
        ss.combine_similarities([[0.1]], "MODE_INVALIDO")  # qualquer valor não enum


def test_search_returns_expected_group(semantic_search):
    """Garante que:
    – o loop de paginação é encerrado,
    – apenas um resultado é devolvido,
    – campos principais são preenchidos corretamente,
    – score corresponde ao valor ‘mockado’."""
    results = list(
        semantic_search.search(
            query="texto qualquer",
            similarity_threshold=0.1,  # abaixo de 0.9 para garantir retorno
        )
    )

    assert len(results) == 1
    res = results[0]
    assert res.external_id == "0d1a8427-0330-4ac3-8d70-1df7abbce9b8"
    assert res.title == "Documento Teste"
    assert res.content == "chunk-1chunk-2" or res.content.endswith("chunk-2")
    assert res.score == pytest.approx(0.9)
    # Cada chunk dentro do group deve estar presente
    assert {c.content for c in res.chunks} == {"chunk-1", "chunk-2"}
