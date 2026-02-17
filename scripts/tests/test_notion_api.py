#!/usr/bin/env python3
"""
Testes para notion_api.py

Cobre funções puras e lógica de parsing sem realizar requisições reais:
- _extract_title
- _extract_page_summary
- _make_rich_text / _make_paragraph_block / _make_heading_block
- NotionAPIError / NotionAuthError
- Constantes (NOTION_API_BASE, NOTION_API_VERSION, TIPOS_BLOCO)
- CLI (main) via mock de subprocess / monkeypatch
"""

import json
import os
import sys
import pytest
from unittest.mock import MagicMock, patch, call
from io import StringIO

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from notion_api import (
    NotionAPIError,
    NotionAuthError,
    NOTION_API_BASE,
    NOTION_API_VERSION,
    ENV_TOKEN,
    ENV_DATABASE_ID,
    TIPOS_BLOCO,
    PROPRIEDADES_MARKETING,
    _extract_title,
    _extract_page_summary,
    _make_rich_text,
    _make_paragraph_block,
    _make_heading_block,
    _get_token,
    list_databases,
    list_pages,
    get_page,
    create_page,
    append_block,
    search,
    get_database_schema,
    full_report,
)


# ---------------------------------------------------------------------------
# Helpers / factories
# ---------------------------------------------------------------------------


def make_database(db_id: str = "db-001", title: str = "Marketing DB") -> dict:
    """Cria objeto de banco de dados no formato da Notion API."""
    return {
        "object": "database",
        "id": db_id,
        "title": [{"plain_text": title}],
        "url": f"https://notion.so/{db_id}",
        "created_time": "2026-01-01T00:00:00.000Z",
        "last_edited_time": "2026-02-01T12:00:00.000Z",
        "properties": {
            "Name": {"type": "title"},
            "Status": {"type": "select"},
            "Tags": {"type": "multi_select"},
        },
    }


def make_page(
    page_id: str = "page-001",
    title: str = "Post de Instagram",
    database_id: str = "db-001",
) -> dict:
    """Cria objeto de página no formato da Notion API."""
    return {
        "object": "page",
        "id": page_id,
        "created_time": "2026-01-15T10:00:00.000Z",
        "last_edited_time": "2026-02-10T14:30:00.000Z",
        "url": f"https://notion.so/{page_id}",
        "parent": {"type": "database_id", "database_id": database_id},
        "properties": {
            "title": {
                "type": "title",
                "title": [{"plain_text": title}],
            }
        },
    }


def make_search_result(items: list) -> dict:
    """Emula resposta de /search da Notion API."""
    return {
        "object": "list",
        "results": items,
        "has_more": False,
        "next_cursor": None,
    }


# ---------------------------------------------------------------------------
# NotionAPIError / NotionAuthError
# ---------------------------------------------------------------------------


class TestNotionAPIError:
    def test_erro_sem_status(self):
        e = NotionAPIError("Erro genérico")
        assert "Erro genérico" in str(e)
        assert e.status is None
        assert e.code is None

    def test_erro_com_status(self):
        e = NotionAPIError("Não autorizado", status=401)
        assert "[HTTP 401]" in str(e)
        assert e.status == 401

    def test_erro_com_codigo(self):
        e = NotionAPIError("Objeto não encontrado", status=404, code="object_not_found")
        assert "object_not_found" in str(e)

    def test_auth_error_e_subclasse(self):
        e = NotionAuthError("Token inválido")
        assert isinstance(e, NotionAPIError)
        assert isinstance(e, NotionAuthError)


# ---------------------------------------------------------------------------
# _extract_title
# ---------------------------------------------------------------------------


class TestExtractTitle:
    def test_database_com_lista_de_title(self):
        db = make_database(title="Meu DB")
        assert _extract_title(db) == "Meu DB"

    def test_page_com_propriedade_title(self):
        page = make_page(title="Conteúdo Incrível")
        assert _extract_title(page) == "Conteúdo Incrível"

    def test_objeto_sem_titulo_retorna_sem_titulo(self):
        obj = {"object": "page", "properties": {}}
        assert _extract_title(obj) == "(sem título)"

    def test_database_lista_vazia_retorna_sem_titulo(self):
        db = {"object": "database", "title": []}
        assert _extract_title(db) == "(sem título)"

    def test_titulo_composto_de_multiplos_segmentos(self):
        obj = {
            "title": [
                {"plain_text": "Parte 1 "},
                {"plain_text": "Parte 2"},
            ]
        }
        assert _extract_title(obj) == "Parte 1 Parte 2"


