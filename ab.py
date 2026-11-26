#!/usr/bin/env python3
"""ab.py — a mesma tarefa COM as suas skills e SEM nenhuma skill, às cegas.

A equipe do Claude Code recomenda: de tempos em tempos, veja o que o modelo faz sem as suas
instruções. Às vezes a skill antiga está segurando o modelo novo ("hobbling").

Roda `claude -p` duas vezes no mesmo diretório:
  - normal (CLAUDE.md, skills e plugins carregados);
  - com `--disable-slash-commands` (nenhuma skill nem comando).
Sorteia quem é A e quem é B, grava as duas respostas lado a lado e guarda a chave à parte.
Você lê, escolhe a melhor e só depois abre a chave.

Uso:
  python3 ab.py "faça um resumo de uma página da reunião em notas.txt" --pasta ~/meu-projeto
  python3 ab.py --tarefa-arquivo tarefa.txt --saida resultado-ab
  python3 ab.py "..." --modelo claude-sonnet-5-5 --teto 600
  python3 ab.py --chave resultado-ab          # depois de escolher: mostra quem era quem

Usa a SUA assinatura do Claude Code (o comando `claude` já logado). Não chama API.
"""
from __future__ import annotations

import argparse
import json
import random
import shutil
import subprocess
import sys
import time
from pathlib import Path

VERSAO = "0.1.0"
SEM_SKILL = ["--disable-slash-commands"]


def rodar(tarefa: str, pasta: Path, extra: list[str], modelo: str | None, teto: int) -> dict:
    cmd = ["claude", "-p", tarefa, "--output-format", "text", *extra]
    if modelo:
        cmd += ["--model", modelo]
    ini = time.time()
    try:
        r = subprocess.run(cmd, cwd=pasta, capture_output=True, text=True, timeout=teto, stdin=subprocess.DEVNULL)
        texto, erro, cod = r.stdout.strip(), r.stderr.strip()[-500:], r.returncode
    except subprocess.TimeoutExpired:
        texto, erro, cod = "", f"passou de {teto} s", 124
    return {"comando": " ".join(cmd[:2] + ["<tarefa>"] + cmd[3:]), "segundos": round(time.time() - ini, 1),
            "palavras": len(texto.split()), "codigo": cod, "erro": erro, "texto": texto}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Tarefa com e sem skills, às cegas.")
    ap.add_argument("tarefa", nargs="?", help="o pedido, entre aspas")
    ap.add_argument("--tarefa-arquivo")
    ap.add_argument("--pasta", default=".", help="onde o claude roda (o projeto da tarefa)")
    ap.add_argument("--saida", default="resultado-ab")
    ap.add_argument("--modelo")
    ap.add_argument("--teto", type=int, default=600, help="segundos por rodada")
    ap.add_argument("--semente", type=int)
    ap.add_argument("--chave", metavar="PASTA", help="mostra quem era A e quem era B")
    ap.add_argument("--versao", action="version", version=VERSAO)
    a = ap.parse_args(argv)

    if a.chave:
        k = json.loads((Path(a.chave) / ".chave.json").read_text(encoding="utf-8"))
        print(f"A = {k['A']}\nB = {k['B']}")
        return 0

    tarefa = Path(a.tarefa_arquivo).read_text(encoding="utf-8") if a.tarefa_arquivo else a.tarefa
    if not tarefa:
        ap.error("passe a tarefa entre aspas ou --tarefa-arquivo")
    if not shutil.which("claude"):
        print("comando `claude` não encontrado (instale o Claude Code e faça login)", file=sys.stderr)
        return 2
    pasta = Path(a.pasta).expanduser().resolve()
    saida = Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)

    rodadas = {"com skills": rodar(tarefa, pasta, [], a.modelo, a.teto),
               "sem skills": rodar(tarefa, pasta, SEM_SKILL, a.modelo, a.teto)}
    ordem = list(rodadas)
    random.Random(a.semente).shuffle(ordem)
    chave = {"A": ordem[0], "B": ordem[1]}

    linhas = [f"# Teste A/B — com e sem skills ({VERSAO})", "", f"**Tarefa:** {tarefa.strip()}", "",
              "Leia as duas, escolha a melhor e anote o porquê. Só depois rode "
              f"`python3 ab.py --chave {saida}`.", ""]
    for rotulo in ("A", "B"):
        r = rodadas[chave[rotulo]]
        (saida / f"{rotulo}.md").write_text(r["texto"] + "\n", encoding="utf-8")
        linhas += [f"## Resposta {rotulo}", "", f"_{r['segundos']} s · {r['palavras']} palavras_", ""]
        linhas += [r["texto"] or f"(sem resposta: {r['erro']})", ""]
    linhas += ["## Sua escolha", "", "- Melhor: A / B / empate", "- Por quê:", ""]
    (saida / "comparar.md").write_text("\n".join(linhas), encoding="utf-8")
    (saida / ".chave.json").write_text(json.dumps({**chave, "rodadas": {k: {x: v for x, v in r.items() if x != "texto"}
                                                                          for k, r in rodadas.items()}},
                                                   ensure_ascii=False, indent=1), encoding="utf-8")
    for rotulo in ("A", "B"):
        r = rodadas[chave[rotulo]]
        print(f"{rotulo}: {r['segundos']} s, {r['palavras']} palavras, código {r['codigo']}")
    print(f"compare em: {saida / 'comparar.md'}")
    return 0 if all(r["codigo"] == 0 for r in rodadas.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
