#!/usr/bin/env python3
"""podar.py — o que a sua skill ensina que o modelo novo já sabe fazer.

Só lê. Não altera nenhum arquivo, não usa internet nem IA.

Lê um ou mais SKILL.md (ou pastas com skills) e classifica cada linha de
instrução em dois grupos:

  PASSO    o "como fazer": verbo de procedimento no começo, lista
           numerada, "primeiro / depois / em seguida / por fim".
           Candidato a cortar quando o modelo novo já faz sozinho.
  GUARDAR  o que o modelo não tem como saber:
           correção   "nunca", "não prometa", "evite", "fale de você"
           definição  "X significa", "para nós", "chamamos de"
           marca      cor (#FACC15), fonte, logo, tom de voz
           dados      número, caminho de arquivo, e-mail, nome próprio
  neutro   frase que não bate com nenhuma regra (fica fora da conta).

% de passo = passo ÷ (passo + guardar). O neutro não entra.
As listas de palavras são em português (com poucas em inglês e
espanhol): skill escrita em outra língua cai mais no neutro.

Ordem de decisão (a primeira que bate vence):
  correção > definição > marca > dados > passo > neutro
Por quê: "1. Nunca prometa prazo" é uma correção, não um passo. E um
passo que carrega um dado seu ("Abra clientes.csv") fica no GUARDAR:
o modelo não sabe o nome do seu arquivo.

O que não entra na conta: o cabeçalho (--- name/description ---),
títulos (#), linhas em branco, comentários <!-- --> de uma linha e o
conteúdo de blocos de código.
Acentos e maiúsculas não importam (o texto é normalizado antes).

É heurística: uma lista de palavras, não um juiz. Antes de cortar,
rode a tarefa com e sem a skill no ab.py e compare.

Uso:
  python3 podar.py minha-skill/SKILL.md
  python3 podar.py ~/.claude/skills            # todas as skills da pasta
  python3 podar.py a/SKILL.md b/SKILL.md --json
  python3 podar.py minha-skill --todos         # lista todas as linhas
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

VERSAO = "0.2.2"

GUARDAR = ("correção", "definição", "marca", "dados")


def _sem_acento(texto: str) -> str:
    nfd = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


def _rx(*padroes: str) -> re.Pattern:
    return re.compile("|".join(padroes))


# Regras escritas sem acento e em minúsculas (o texto é normalizado).
CORRECAO = _rx(
    r"\b(nunca|jamais|evite|evitar|proibido|never|avoid)\b",
    r"\bnao (prometa|use|usa|escreva|diga|coloque|ponha|invente|mande"
    r"|cite|mencione|repita|comece|termine|chame|trate|faca|envie)\b",
    r"\b(em vez de|no lugar de|en vez de|no prometas|don'?t)\b",
    r"\bfale (de|com) voce\b|\btrate (o|a|os|as) .+ por\b",
    r"^sem\b",
)
DEFINICAO = _rx(
    r"\b(significa|quer dizer|para nos|pra nos|chamamos de"
    r"|entendemos por|means|para nosotros)\b",
    r"^[\"“'][^\"”']+[\"”'] ?(=|:|e )",
)
MARCA = _rx(
    r"#[0-9a-f]{3}(?:[0-9a-f]{3})?\b",
    r"\b(cor|cores|fonte|fontes|tipografia|paleta|logo|logotipo"
    r"|negrito|font|fonts|color|colors|colores)\b",
    r"\btom (de voz|formal|informal|leve|direto|serio)\b",
)
DADOS = _rx(
    r"\d",
    r"[\w.-]+@[\w-]+\.\w+",
    r"(~/|\./|\b[\w-]+/[\w./-]+)",
    r"\b[\w-]+\.(csv|xlsx|xls|json|md|pdf|txt|docx|html)\b",
    r"\br\$",
)
PASSO = _rx(
    r"^(primeiro|depois|em seguida|por fim|finalmente|entao|antes de"
    r"|ao terminar|no final|first|then|next|finally|primero|despues)\b",
    r"^(passo|etapa|step|paso)\b",
    r"^(abra|leia|releia|escreva|use|faca|crie|monte|gere|verifique"
    r"|confira|cheque|revise|copie|cole|salve|envie|comece|separe"
    r"|organize|liste|divida|formate|coloque|adicione|inclua|resuma"
    r"|identifique|analise|pense|garanta|certifique-se|compare|ordene"
    r"|numere|termine|finalize|pergunte|explique|mantenha|procure"
    r"|busque|anote|registre|corrija|ajuste|defina|escolha|leve"
    r"|considere|lembre-se|seja|deixe|tenha|read|write|check|open"
    r"|lee|escribe|revisa|abre)\b",
)

# Nome próprio: Palavra com inicial maiúscula (não tudo em CAIXA ALTA)
# que não abre a frase.
NOME_PROPRIO = re.compile(
    r"(?<![.!?:]\s)(?<!^)\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]{2,}")
COMUNS = {"Claude", "Markdown", "SKILL", "PDF", "Use", "Para", "Não"}

MARCADOR = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+|\[[ x]\]\s+)")


def linhas_de_instrucao(texto: str):
    """(número da linha, texto limpo, era lista numerada)."""
    linhas = texto.splitlines()
    i = 0
    if linhas and linhas[0].strip() == "---":
        for j in range(1, len(linhas)):
            if linhas[j].strip() == "---":
                i = j + 1
                break
    em_codigo = False
    for n in range(i, len(linhas)):
        bruta = linhas[n].strip()
        if bruta.startswith("```"):
            em_codigo = not em_codigo
            continue
        if (em_codigo or not bruta or bruta.startswith("#")
                or bruta.startswith("<!--")):
            continue
        if set(bruta) <= set("|-: "):
            continue
        numerada = bool(re.match(r"^\d+[.)]\s+", bruta))
        limpa = MARCADOR.sub("", bruta).strip().strip("|").strip()
        limpa = re.sub(r"[*_`]", "", limpa)
        if limpa:
            yield n + 1, limpa, numerada


def classificar(texto: str, numerada: bool = False) -> str:
    """Devolve: correção, definição, marca, dados, passo ou neutro."""
    t = _sem_acento(texto).strip()
    if CORRECAO.search(t):
        return "correção"
    if DEFINICAO.search(t):
        return "definição"
    if MARCA.search(t):
        return "marca"
    if DADOS.search(t):
        return "dados"
    nomes = [m for m in NOME_PROPRIO.findall(texto) if m not in COMUNS]
    if nomes:
        return "dados"
    if numerada or PASSO.search(t):
        return "passo"
    return "neutro"


def nome_da_skill(texto: str, caminho: str) -> str:
    m = re.search(r"^name:\s*[\"']?([^\"'\n]+)", texto, re.M)
    return m.group(1).strip() if m else Path(caminho).parent.name


def analisar(caminho: str) -> dict:
    texto = Path(caminho).read_text(encoding="utf-8", errors="replace")
    itens = [{"linha": n, "tipo": classificar(t, num), "texto": t}
             for n, t, num in linhas_de_instrucao(texto)]
    conta = {k: 0 for k in ("passo",) + GUARDAR + ("neutro",)}
    for it in itens:
        conta[it["tipo"]] += 1
    total = len(itens)
    contadas = conta["passo"] + sum(conta[k] for k in GUARDAR)
    return {
        "arquivo": caminho,
        "skill": nome_da_skill(texto, caminho),
        "linhas": total,
        "contagem": conta,
        "guardar": sum(conta[k] for k in GUARDAR),
        "contadas": contadas,
        "pct_passo": (round(100 * conta["passo"] / contadas)
                      if contadas else 0),
        "itens": itens,
    }


def achar_skills(alvos: list[str]) -> list[str]:
    achados = []
    for alvo in alvos:
        p = Path(alvo)
        if p.is_dir():
            if (p / "SKILL.md").is_file():
                achados.append(str(p / "SKILL.md"))
            else:
                achados += [str(x) for x in sorted(p.rglob("SKILL.md"))]
        elif p.is_file():
            achados.append(alvo)
        else:
            raise FileNotFoundError(alvo)
    return achados


def _corta(texto: str, largura: int = 56) -> str:
    return texto if len(texto) <= largura else texto[:largura - 1] + "…"


def relatorio(r: dict, maximo: int) -> str:
    c = r["contagem"]
    out = [f"{r['arquivo']}  (skill: {r['skill']})",
           f"  {r['linhas']} linhas de instrução lidas",
           f"  PASSO (como fazer, candidato a cortar) {c['passo']:>4}"
           f"  ({r['pct_passo']}% de {r['contadas']})",
           f"  GUARDAR (o modelo não sabe)            {r['guardar']:>4}",
           "    " + " · ".join(f"{k} {c[k]}" for k in GUARDAR),
           f"  neutro (fora da conta)                 {c['neutro']:>4}"]
    for titulo, filtro in (("Passos", lambda t: t == "passo"),
                           ("Guardar", lambda t: t in GUARDAR)):
        sel = [it for it in r["itens"] if filtro(it["tipo"])]
        if not sel:
            continue
        out.append(f"\n  {titulo}:")
        for it in sel[:maximo]:
            rot = "" if it["tipo"] == "passo" else f"[{it['tipo']}] "
            out.append(f"    L{it['linha']:<3} {rot}"
                       f"{_corta(it['texto'], 58 - len(rot))}")
        if len(sel) > maximo:
            out.append(f"    … e mais {len(sel) - maximo}"
                       " (use --todos)")
    return "\n".join(out)


RECOMENDA = (
    "Recomendação: não corte no escuro. Rode a mesma tarefa com e sem\n"
    "a skill (python3 ab.py \"<tarefa>\" --pasta <projeto>) e compare.\n"
    "Saiu igual ou melhor sem os passos? Corte os passos e guarde os\n"
    "dados, a marca, as definições e as correções.")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Separa PASSO (candidato a cortar) de CONTEXTO "
                    "(guardar) em SKILL.md. Só lê.")
    ap.add_argument("alvos", nargs="+",
                    help="SKILL.md ou pasta com skills")
    ap.add_argument("--json", action="store_true",
                    help="saída em JSON")
    ap.add_argument("--max", type=int, default=6,
                    help="trechos por lista (padrão 6)")
    ap.add_argument("--todos", action="store_true",
                    help="lista todas as linhas")
    a = ap.parse_args(argv)
    try:
        arquivos = achar_skills(a.alvos)
    except FileNotFoundError as e:
        print(f"Não achei: {e}", file=sys.stderr)
        return 2
    if not arquivos:
        print("Nenhum SKILL.md encontrado.", file=sys.stderr)
        return 2
    rs = [analisar(f) for f in arquivos]
    if a.json:
        print(json.dumps(rs, ensure_ascii=False, indent=2))
        return 0
    maximo = 10 ** 6 if a.todos else a.max
    print("podar.py — PASSO (como fazer) × GUARDAR (o que só você sabe)\n")
    print("\n\n".join(relatorio(r, maximo) for r in rs))
    if len(rs) > 1:
        tl = sum(r["linhas"] for r in rs)
        tc = sum(r["contadas"] for r in rs)
        tp = sum(r["contagem"]["passo"] for r in rs)
        pct = round(100 * tp / tc) if tc else 0
        print(f"\nTotal: {len(rs)} skills, {tl} linhas, {tp} de passo"
              f" ({pct}% de {tc} passo + guardar)")
    print("\n" + RECOMENDA)
    return 0


if __name__ == "__main__":
    sys.exit(main())
