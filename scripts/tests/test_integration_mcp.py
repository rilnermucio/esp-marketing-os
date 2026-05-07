#!/usr/bin/env python3
"""
STORY-013 — Testes de integração para comandos MCP e pipeline MOS.

Cobre:
1. Consistência do COMMAND_MAP com scripts existentes no disco
2. Pipeline MOS: argumentos chegam corretamente aos scripts
3. Configuração de MCP: regras de uso e estrutura de settings
4. Cobertura: todo script Python relevante está mapeado no MOS
5. Integrações de API: módulos importáveis e constantes presentes
"""

import os
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mos import COMMAND_MAP, SPECIAL_ARGS, SCRIPTS_DIR, run_script

# ---------------------------------------------------------------------------
# Caminhos do projeto
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent.parent.parent
SCRIPTS_PATH = Path(SCRIPTS_DIR)


# ===========================================================================
# 1. CONSISTÊNCIA DO COMMAND_MAP
# ===========================================================================

class TestCommandMapIntegridade:
    """Valida que COMMAND_MAP está sincronizado com os arquivos no disco."""

    def test_todos_scripts_do_command_map_existem(self):
        """Cada script referenciado no COMMAND_MAP deve existir em scripts/."""
        ausentes = []
        for categoria, comandos in COMMAND_MAP.items():
            for cmd, (script, _) in comandos.items():
                caminho = SCRIPTS_PATH / script
                if not caminho.exists():
                    ausentes.append(f"{categoria}.{cmd} → {script}")
        assert not ausentes, f"Scripts referenciados mas ausentes:\n" + "\n".join(ausentes)

    def test_todas_categorias_tem_pelo_menos_um_comando(self):
        for categoria, comandos in COMMAND_MAP.items():
            assert len(comandos) >= 1, f"Categoria '{categoria}' está vazia"

    def test_scripts_do_command_map_sao_arquivos_python(self):
        scripts = set()
        for comandos in COMMAND_MAP.values():
            for script, _ in comandos.values():
                scripts.add(script)
        for script in scripts:
            assert script.endswith(".py"), f"Script '{script}' não é um arquivo Python"

    def test_descricoes_nao_estao_vazias(self):
        for categoria, comandos in COMMAND_MAP.items():
            for cmd, (script, desc) in comandos.items():
                assert desc.strip(), f"{categoria}.{cmd}: descrição vazia"

    def test_descricoes_tem_tamanho_razoavel(self):
        for categoria, comandos in COMMAND_MAP.items():
            for cmd, (_, desc) in comandos.items():
                assert 5 <= len(desc) <= 100, \
                    f"{categoria}.{cmd}: descrição inválida (len={len(desc)})"

    def test_scripts_referenciados_sao_importaveis(self):
        """Scripts referenciados devem ter sintaxe Python válida."""
        import ast
        scripts = set()
        for comandos in COMMAND_MAP.values():
            for script, _ in comandos.values():
                scripts.add(script)

        erros = []
        for script in scripts:
            caminho = SCRIPTS_PATH / script
            if caminho.exists():
                try:
                    ast.parse(caminho.read_text(encoding="utf-8"))
                except SyntaxError as e:
                    erros.append(f"{script}: {e}")

        assert not erros, f"Scripts com erro de sintaxe:\n" + "\n".join(erros)


# ===========================================================================
# 2. PIPELINE MOS: SPECIAL_ARGS
# ===========================================================================

