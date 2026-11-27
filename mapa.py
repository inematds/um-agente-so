#!/usr/bin/env python3
"""mapa.py — quantos "agentes" você criou e quais skills você já tem.

Só lê. Não altera nada, não usa internet nem IA.

Um "agente" aqui é uma pasta de trabalho com instruções próprias (CLAUDE.md ou AGENTS.md).
Cada uma precisa ser treinada de novo. A tese do Um Agente Só: poucas pastas, muitas skills.

Uso:
  python3 mapa.py                         # procura em ~ (até 3 níveis) e nas pastas de skills padrão
  python3 mapa.py --raiz ~/projetos --profundidade 2
  python3 mapa.py --md relatorio.md       # grava o relatório em Markdown
"""
from __future__ import annotations

import argparse
import collections
import os
import re
import sys
from pathlib import Path

VERSAO = "0.2.1"
INSTRUCOES = ("CLAUDE.md", "AGENTS.md")
PULAR = {".git", "node_modules", ".venv", "venv", "__pycache__", ".cache", ".npm", ".local",
         "snap", ".cargo", ".rustup", "go", "dist", "build", ".next", "site-packages"}
PASTAS_SKILLS = ("~/.claude/skills", "~/.agents/skills", "~/.codex/skills")


def achar_agentes(raiz: Path, profundidade: int) -> list[Path]:
    """Pastas (até `profundidade` níveis abaixo da raiz) que têm CLAUDE.md ou AGENTS.md."""
    achados = []
    base = len(raiz.parts)
    for dirpath, dirnames, filenames in os.walk(raiz):
        nivel = len(Path(dirpath).parts) - base
        dirnames[:] = [d for d in dirnames if d not in PULAR and not d.startswith(".")] if nivel < profundidade else []
        if any(f in filenames for f in INSTRUCOES):
            achados.append(Path(dirpath))
    return sorted(achados)


