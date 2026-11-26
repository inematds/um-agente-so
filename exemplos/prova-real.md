# Prova real (máquina do INEMA, 26/11/2026)

## 1. Mapa — quantos "agentes" a gente criou

`python3 mapa.py --raiz ~/projetos --profundidade 2`

- **525 pastas com instruções próprias** (CLAUDE.md ou AGENTS.md) — 525 "agentes" que precisam ser mantidos um a um.
- **119 skills instaladas**: ferramenta 61, procedimento 28, artefato 26, banco 4.
- **51 skills com descrição curta demais** (< 40 letras). É pela descrição que o Claude decide se abre a skill.
- A mesma regra repetida em **65 a 73 pastas** (ex.: "quando eu te corrigir, grave a lição", "autor dos commits"). Isso é uma linha global ou UMA skill, não 73 cópias.

(Lista de pastas e skills fica só na máquina; não publicamos.)

## 2. Teste A/B — mesma tarefa com e sem skills, às cegas

`python3 ab.py "Organize as notas da reunião…" --pasta exemplos/projeto-teste --modelo claude-sonnet-5-5 --semente 7`

O projeto-teste tem uma skill antiga, `ata-reuniao` ("escreva ATA DE REUNIÃO… não tire conclusões… termine com Fim da ata").
Conferido antes: com a skill carregada o Claude responde "sim, tenho a ata-reuniao"; com `--disable-slash-commands`, "não".

| | com skills | sem nenhuma skill |
|---|---|---|
| tempo | 12,1 s | 10,6 s |
| tamanho | 160 palavras (tabela) | 112 palavras (lista) |
| quem faz o quê e prazo | sim | sim |
| seguiu a skill antiga ("ATA DE REUNIÃO", "Fim da ata") | não | — |

Leitura: o modelo novo entregou o que a equipe precisa nas duas rodadas, e a skill antiga nem foi seguida.
Ela só ocupa espaço: candidata a sair ou a ser reescrita. Respostas completas em `resultado-ab/`.