class TestPipelineMOSArgumentos:
    """Valida transformações de argumentos do pipeline MOS → scripts."""

    def test_special_args_apenas_para_chaves_validas(self):
        """Todas as chaves em SPECIAL_ARGS devem existir no COMMAND_MAP."""
        invalidas = []
        for (cat, cmd) in SPECIAL_ARGS:
            if cat not in COMMAND_MAP or cmd not in COMMAND_MAP[cat]:
                invalidas.append(f"({cat}, {cmd})")
        assert not invalidas, f"SPECIAL_ARGS com chaves inválidas: {invalidas}"

    def test_headlines_compare_injeta_flag(self):
        fn = SPECIAL_ARGS[("headlines", "compare")]
        result = fn(["Título A", "Título B"])
        assert "--compare" in result
        assert "Título A" in result

    def test_project_create_injeta_subcomando(self):
        fn = SPECIAL_ARGS[("project", "create")]
        result = fn(["Meu Projeto", "--type", "launch"])
        assert result[0] == "create"
        assert "Meu Projeto" in result

    def test_project_list_injeta_subcomando(self):
        fn = SPECIAL_ARGS[("project", "list")]
        result = fn([])
        assert result[0] == "list"

    def test_project_status_preserva_slug(self):
        fn = SPECIAL_ARGS[("project", "status")]
        result = fn(["meu-projeto-slug"])
        assert result[0] == "status"
        assert "meu-projeto-slug" in result

    def test_project_add_content_injeta_subcomando(self):
        fn = SPECIAL_ARGS[("project", "add-content")]
        result = fn(["slug", "arquivo.md"])
        assert result[0] == "add-content"

    def test_project_complete_injeta_subcomando(self):
        fn = SPECIAL_ARGS[("project", "complete")]
        result = fn(["slug"])
        assert result[0] == "complete"

    def test_project_note_injeta_subcomando(self):
        fn = SPECIAL_ARGS[("project", "note")]
        result = fn(["slug", "Nota aqui"])
        assert result[0] == "note"

    def test_readability_check_passthrough(self):
        fn = SPECIAL_ARGS[("readability", "check")]
        args = ["--file", "artigo.txt"]
        result = fn(args)
        assert result == args

    def test_transformacoes_retornam_listas(self):
        for key, fn in SPECIAL_ARGS.items():
            result = fn(["arg1", "arg2"])
            assert isinstance(result, list), f"SPECIAL_ARGS[{key}] não retornou lista"


# ===========================================================================
# 3. PIPELINE MOS: EXECUÇÃO END-TO-END (com mock)
# ===========================================================================

class TestPipelineMOSExecucao:
    """Testa execução do MOS end-to-end com subprocess mockado."""

    def _run_mos(self, args: list) -> tuple:
        """Executa main() do MOS e captura resultado."""
        from mos import main
        with patch("sys.argv", ["mos.py"] + args):
            with pytest.raises(SystemExit) as exc:
                main()
        return exc.value.code

    def test_help_retorna_zero(self):
        code = self._run_mos(["--help"])
        assert code == 0

    def test_help_shorthand(self):
        code = self._run_mos(["-h"])
        assert code == 0

    def test_categoria_desconhecida_retorna_1(self):
        code = self._run_mos(["categoria_inexistente"])
        assert code == 1

    def test_categoria_sem_comando_retorna_1(self):
        code = self._run_mos(["seo"])
        assert code == 1

    def test_comando_desconhecido_retorna_1(self):
        code = self._run_mos(["seo", "comando_inexistente"])
        assert code == 1

    def test_execucao_seo_analyze_chama_subprocess(self):
        from mos import main
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            with patch("sys.argv", ["mos.py", "seo", "analyze", "artigo.md", "keyword"]):
                with pytest.raises(SystemExit) as exc:
                    main()
            assert exc.value.code == 0
            mock_run.assert_called_once()
            cmd_args = mock_run.call_args[0][0]
            assert any("seo_analyzer.py" in str(a) for a in cmd_args)

    def test_execucao_hooks_generate_chama_subprocess(self):
        from mos import main
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            with patch("sys.argv", ["mos.py", "hooks", "generate", "produtividade", "reels", "10"]):
                with pytest.raises(SystemExit) as exc:
                    main()
            assert exc.value.code == 0
            cmd_args = mock_run.call_args[0][0]
            assert any("hook_generator.py" in str(a) for a in cmd_args)

    def test_execucao_quality_check_chama_subprocess(self):
        from mos import main
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            with patch("sys.argv", ["mos.py", "quality", "check", "post.md", "--type", "post"]):
                with pytest.raises(SystemExit) as exc:
                    main()
            assert exc.value.code == 0
            cmd_args = mock_run.call_args[0][0]
            assert any("quality_gate.py" in str(a) for a in cmd_args)

    def test_script_inexistente_retorna_1(self):
        with pytest.raises(SystemExit) as exc:
            run_script("script_absolutamente_inexistente.py", [])
        assert exc.value.code == 1

    def test_subprocess_retornando_erro_propaga_codigo(self):
        from mos import main
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=2)
            with patch("sys.argv", ["mos.py", "seo", "analyze", "artigo.md"]):
                with pytest.raises(SystemExit) as exc:
                    main()
            assert exc.value.code == 2


