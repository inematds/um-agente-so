import html
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
import podar  # noqa: E402

EX = RAIZ / "exemplos" / "seis-niveis"
INCHADA = "exemplos/seis-niveis/relatorio-inchado/SKILL.md"


def rodar(*args, cwd=RAIZ):
    return subprocess.run([sys.executable, str(RAIZ / "podar.py"), *args],
                          capture_output=True, text=True, cwd=cwd)


def foto(pasta: Path) -> dict:
    return {str(p.relative_to(pasta)): p.read_bytes() if p.is_file() else None
            for p in sorted(pasta.rglob("*"))}


class TestClassificar(unittest.TestCase):
    def test_um_caso_por_tipo(self):
        casos = {
            "Depois, separe os pedidos por cliente.": "passo",
            "Revise o texto antes de entregar.": "passo",
            "Nunca mostre o valor de cada cliente.": "correção",
            "Não prometa prazo de entrega.": "correção",
            "Fale de você com cliente antigo.": "correção",
            "Sem saudação longa.": "correção",
            '"Pedido parado" significa sem resposta.': "definição",
            "Para nós, orçamento fechado é o aprovado.": "definição",
            "Destaque #0E7C66, títulos em Sora.": "marca",
            "Fontes: corpo em Inter.": "marca",
            "Os pedidos estão em pedidos/semana.csv.": "dados",
            "Mande para a Marta, não para o caixa.": "dados",
            "Telefone: (51) 3000-0000.": "dados",
            "Uma frase qualquer sem regra.": "neutro",
        }
        for texto, tipo in casos.items():
            self.assertEqual(podar.classificar(texto), tipo, texto)

    def test_lista_numerada_e_passo(self):
        self.assertEqual(podar.classificar("Faça o relatório", True), "passo")
        self.assertEqual(podar.classificar("o relatório", True), "passo")

    def test_correcao_vence_passo(self):
        self.assertEqual(podar.classificar("Use nunca mais de uma página"),
                         "correção")
        self.assertEqual(podar.classificar("Nunca prometa prazo", True),
                         "correção")

    def test_passo_com_dado_fica_no_guardar(self):
        self.assertEqual(podar.classificar("Abra clientes.csv", True), "dados")

    def test_acento_e_maiuscula_nao_importam(self):
        self.assertEqual(podar.classificar("NAO PROMETA PRAZO"), "correção")
        self.assertEqual(podar.classificar("primeiro, LEIA tudo"), "passo")

    def test_ignora_cabecalho_titulo_e_codigo(self):
        texto = ("---\nname: x\ndescription: Nunca use isto\n---\n"
                 "# Nunca prometa\n\n```\nnunca\n```\n<!-- nunca -->\n- Leia o pedido.\n")
        itens = list(podar.linhas_de_instrucao(texto))
        self.assertEqual([t for _, t, _ in itens], ["Leia o pedido."])
        self.assertEqual(itens[0][0], 11)


class TestExemplos(unittest.TestCase):
    def test_definicao_sem_passo(self):
        r = podar.analisar(str(RAIZ / "modelos" / "definicao" / "SKILL.md"))
        self.assertEqual(r["contagem"]["passo"], 0)

    def test_email_v2_tem_tres_correcoes_a_mais(self):
        v1 = podar.analisar(str(EX / "email-cliente-v1" / "SKILL.md"))
        v2 = podar.analisar(str(EX / "email-cliente-v2" / "SKILL.md"))
        self.assertEqual(v1["contagem"]["correção"], 0)
        self.assertEqual(v2["contagem"]["correção"], 3)

    def test_proposta_nao_guarda_cor_nem_fonte(self):
        texto = (EX / "proposta-curta" / "SKILL.md").read_text()
        self.assertNotRegex(texto, r"#[0-9A-Fa-f]{6}")
        self.assertNotIn("Sora", texto)
        self.assertIn("`marca`", texto)
        self.assertIn("`definicoes`", texto)

    def test_inchada_maioria_passo(self):
        r = podar.analisar(str(RAIZ / INCHADA))
        self.assertGreater(r["pct_passo"], 50)
        self.assertGreater(r["guardar"], 0)

    def test_neutro_fica_fora_da_porcentagem(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "SKILL.md"
            f.write_text("- Leia o pedido.\n- Nunca prometa prazo.\n"
                         "- Uma frase qualquer.\n- Outra frase solta.\n")
            r = podar.analisar(str(f))
        self.assertEqual(r["contagem"]["neutro"], 2)
        self.assertEqual(r["contadas"], 2)
        self.assertEqual(r["pct_passo"], 50)

    def test_saida_congelada_bate(self):
        r = rodar(INCHADA)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout, (EX / "saida-podar.txt").read_text())

    def test_saida_esta_nos_tres_guias(self):
        linhas = [ln.strip() for ln in
                  (EX / "saida-podar.txt").read_text().splitlines()
                  if ln.strip()]
        for guia in ("guia/index.html", "guia/en/index.html",
                     "guia/es/index.html"):
            pagina = (RAIZ / guia).read_text()
            for ln in linhas:
                self.assertTrue(html.escape(ln, quote=False) in pagina,
                                f"{guia} sem a linha: {ln}")


class TestCLI(unittest.TestCase):
    def test_json(self):
        r = rodar(str(EX), "--json")
        self.assertEqual(r.returncode, 0, r.stderr)
        dados = json.loads(r.stdout)
        self.assertEqual(len(dados), 6)
        for item in dados:
            self.assertEqual(set(item["contagem"]),
                             {"passo", "correção", "definição", "marca",
                              "dados", "neutro"})
            self.assertEqual(sum(item["contagem"].values()), item["linhas"])

    def test_nao_escreve_nada(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "s").mkdir()
            (d / "s" / "SKILL.md").write_text(
                "---\nname: s\ndescription: teste\n---\n1. Leia tudo.\n"
                "- Nunca prometa prazo.\n")
            antes = foto(d)
            for extra in ((), ("--json",), ("--todos",)):
                r = rodar(str(d), *extra, cwd=d)
                self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(foto(d), antes)

    def test_alvo_inexistente(self):
        self.assertEqual(podar.main(["/nao/existe/SKILL.md"]), 2)


if __name__ == "__main__":
    unittest.main()