# ---------------------------------------------------------------------------
# _extract_page_summary
# ---------------------------------------------------------------------------


class TestExtractPageSummary:
    def test_retorna_dict(self):
        page = make_page()
        result = _extract_page_summary(page)
        assert isinstance(result, dict)

    def test_campos_basicos_presentes(self):
        page = make_page(page_id="p1", title="Minha Página")
        result = _extract_page_summary(page)
        assert result["id"] == "p1"
        assert result["titulo"] == "Minha Página"
        assert result["tipo"] == "page"

    def test_datas_truncadas_em_10_chars(self):
        page = make_page()
        result = _extract_page_summary(page)
        assert len(result["criado_em"]) == 10
        assert len(result["editado_em"]) == 10

    def test_url_presente(self):
        page = make_page(page_id="page-xyz")
        result = _extract_page_summary(page)
        assert "page-xyz" in result["url"]

    def test_parent_tipo_database(self):
        page = make_page(database_id="db-999")
        result = _extract_page_summary(page)
        assert result["parent_tipo"] == "database_id"
        assert result["parent_id"] == "db-999"


# ---------------------------------------------------------------------------
# _make_rich_text / _make_paragraph_block / _make_heading_block
# ---------------------------------------------------------------------------


class TestBlocoHelpers:
    def test_make_rich_text_retorna_lista(self):
        rt = _make_rich_text("Olá mundo")
        assert isinstance(rt, list)
        assert len(rt) == 1

    def test_make_rich_text_conteudo(self):
        rt = _make_rich_text("Texto de teste")
        assert rt[0]["type"] == "text"
        assert rt[0]["text"]["content"] == "Texto de teste"

    def test_make_paragraph_block_tipo(self):
        block = _make_paragraph_block("Parágrafo")
        assert block["type"] == "paragraph"
        assert block["object"] == "block"

    def test_make_paragraph_block_conteudo(self):
        block = _make_paragraph_block("Conteúdo aqui")
        rich = block["paragraph"]["rich_text"]
        assert rich[0]["text"]["content"] == "Conteúdo aqui"

    def test_make_heading_nivel_1(self):
        block = _make_heading_block("Título principal", level=1)
        assert block["type"] == "heading_1"
        assert "heading_1" in block

    def test_make_heading_nivel_2(self):
        block = _make_heading_block("Subtítulo", level=2)
        assert block["type"] == "heading_2"

    def test_make_heading_nivel_3(self):
        block = _make_heading_block("Sub-subtítulo", level=3)
        assert block["type"] == "heading_3"

    def test_make_heading_nivel_invalido_limita(self):
        block_alta = _make_heading_block("Teste", level=10)
        assert block_alta["type"] == "heading_3"
        block_baixa = _make_heading_block("Teste", level=0)
        assert block_baixa["type"] == "heading_1"


# ---------------------------------------------------------------------------
# _get_token
# ---------------------------------------------------------------------------


class TestGetToken:
    def test_retorna_token_da_env(self, monkeypatch):
        monkeypatch.setenv(ENV_TOKEN, "secret-token-abc")
        assert _get_token() == "secret-token-abc"

    def test_token_vazio_levanta_auth_error(self, monkeypatch):
        monkeypatch.delenv(ENV_TOKEN, raising=False)
        with pytest.raises(NotionAuthError):
            _get_token()

    def test_token_apenas_espacos_levanta_auth_error(self, monkeypatch):
        monkeypatch.setenv(ENV_TOKEN, "   ")
        with pytest.raises(NotionAuthError):
            _get_token()


# ---------------------------------------------------------------------------
# list_databases
# ---------------------------------------------------------------------------