def ler_frontmatter(texto: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---", texto, re.S)
    campos = {}
    if m:
        for linha in m.group(1).splitlines():
            if ":" in linha and not linha.startswith(" "):
                k, v = linha.split(":", 1)
                campos[k.strip()] = v.strip().strip('"').strip("'")
    return campos


def tipo_da_skill(pasta: Path, texto: str) -> str:
    """Heurística simples dos 4 tipos (o nome é só uma etiqueta para você olhar)."""
    corpo = re.sub(r"^---.*?---", "", texto, count=1, flags=re.S)
    linhas = [l for l in corpo.splitlines() if l.strip()]
    arquivos = [p for p in pasta.rglob("*") if p.is_file() and p.name != "SKILL.md"]
    tem_codigo = any(p.suffix in {".py", ".sh", ".js", ".mjs", ".ts"} for p in arquivos)
    links = len(re.findall(r"https?://|\]\(|~/|/home/", corpo))
    marca = re.search(r"\b(cor(es)?|fonte|font|paleta|logo|#[0-9a-fA-F]{6})\b", corpo, re.I)
    if marca and not tem_codigo:
        return "artefato"
    passos = [l for l in linhas if re.match(r"\s*(\d+[.)]|[-*])\s", l)]
    if len(linhas) <= 4 and not arquivos and len(passos) < 2:
        return "definição"
    if links >= 8 and links > len(linhas) / 4:
        return "banco"
    if tem_codigo:
        return "ferramenta"
    return "procedimento"


def achar_skills() -> list[dict]:
    vistas = []
    for pasta_base in PASTAS_SKILLS:
        base = Path(os.path.expanduser(pasta_base))
        if not base.is_dir():
            continue
        for skill_md in sorted(base.glob("*/SKILL.md")):
            try:
                texto = skill_md.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            fm = ler_frontmatter(texto)
            vistas.append({
                "onde": pasta_base,
                "nome": fm.get("name", skill_md.parent.name),
                "descricao": fm.get("description", ""),
                "tipo": tipo_da_skill(skill_md.parent, texto),
                "palavras": len(texto.split()),
            })
    return vistas


def linhas_repetidas(agentes: list[Path], minimo: int = 3) -> list[tuple[str, int]]:
    """Regras que aparecem em várias pastas = candidatas a virar UMA skill (ou uma linha global)."""
    contagem = collections.Counter()
    for a in agentes:
        vistas = set()
        for nome in INSTRUCOES:
            arq = a / nome
            if arq.is_file():
                for l in arq.read_text(encoding="utf-8", errors="replace").splitlines():
                    l = re.sub(r"\s+", " ", l.strip(" -*#>")).strip()
                    if 25 <= len(l) <= 200:
                        vistas.add(l)
        contagem.update(vistas)
    return [(l, n) for l, n in contagem.most_common(15) if n >= minimo]


def relatorio(raiz: Path, agentes, skills, repetidas) -> str:
    out = [f"# Um Agente Só — mapa ({VERSAO})", "",
           f"Raiz procurada: `{raiz}`", "",
           "## Resumo", "",
           f"- **Agentes (pastas com instruções próprias): {len(agentes)}**",
           f"- **Skills instaladas: {len(skills)}**"]
    if skills:
        tipos = collections.Counter(s["tipo"] for s in skills)
        out.append("- Tipos: " + ", ".join(f"{t} {n}" for t, n in tipos.most_common()))
        curtas = [s for s in skills if len(s["descricao"]) < 40]
        out.append(f"- Skills com descrição curta demais (< 40 letras; o Claude decide pela descrição): {len(curtas)}")
    out += ["", "## Leitura", ""]
    if len(agentes) > 5:
        out.append(f"Você tem {len(agentes)} pastas que funcionam como agentes separados. Cada uma tem regra e memória próprias. "
                   "Junte o trabalho numa pasta principal e transforme o que se repete em skill (veja `prompts/juntar-agentes.txt`).")
    else:
        out.append("Poucas pastas de agente: bom. Agora invista nas skills que você mais usa.")
    if repetidas:
        out += ["", "## Regras repetidas em várias pastas (viram uma skill ou uma linha global)", "",
                "| vezes | regra |", "|---:|---|"]
        out += [f"| {n} | {l.replace('|', '/')[:160]} |" for l, n in repetidas]
    out += ["", "## Agentes encontrados", ""]
    out += [f"- `{a}`" for a in agentes[:200]]
    if len(agentes) > 200:
        out.append(f"- … e mais {len(agentes) - 200}")
    if skills:
        out += ["", "## Skills", "", "| tipo | nome | palavras | descrição |", "|---|---|---:|---|"]
        for s in sorted(skills, key=lambda s: (s["tipo"], s["nome"])):
            out.append(f"| {s['tipo']} | {s['nome']} | {s['palavras']} | {s['descricao'][:90].replace('|', '/')} |")
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Conta seus agentes e skills (só leitura).")
    ap.add_argument("--raiz", default="~", help="onde procurar pastas com CLAUDE.md/AGENTS.md (padrão: ~)")
    ap.add_argument("--profundidade", type=int, default=3)
    ap.add_argument("--md", help="grava o relatório neste arquivo")
    ap.add_argument("--versao", action="version", version=VERSAO)
    a = ap.parse_args(argv)
    raiz = Path(os.path.expanduser(a.raiz)).resolve()
    if not raiz.is_dir():
        print(f"raiz não existe: {raiz}", file=sys.stderr)
        return 2
    agentes = achar_agentes(raiz, a.profundidade)
    skills = achar_skills()
    texto = relatorio(raiz, agentes, skills, linhas_repetidas(agentes))
    if a.md:
        Path(a.md).write_text(texto, encoding="utf-8")
    print(texto if not a.md else texto.split("## Leitura")[0] + f"Relatório completo: {a.md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
