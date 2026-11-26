import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
import ab  # noqa: E402
import mapa  # noqa: E402


class TestMapa(unittest.TestCase):
    def test_acha_agentes_e_regras_repetidas(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            for nome in ("vendas", "suporte", "conteudo"):
                (d / nome).mkdir()
                (d / nome / "CLAUDE.md").write_text("Responda sempre em português, com frases curtas e diretas.\n")
            (d / "sem-agente").mkdir()
            ags = mapa.achar_agentes(d, 2)
            self.assertEqual(len(ags), 3)
            rep = mapa.linhas_repetidas(ags)
            self.assertEqual(rep[0][1], 3)

    def test_profundidade_limita(self):
        with tempfile.TemporaryDirectory() as d:
            fundo = Path(d) / "a" / "b" / "c"
            fundo.mkdir(parents=True)
            (fundo / "AGENTS.md").write_text("x")
            self.assertEqual(mapa.achar_agentes(Path(d), 2), [])
            self.assertEqual(len(mapa.achar_agentes(Path(d), 3)), 1)

    def test_tipos_dos_modelos(self):
        esperado = {"definicao": "definição", "artefato": "artefato", "procedimento": "procedimento"}
        for pasta, tipo in esperado.items():
            p = RAIZ / "modelos" / pasta
            self.assertEqual(mapa.tipo_da_skill(p, (p / "SKILL.md").read_text()), tipo, pasta)

    def test_frontmatter(self):
        fm = mapa.ler_frontmatter("---\nname: x\ndescription: \"faz y\"\n---\ncorpo")
        self.assertEqual(fm, {"name": "x", "description": "faz y"})

    def test_cli_grava_md(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "p").mkdir()
            (Path(d) / "p" / "CLAUDE.md").write_text("oi")
            md = Path(d) / "m.md"
            r = subprocess.run([sys.executable, str(RAIZ / "mapa.py"), "--raiz", d, "--md", str(md)],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("Agentes (pastas com instruções próprias): 1", md.read_text())


class TestAB(unittest.TestCase):
    def test_as_cegas_com_chave(self):
        def falso(cmd, **kw):
            texto = "sem" if "--disable-slash-commands" in cmd else "com"
            return mock.Mock(stdout=texto, stderr="", returncode=0)
        with tempfile.TemporaryDirectory() as d, \
                mock.patch.object(ab.subprocess, "run", side_effect=falso), \
                mock.patch.object(ab.shutil, "which", return_value="/bin/claude"):
            self.assertEqual(ab.main(["tarefa x", "--pasta", d, "--saida", f"{d}/r", "--semente", "1"]), 0)
            chave = json.loads(Path(f"{d}/r/.chave.json").read_text())
            self.assertEqual(sorted([chave["A"], chave["B"]]), ["com skills", "sem skills"])
            for rot in ("A", "B"):
                esperado = "sem" if chave[rot] == "sem skills" else "com"
                self.assertEqual(Path(f"{d}/r/{rot}.md").read_text().strip(), esperado)
            comparar = Path(f"{d}/r/comparar.md").read_text()
            self.assertNotIn("com skills", comparar.split("## Resposta A")[1])

    def test_sem_claude(self):
        with mock.patch.object(ab.shutil, "which", return_value=None):
            self.assertEqual(ab.main(["x"]), 2)


if __name__ == "__main__":
    unittest.main()