class TestListDatabases:
    def test_retorna_lista(self, monkeypatch):
        db = make_database()
        monkeypatch.setattr(
            "notion_api._api_post",
            lambda path, token, payload: make_search_result([db]),
        )
        result = list_databases("tok")
        assert isinstance(result, list)
        assert len(result) == 1

    def test_campos_retornados(self, monkeypatch):
        db = make_database(db_id="db-abc", title="Base de Conteúdo")
        monkeypatch.setattr(
            "notion_api._api_post",
            lambda path, token, payload: make_search_result([db]),
        )
        result = list_databases("tok")
        assert result[0]["id"] == "db-abc"
        assert result[0]["titulo"] == "Base de Conteúdo"

    def test_lista_vazia(self, monkeypatch):
        monkeypatch.setattr(
            "notion_api._api_post",
            lambda path, token, payload: make_search_result([]),
        )
        result = list_databases("tok")
        assert result == []

    def test_multiplos_databases(self, monkeypatch):
        dbs = [make_database(f"db-{i}", f"DB {i}") for i in range(5)]
        monkeypatch.setattr(
            "notion_api._api_post",
            lambda path, token, payload: make_search_result(dbs),
        )
        result = list_databases("tok")
        assert len(result) == 5


# ---------------------------------------------------------------------------
# list_pages
# ---------------------------------------------------------------------------


class TestListPages:
    def test_retorna_lista(self, monkeypatch):
        page = make_page()
        monkeypatch.setattr(
            "notion_api._api_post",
            lambda path, token, payload: make_search_result([page]),
        )
        result = list_pages("tok", "db-001")
        assert isinstance(result, list)
        assert len(result) == 1

    def test_campos_da_pagina(self, monkeypatch):
        page = make_page(page_id="p-007", title="Post de SEO")
        monkeypatch.setattr(
            "notion_api._api_post",
            lambda path, token, payload: make_search_result([page]),
        )
        result = list_pages("tok", "db-001")
        assert result[0]["id"] == "p-007"
        assert result[0]["titulo"] == "Post de SEO"

    def test_lista_vazia(self, monkeypatch):
        monkeypatch.setattr(
            "notion_api._api_post",
            lambda path, token, payload: make_search_result([]),
        )
        result = list_pages("tok", "db-001")
        assert result == []


# ---------------------------------------------------------------------------
# get_page
# ---------------------------------------------------------------------------


class TestGetPage:
    def test_retorna_dict(self, monkeypatch):
        page = make_page(page_id="p-abc")
        monkeypatch.setattr(
            "notion_api._api_get",
            lambda path, token, params=None: page,
        )
        result = get_page("tok", "p-abc")
        assert isinstance(result, dict)

    def test_campos_essenciais(self, monkeypatch):
        page = make_page(page_id="p-xyz", title="Artigo Blog")
        monkeypatch.setattr(
            "notion_api._api_get",
            lambda path, token, params=None: page,
        )
        result = get_page("tok", "p-xyz")
        assert result["id"] == "p-xyz"
        assert result["titulo"] == "Artigo Blog"

    def test_tem_campo_propriedades(self, monkeypatch):
        page = make_page()
        monkeypatch.setattr(
            "notion_api._api_get",
            lambda path, token, params=None: page,
        )
        result = get_page("tok", "page-001")
        assert "propriedades" in result
        assert isinstance(result["propriedades"], dict)


# ---------------------------------------------------------------------------
# create_page
# ---------------------------------------------------------------------------


class TestCreatePage:
    def _mock_api_post(self, title: str, page_id: str = "new-page-id"):
        created = make_page(page_id=page_id, title=title)
        return lambda path, token, payload: created

    def test_retorna_dict_com_id(self, monkeypatch):
        monkeypatch.setattr("notion_api._api_post", self._mock_api_post("Post Novo", "n-001"))
        result = create_page("tok", "db-001", "Post Novo")
        assert result["id"] == "n-001"
        assert result["titulo"] == "Post Novo"

    def test_url_presente_no_resultado(self, monkeypatch):
        monkeypatch.setattr("notion_api._api_post", self._mock_api_post("Título Qualquer"))
        result = create_page("tok", "db-001", "Título Qualquer")
        assert "url" in result
        assert isinstance(result["url"], str)

    def test_com_conteudo_inclui_children(self, monkeypatch):
        payloads_capturados = []

        def mock_post(path, token, payload):
            payloads_capturados.append(payload)
            return make_page(title="Com conteúdo")

        monkeypatch.setattr("notion_api._api_post", mock_post)
        create_page("tok", "db-001", "Com conteúdo", content="Texto inicial do post")
        assert len(payloads_capturados) == 1
        assert "children" in payloads_capturados[0]

    def test_sem_conteudo_sem_children(self, monkeypatch):
        payloads_capturados = []

        def mock_post(path, token, payload):
            payloads_capturados.append(payload)
            return make_page(title="Sem conteúdo")

        monkeypatch.setattr("notion_api._api_post", mock_post)
        create_page("tok", "db-001", "Sem conteúdo")
        assert "children" not in payloads_capturados[0]


