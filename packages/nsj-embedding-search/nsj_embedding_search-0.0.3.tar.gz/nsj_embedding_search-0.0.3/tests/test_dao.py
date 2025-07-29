# test_dao.py
import uuid

import pytest

# Ajuste o import conforme a estrutura real do seu projeto
from nsj_embedding_search.dao import DAO


# ---------------------------------------------------------------------------
# Dublê (mock) para o DBAdapter3
# ---------------------------------------------------------------------------


class DummyDB:
    """Registra a última chamada a execute() para inspeção pelos testes."""

    def __init__(self):
        self.last_sql = None
        self.last_kwargs = None
        self.return_value = [{"fake": "row"}]

    def execute(self, sql, **kwargs):
        self.last_sql = sql
        self.last_kwargs = kwargs
        return self.return_value


@pytest.fixture
def dao(monkeypatch):
    """Instância de DAO com DBAdapter3 substituído pelo DummyDB."""
    dummy_db = DummyDB()

    # Patching do símbolo DBAdapter3 *dentro do módulo dao*
    import nsj_embedding_search.dao as dao_module

    monkeypatch.setattr(dao_module, "DBAdapter3", lambda conn: dummy_db)

    return DAO(dbconn=None, index_table="idx_test"), dummy_db


# ---------------------------------------------------------------------------
# Testes: list
# ---------------------------------------------------------------------------


def test_list_without_metadata(dao):
    dao_obj, dummy_db = dao

    result = dao_obj.list()  # metadata padrão: None

    # retorno deve ser o valor devolvido pelo DummyDB
    assert result == dummy_db.return_value

    # WHERE não deve existir quando metadata é None
    assert "WHERE metadata" not in dummy_db.last_sql
    # parâmetros devem conter apenas metadata=None
    assert dummy_db.last_kwargs == {"metadata": None}


def test_list_with_metadata(dao):
    dao_obj, dummy_db = dao
    meta = {"foo": "bar"}

    dao_obj.list(metadata=meta, limit_results=42)

    sql = dummy_db.last_sql.upper()
    # WHERE clause deve aparecer
    assert "WHERE METADATA @> %(METADATA)S".upper() in sql
    # LIMIT customizado deve ser respeitado
    assert "LIMIT 42" in sql
    # Parâmetros passados
    assert dummy_db.last_kwargs == {"metadata": meta}


# ---------------------------------------------------------------------------
# Testes: insert
# ---------------------------------------------------------------------------


def test_insert_builds_correct_sql_and_params(dao):
    dao_obj, dummy_db = dao
    ext_id = uuid.uuid4()

    dao_obj.insert(
        external_id=ext_id,
        title="Título",
        content="Conteúdo",
        reference={"ref": 1},
        metadata={"k": "v"},
        chunck_number=3,
        total_chunks=7,
    )

    sql_upper = dummy_db.last_sql.upper()
    # Insert na tabela correta
    assert sql_upper.startswith(f"INSERT INTO {dao_obj._index_table}".upper())
    # Todos os parâmetros obrigatórios
    expected_keys = {
        "external_id",
        "title",
        "content",
        "reference",
        "metadata",
        "chunck_number",
        "total_chunks",
    }
    assert set(dummy_db.last_kwargs.keys()) == expected_keys
    assert dummy_db.last_kwargs["external_id"] == ext_id


# ---------------------------------------------------------------------------
# Teste: delete
# ---------------------------------------------------------------------------


def test_delete_executes_correct_sql(dao):
    dao_obj, dummy_db = dao
    ext_id = uuid.uuid4()

    dao_obj.delete(external_id=ext_id)

    sql_upper = dummy_db.last_sql.upper()
    assert sql_upper.startswith(f"DELETE FROM {dao_obj._index_table}".upper())
    assert "WHERE EXTERNAL_ID =" in sql_upper
    assert dummy_db.last_kwargs == {"external_id": ext_id}