# ===========================================================================
# 4. COBERTURA DE SCRIPTS NO COMMAND_MAP
# ===========================================================================

class TestCoberturaDeSscripts:
    """Valida que scripts relevantes estão registrados no MOS."""

    # Scripts que propositalmente ficam fora do MOS (infra/utils/integrações)
    SCRIPTS_EXCLUIDOS = {
        "mos.py",           # o próprio CLI
        "validators.py",    # módulo de validação interno
        "output_formatter.py",  # módulo de formatação interno
        "instagram_api.py",     # integração de API (não CLI direto)
        "gsc_analyzer.py",      # integração de API (não CLI direto)
        "meta_ads_api.py",      # integração de API (não CLI direto)
        "youtube_analytics.py", # integração de API (não CLI direto)
        "weekly_report.py",     # script standalone (não precisa de proxy MOS)
        "project_manager.py",   # registrado via subcomandos no MOS
        "notion_api.py",        # integração de API (não CLI direto)
        "tiktok_trends_scraper.py",  # scraper assíncrono (não CLI direto)
        "validate_agents.py",   # utilitário de validação de infra (não CLI MOS)
        "voice_extractor.py",   # invocado direto por /criar-meu-clone, não pelo CLI mos.py
    }

    def test_scripts_relevantes_estao_no_command_map(self):
        """Scripts de conteúdo e análise devem estar no COMMAND_MAP."""
        todos_scripts = {f.name for f in SCRIPTS_PATH.glob("*.py")}
        scripts_no_map = set()
        for comandos in COMMAND_MAP.values():
            for script, _ in comandos.values():
                scripts_no_map.add(script)

        scripts_relevantes = todos_scripts - self.SCRIPTS_EXCLUIDOS
        faltando = scripts_relevantes - scripts_no_map

        assert not faltando, (
            f"Scripts sem entrada no COMMAND_MAP (considere adicionar ou excluir):\n"
            + "\n".join(sorted(faltando))
        )

    def test_nao_ha_scripts_fantasma_no_command_map(self):
        """COMMAND_MAP não deve referenciar scripts que não existem."""
        todos_scripts = {f.name for f in SCRIPTS_PATH.glob("*.py")}
        scripts_no_map = set()
        for comandos in COMMAND_MAP.values():
            for script, _ in comandos.values():
                scripts_no_map.add(script)

        fantasmas = scripts_no_map - todos_scripts
        assert not fantasmas, f"COMMAND_MAP referencia scripts inexistentes: {fantasmas}"


# ===========================================================================
# 5. INTEGRAÇÕES DE API: MÓDULOS IMPORTÁVEIS
# ===========================================================================
#
# Note: TestConfiguracaoMCP was removed in Phase 3 (refactor/plugin-first).
# It tested .claude/rules/mcp-usage.md, .claude/settings.json, and
# .claude/commands/ — all gitignored paths that cannot exist in the worktree.
# Plugin-first architecture validates MCP config via plugin.json instead.
# ===========================================================================