# ---------------------------------------------------------------------------
# append_block
# ---------------------------------------------------------------------------


class TestAppendBlock:
    def _mock_patch(self, block_ids: list):
        resp = {"results": [{"id": bid} for bid in block_ids]}
        return lambda path, token, payload: resp

    def test_retorna_dict_com_total(self, monkeypatch):
        monkeypatch.setattr("notion_api._api_patch", self._mock_patch(["b-001"]))
        result = append_block("tok", "page-001", "Texto do bloco")
        assert result["total"] == 1
        assert "b-001" in result["blocos_criados"]

    def test_tipo_paragraph_padrao(self, monkeypatch):
        payloads = []

        def mock_patch(path, token, payload):
            payloads.append(payload)
            return {"results": [{"id": "b-x"}]}

        monkeypatch.setattr("notion_api._api_patch", mock_patch)
        append_block("tok", "page-001", "Texto parágrafo")
        children = payloads[0]["children"]
        assert children[0]["type"] == "paragraph"

    def test_tipo_heading_2(self, monkeypatch):
        payloads = []

        def mock_patch(path, token, payload):
            payloads.append(payload)
            return {"results": [{"id": "b-y"}]}

        monkeypatch.setattr("notion_api._api_patch", mock_patch)
        append_block("tok", "page-001", "Título seção", block_type="heading_2")
        children = payloads[0]["children"]
        assert children[0]["type"] == "heading_2"

    def test_tipo_invalido_usa_paragraph(self, monkeypatch):
        payloads = []

        def mock_patch(path, token, payload):
            payloads.append(payload)
            return {"results": [{"id": "b-z"}]}

        monkeypatch.setattr("notion_api._api_patch", mock_patch)
        append_block("tok", "page-001", "Texto", block_type="tipo_inexistente")
        children = payloads[0]["children"]
        assert children[0]["type"] == "paragraph"

    def test_page_id_no_retorno(self, monkeypatch):
        monkeypatch.setattr("notion_api._api_patch", self._mock_patch(["b-1"]))
        result = append_block("tok", "minha-pagina", "Texto")
        assert result["page_id"] == "minha-pagina"


# ---------------------------------------------------------------------------
# search
# ---------------------------------------------------------------------------


class TestSearch:
    def test_retorna_lista(self, monkeypatch):
        page = make_page(title="Resultado de busca")
        monkeypatch.setattr(
            "notion_api._api_post",
            lambda path, token, payload: make_search_result([page]),
        )
        result = search("tok", "marketing")
        assert isinstance(result, list)
        assert len(result) == 1

    def test_resultado_tem_titulo(self, monkeypatch):
        page = make_page(title="Conteúdo Viral")
        monkeypatch.setattr(
            "notion_api._api_post",
            lambda path, token, payload: make_search_result([page]),
        )
        result = search("tok", "viral")
        assert result[0]["titulo"] == "Conteúdo Viral"

    def test_sem_resultados(self, monkeypatch):
        monkeypatch.setattr(
            "notion_api._api_post",
            lambda path, token, payload: make_search_result([]),
        )
        result = search("tok", "termo inexistente")
        assert result == []

    def test_filtro_tipo_page(self, monkeypatch):
        payloads = []

        def mock_post(path, token, payload):
            payloads.append(payload)
            return make_search_result([])

        monkeypatch.setattr("notion_api._api_post", mock_post)
        search("tok", "conteúdo", search_type="page")
        assert payloads[0].get("filter", {}).get("value") == "page"

    def test_sem_filtro_tipo_sem_filter_key(self, monkeypatch):
        payloads = []

        def mock_post(path, token, payload):
            payloads.append(payload)
            return make_search_result([])

        monkeypatch.setattr("notion_api._api_post", mock_post)
        search("tok", "qualquer", search_type=None)
        assert "filter" not in payloads[0]


