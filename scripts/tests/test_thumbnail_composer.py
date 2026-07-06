"""Testes para thumbnail_composer.py — overlay tipográfico determinístico."""

from __future__ import annotations

import os
import sys

import pytest

PIL = pytest.importorskip("PIL", reason="Pillow é dependência da Fase 2 (mídia)")
from PIL import Image  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import thumbnail_composer as tc  # noqa: E402


@pytest.fixture
def bg(tmp_path):
    """Fundo 800x600 (não-16:9 de propósito, pra exercitar o cover)."""
    path = tmp_path / "fundo.png"
    Image.new("RGB", (800, 600), (180, 40, 40)).save(path)
    return str(path)


class TestCompose:
    def test_gera_png_1280x720(self, bg, tmp_path):
        out = str(tmp_path / "thumb.png")
        result = tc.compose(bg, "Como dobrar suas vendas", out)
        assert os.path.exists(result)
        with Image.open(result) as img:
            assert img.size == (1280, 720)

    def test_texto_com_acentos_pt_br(self, bg, tmp_path):
        out = str(tmp_path / "thumb.png")
        tc.compose(bg, "Promoção de verão já começou", out)
        assert os.path.exists(out)

    def test_texto_longo_quebra_sem_estourar(self, bg, tmp_path):
        out = str(tmp_path / "thumb.png")
        texto = "o guia definitivo e completo de marketing digital para pequenos negócios brasileiros em crescimento"
        tc.compose(bg, texto, out)
        with Image.open(out) as img:
            assert img.size == (1280, 720)

    @pytest.mark.parametrize("pos", ["top", "center", "bottom"])
    def test_posicoes(self, bg, tmp_path, pos):
        out = str(tmp_path / f"thumb-{pos}.png")
        tc.compose(bg, "Teste de posição", out, pos=pos)
        assert os.path.exists(out)

    def test_cria_diretorio_de_saida(self, bg, tmp_path):
        out = str(tmp_path / "sub" / "dir" / "thumb.png")
        tc.compose(bg, "Cria diretório", out)
        assert os.path.exists(out)

    def test_fundo_inexistente_levanta_erro(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            tc.compose(str(tmp_path / "nao-existe.png"), "x", str(tmp_path / "o.png"))

    def test_overlay_altera_pixels_do_fundo(self, bg, tmp_path):
        """A faixa de contraste + texto precisam aparecer de fato na imagem."""
        out = str(tmp_path / "thumb.png")
        tc.compose(bg, "Texto visível", out, pos="bottom")
        with Image.open(out) as img:
            # A posição vertical do bloco varia com o tamanho da fonte; varre a
            # metade inferior da coluna central procurando pixels da faixa/texto
            alterados = [
                img.getpixel((640, y)) != (180, 40, 40) for y in range(360, 720, 8)
            ]
            assert any(alterados), "nenhum pixel do overlay encontrado no fundo"


class TestHelpers:
    def test_cover_resize_sempre_1280x720(self):
        for size in [(800, 600), (1920, 1080), (500, 1000), (1280, 720)]:
            img = Image.new("RGB", size, (10, 10, 10))
            assert tc.cover_resize(img).size == (1280, 720)

    def test_wrap_by_width_nao_perde_palavras(self, bg, tmp_path):
        from PIL import ImageDraw

        draw = ImageDraw.Draw(Image.new("RGB", (100, 100)))
        font = tc.load_font(48)
        texto = "uma frase com várias palavras pra quebrar"
        lines = tc.wrap_by_width(draw, texto, font, 300)
        assert " ".join(lines).split() == texto.split()