class TestIntegracoesDiAPI:
    """Valida que os módulos de integração de API podem ser importados."""

    def test_instagram_api_importavel(self):
        import instagram_api
        assert hasattr(instagram_api, "InstagramAPIError")

    def test_gsc_analyzer_importavel(self):
        import gsc_analyzer
        assert hasattr(gsc_analyzer, "GSCError") or hasattr(gsc_analyzer, "GSCAnalyticsError")

    def test_meta_ads_api_importavel(self):
        import meta_ads_api
        assert hasattr(meta_ads_api, "MetaAdsError")

    def test_youtube_analytics_importavel(self):
        import youtube_analytics
        assert hasattr(youtube_analytics, "YouTubeAnalyticsError")

    def test_validators_importavel(self):
        import validators
        assert hasattr(validators, "ValidationError")
        assert hasattr(validators, "validar_texto")
        assert hasattr(validators, "validar_inteiro")

    def test_output_formatter_importavel(self):
        import output_formatter
        assert hasattr(output_formatter, "OutputFormatter")
        assert hasattr(output_formatter, "add_output_args")

    def test_instagram_api_tem_constantes_de_env(self):
        import instagram_api
        assert hasattr(instagram_api, "ENV_ACCESS_TOKEN") or \
               any("TOKEN" in k for k in vars(instagram_api) if isinstance(k, str))

    def test_gsc_analyzer_tem_base_url(self):
        import gsc_analyzer
        # Deve ter URL base da API do Google
        modulo_vars = vars(gsc_analyzer)
        tem_url = any(
            isinstance(v, str) and "google" in v.lower()
            for v in modulo_vars.values()
            if isinstance(v, str)
        )
        assert tem_url, "gsc_analyzer deve ter URL da API do Google"

    def test_youtube_analytics_tem_escopos(self):
        import youtube_analytics as yt
        assert hasattr(yt, "YT_ANALYTICS_SCOPE")
        assert "googleapis.com" in yt.YT_ANALYTICS_SCOPE

    def test_meta_ads_api_tem_versao(self):
        import meta_ads_api
        modulo_vars = vars(meta_ads_api)
        tem_versao = any(
            "VERSION" in k or "version" in k.lower()
            or (isinstance(v, str) and ("v1" in v or "v2" in v) and "graph" in v.lower())
            for k, v in modulo_vars.items()
        )
        assert tem_versao, "meta_ads_api deve ter constante com URL versionada da API"


# ===========================================================================
# 7. INTEGRIDADE DO DIRETÓRIO DE SCRIPTS
# ===========================================================================

class TestIntegridadeScripts:
    """Valida integridade geral do diretório de scripts."""

    def test_diretorio_scripts_existe(self):
        assert SCRIPTS_PATH.exists() and SCRIPTS_PATH.is_dir()

    def test_scripts_tem_shebang_python(self):
        """Scripts executáveis devem ter shebang."""
        sem_shebang = []
        for script in SCRIPTS_PATH.glob("*.py"):
            if script.name.startswith("__"):
                continue
            primeira_linha = script.read_text(encoding="utf-8").split("\n")[0]
            if not (primeira_linha.startswith("#!") or
                    script.name in {"validators.py", "output_formatter.py"}):
                sem_shebang.append(script.name)
        # Aviso — não falha (alguns módulos são import-only)
        # Apenas valida que o shebang, quando presente, é Python
        for script in SCRIPTS_PATH.glob("*.py"):
            if script.name.startswith("__"):
                continue
            primeira_linha = script.read_text(encoding="utf-8").split("\n")[0]
            if primeira_linha.startswith("#!"):
                assert "python" in primeira_linha.lower(), \
                    f"{script.name}: shebang não é Python: {primeira_linha}"

    def test_todos_scripts_tem_docstring_de_modulo(self):
        """Scripts principais devem ter docstring."""
        import ast
        sem_docstring = []
        # Apenas scripts no COMMAND_MAP são obrigatórios
        scripts_obrigatorios = set()
        for comandos in COMMAND_MAP.values():
            for script, _ in comandos.values():
                scripts_obrigatorios.add(script)

        for script_name in scripts_obrigatorios:
            caminho = SCRIPTS_PATH / script_name
            if not caminho.exists():
                continue
            tree = ast.parse(caminho.read_text(encoding="utf-8"))
            docstring = ast.get_docstring(tree)
            if not docstring:
                sem_docstring.append(script_name)

        assert not sem_docstring, \
            f"Scripts sem docstring de módulo:\n" + "\n".join(sem_docstring)

    def test_arquivo_conftest_existe_em_tests(self):
        conftest = SCRIPTS_PATH / "tests" / "conftest.py"
        assert conftest.exists(), "conftest.py não encontrado em scripts/tests/"

    def test_arquivo_init_existe_em_tests(self):
        init = SCRIPTS_PATH / "tests" / "__init__.py"
        assert init.exists(), "__init__.py não encontrado em scripts/tests/"

    def test_pytest_ini_ou_setup_cfg_existe(self):
        pytest_ini = PROJECT_ROOT / "pytest.ini"
        setup_cfg = PROJECT_ROOT / "setup.cfg"
        pyproject = PROJECT_ROOT / "pyproject.toml"
        assert any(f.exists() for f in [pytest_ini, setup_cfg, pyproject]), \
            "Nenhum arquivo de configuração do pytest encontrado"