# ---------------------------------------------------------------------------
# get_database_schema
# ---------------------------------------------------------------------------


class TestGetDatabaseSchema:
    def test_retorna_schema(self, monkeypatch):
        db = make_database(db_id="db-schema", title="Schema DB")
        monkeypatch.setattr(
            "notion_api._api_get",
            lambda path, token, params=None: db,
        )
        result = get_database_schema("tok", "db-schema")
        assert result["id"] == "db-schema"
        assert result["titulo"] == "Schema DB"

    def test_propriedades_mapeadas(self, monkeypatch):
        db = make_database()
        monkeypatch.setattr(
            "notion_api._api_get",
            lambda path, token, params=None: db,
        )
        result = get_database_schema("tok", "db-001")
        assert "Name" in result["propriedades"]
        assert result["propriedades"]["Name"] == "title"

    def test_total_propriedades(self, monkeypatch):
        db = make_database()  # 3 propriedades: Name, Status, Tags
        monkeypatch.setattr(
            "notion_api._api_get",
            lambda path, token, params=None: db,
        )
        result = get_database_schema("tok", "db-001")
        assert result["total_propriedades"] == 3


# ---------------------------------------------------------------------------
# full_report
# ---------------------------------------------------------------------------


class TestFullReport:
    def test_retorna_dict(self, monkeypatch):
        monkeypatch.setattr(
            "notion_api.list_databases",
            lambda token, limit=50: [],
        )
        result = full_report("tok")
        assert isinstance(result, dict)

    def test_tem_campos_essenciais(self, monkeypatch):
        monkeypatch.setattr("notion_api.list_databases", lambda token, limit=50: [])
        result = full_report("tok")
        assert "gerado_em" in result
        assert "total_databases" in result
        assert "databases" in result

    def test_com_database_id_inclui_paginas(self, monkeypatch):
        monkeypatch.setattr("notion_api.list_databases", lambda token, limit=50: [])
        monkeypatch.setattr(
            "notion_api.get_database_schema",
            lambda token, db_id: {
                "id": db_id, "titulo": "DB", "propriedades": {}, "total_propriedades": 0
            },
        )
        monkeypatch.setattr(
            "notion_api.list_pages",
            lambda token, db_id, limit=20: [make_page() for _ in range(3)],
        )
        result = full_report("tok", database_id="db-001")
        assert "paginas_recentes" in result
        assert result["total_paginas"] == 3

    def test_erro_database_capturado(self, monkeypatch):
        monkeypatch.setattr("notion_api.list_databases", lambda token, limit=50: [])
        monkeypatch.setattr(
            "notion_api.get_database_schema",
            lambda token, db_id: (_ for _ in ()).throw(NotionAPIError("não encontrado", 404)),
        )
        result = full_report("tok", database_id="db-invalido")
        assert "erro_database" in result


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------


class TestConstantes:
    def test_notion_api_base_url(self):
        assert NOTION_API_BASE.startswith("https://")
        assert "notion.com" in NOTION_API_BASE

    def test_notion_api_version_formato(self):
        # Formato: YYYY-MM-DD
        partes = NOTION_API_VERSION.split("-")
        assert len(partes) == 3
        assert len(partes[0]) == 4  # ano

    def test_env_token_nome(self):
        assert ENV_TOKEN == "NOTION_TOKEN"

    def test_env_database_id_nome(self):
        assert ENV_DATABASE_ID == "NOTION_DATABASE_ID"

    def test_tipos_bloco_tem_essenciais(self):
        essenciais = {"paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item"}
        assert essenciais.issubset(TIPOS_BLOCO)

    def test_tipos_bloco_sem_duplicatas(self):
        assert len(TIPOS_BLOCO) == len(set(TIPOS_BLOCO))

    def test_propriedades_marketing_tem_itens(self):
        assert len(PROPRIEDADES_MARKETING) >= 5
        assert all(isinstance(p, str) for p in PROPRIEDADES_MARKETING)
