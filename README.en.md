# Um Agente Só — One Agent Only

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![One Agent Only](guia/assets/banner-en.jpg)](https://inematds.github.io/um-agente-so/guia/en/)

## What it is

One Agent Only is an open kit for people who use Claude Code (or Codex) and have been creating one agent for each task: a folder for sales, another for support, another for content, each with its own rules and its own memory. Anthropic itself now recommends the opposite: **one general agent and many skills**. The model is the processor, the agent is the operating system and skills are the apps; to do something new you install an app, you don't buy another computer. The kit shows how many "agents" you have already created, which rules repeat across them, what types your skills are, and runs a blind test of whether a skill still helps or whether the new model already does better without it.

## 📖 User guide

Full guide (landing + step by step): **https://inematds.github.io/um-agente-so/guia/en/**

🎬 Video: [Watch on YouTube](https://www.youtube.com/watch?v=s2ve490BUl8)

## Start without installing anything by hand

Open Claude Code or Codex and paste:

```text
Read the "One Agent Only" kit at https://github.com/inematds/um-agente-so (README, prompts/ and modelos/).
I want to work with ONE main agent and many skills, instead of one agent folder per task.
1. Download the kit and run mapa.py over my project folders (it only reads). Tell me in plain
   language: how many agent folders (CLAUDE.md/AGENTS.md) I have, how many skills and of what type,
   which descriptions are too short and which rules repeat across several folders.
2. Follow prompts/juntar-agentes.txt: group the agents by subject and propose the skills that take
   their place, and the repeated rules that become ONE line in the main CLAUDE.md.
3. Do not delete, move or edit anything. Just show me the plan and wait for my yes.
4. If I want the blind test (ab.py), ask me first which task to test: it uses two
   responses from my Claude subscription.
```

There is no online version: the map needs to look at the folders on your computer. To download the files: [kit ZIP](https://github.com/inematds/um-agente-so/archive/refs/heads/main.zip).

## The 4 ideas, in order

1. **Fewer agents.** Each agent folder needs to be trained and maintained. Bring the work together in one main agent.
2. **More skills.** A skill is a folder with a `SKILL.md`. The name and description at the top decide whether Claude opens the skill; write the description saying WHEN to use it.
3. **Skills are born from the work.** Do the task once with Claude, correct it the way you would correct an intern and ask for it to become a skill (`prompts/faca-uma-vez.txt`). A skill doesn't have to be a list of steps: it can be a database, brand material or a single sentence.
4. **Test without skills from time to time.** The Claude Code team removed more than 80% of the system prompt on the new models without losing quality. An old instruction can hold the new model back. `ab.py` shows whether your skill still wins.

## The 6 levels of giving skills to your agent

| level | what to do | kit file |
|---|---|---|
| 1 | Ask Claude to write the skill with skill-creator (Anthropic's official skill), and attach 2 or 3 examples of your own. Add this to your general instructions: "always use skill-creator when I ask for a skill". | `prompts/nivel1-peca-ao-claude.txt` |
| 2 | **The most recommended.** Do the task once with Claude, correct it as you would correct an intern, and at the end ask "turn this session into a skill". New rule? Ask it to update the skill. | `prompts/faca-uma-vez.txt` · `exemplos/seis-niveis/email-cliente-v1` → `email-cliente-v2` |
| 3 | Record your screen while you do the task, and say what you do and why (Win+G or OBS, free). Hand over the video, or the transcript with timestamps, and ask for the skill. | `prompts/nivel3-grave-a-tela.txt` |
| 4 | Store your context once, in small skills: data, brand, definitions. Your work skills cite these pieces, like LEGO: when the logo changes, you change it in one place only. | `exemplos/seis-niveis/marca`, `definicoes`, `proposta-curta` · `modelos/` |
| 5 | Use other people's skills: the format is an open standard ([agentskills.io](https://agentskills.io)) and usually works in several tools. Use only trusted sources, and ask Claude to review them first. | `prompts/conferir-skill-de-fora.txt` |
| 6 | Prune from time to time. Cut the STEPS (the "how to do it", which a new model does on its own) and keep what it has no way of knowing: your data, your brand, your definitions, and your corrections. Test before you cut. | `podar.py` + `ab.py` |

`podar.py` only reads: in each `SKILL.md`, it separates steps (candidates to cut) from context (keep). Here it is, run on the bloated example skill (`python3 podar.py exemplos/seis-niveis/relatorio-inchado/SKILL.md`, frozen output in [`exemplos/seis-niveis/saida-podar.txt`](exemplos/seis-niveis/saida-podar.txt)):

```text
podar.py — PASSO (como fazer) × GUARDAR (o que só você sabe)

exemplos/seis-niveis/relatorio-inchado/SKILL.md  (skill: relatorio-semanal)
  27 linhas de instrução lidas
  PASSO (como fazer, candidato a cortar)   21  (78% de 27)
  GUARDAR (o modelo não sabe)               6
    correção 2 · definição 1 · marca 1 · dados 2
  neutro (fora da conta)                    0

  Passos:
    L9   Primeiro, leia com atenção todo o material que eu colar.
    L10  Depois, separe os pedidos por cliente.
    L11  Organize as informações em ordem de importância.
    L12  Pense passo a passo antes de escrever qualquer coisa.
    L13  Identifique os pontos principais de cada pedido.
    L14  Escreva um título claro no topo do relatório.
    … e mais 15 (use --todos)

  Guardar:
    L31  [correção] Seja objetivo e evite enrolação.
    L37  [dados] Os pedidos da semana estão em pedidos/semana.csv.
    L38  [dados] Mande para a Marta (dona da loja), não para o cai…
    L39  [definição] "Pedido parado" significa sem resposta do cli…
    L40  [correção] Nunca mostre o valor que cada cliente deve; só…
    L41  [marca] Cores do gráfico: verde #0E7C66 para pago, cinza …

Recomendação: não corte no escuro. Rode a mesma tarefa com e sem
a skill (python3 ab.py "<tarefa>" --pasta <projeto>) e compare.
Saiu igual ou melhor sem os passos? Corte os passos e guarde os
dados, a marca, as definições e as correções.
```

The test has the final word: run the same task with and without the skill in `ab.py`. If the result is the same or better without the steps, cut the steps.

Limit: the word lists in `podar.py` are in Portuguese, for skills written in sentences. Run on the 70 skills on this machine, it finished without errors, but in skills written in English or full of code, most lines fall into data (any number, path or name) or neutral. There it only helps find the obvious steps.

## The proof (INEMA machine, 26/11/2026)

| | |
|---|---|
| agent folders (CLAUDE.md/AGENTS.md) | **525** |
| installed skills | **119** (tool 61, procedure 28, artifact 26, database 4) |
| skills with a description that is too short | **51** |
| same rule repeated | in **65 to 73** folders |

Blind A/B test (meeting notes, `claude-sonnet-5-5`): with skills 12.1 s and 160 words; without any skill 10.6 s and 112 words. Both delivered who does what and the deadline, and the old skill (`ata-reuniao`) wasn't even followed. Details in [`exemplos/prova-real.md`](exemplos/prova-real.md) (in Portuguese).

---

## Technical setup

Prerequisites: Python 3.8+ (standard library only). For `ab.py`, Claude Code installed and logged in (`claude`), through the subscription.

```bash
git clone https://github.com/inematds/um-agente-so ~/um-agente-so
cd ~/um-agente-so
python3 mapa.py --raiz ~/projetos --md mapa.md     # read-only: agents, skills and repeated rules
```

`mapa.py` options: `--raiz` (default `~`), `--profundidade` (default 3), `--md <file>`. It also reads the standard skill folders (`~/.claude/skills`, `~/.agents/skills`, `~/.codex/skills`).

Then the test with and without skills (uses your already logged-in `claude`, through the subscription):

```bash
python3 ab.py "the task you do every week" --pasta ~/your-project
python3 ab.py --chave resultado-ab                 # only after choosing the best one
```

`ab.py` options: `--tarefa-arquivo`, `--pasta`, `--saida` (default `resultado-ab`), `--modelo`, `--teto` (seconds per run, default 600), `--semente`, `--chave <folder>`.

To see what you can prune in a skill (it only reads, it changes nothing):

```bash
python3 podar.py ~/.claude/skills/minha-skill/SKILL.md
python3 podar.py ~/.claude/skills --json          # all skills in the folder, as JSON
```

`podar.py` options: one or more `SKILL.md` files or folders, `--json`, `--max <n>` (excerpts per list, default 6), `--todos`.

### What's in here

| file | what |
|---|---|
| `mapa.py` | counts the folders with CLAUDE.md/AGENTS.md (your "agents"), lists skills by type, finds descriptions that are too short and rules repeated across folders. Read-only, no AI and no internet |
| `podar.py` | reads one or more `SKILL.md` files and separates STEP (the "how to do it", a candidate to cut) from KEEP (data, brand, definitions, corrections). Read-only, no AI and no internet. The heuristic is explained at the top of the file |
| `ab.py` | runs the same task with your skills and with `--disable-slash-commands` (no skills), randomizes A/B and stores the key separately |
| `modelos/` | the 4 types of skill: procedure, database (points to your data), artifact (brand and layout) and definition (one sentence) |
| `prompts/juntar-agentes.txt` (in Portuguese) | plan to replace several agent folders with one main agent + skills (deletes nothing) |
| `prompts/nivel1-peca-ao-claude.txt` (in Portuguese) | level 1: ask skill-creator for the skill and attach 2 or 3 examples of your own |
| `prompts/nivel3-grave-a-tela.txt` (in Portuguese) | level 3: record your screen while you do the task, narrate the why, and hand it to Claude |
| `prompts/faca-uma-vez.txt` (in Portuguese) | do the task once with Claude and turn the session into a skill with skill-creator |
| `prompts/conferir-skill-de-fora.txt` (in Portuguese) | before installing a third-party skill: what it does, whether it accesses the internet or passwords, or deletes files |
| `exemplos/seis-niveis/` | examples of the levels: email v1 → v2 (accumulated corrections), brand + definitions + a proposal that cites both (LEGO), a bloated skill, and the output of `podar.py` |
| `exemplos/prova-real.md` (in Portuguese) | the kit run on the INEMA machine: 525 agent folders, 119 skills, a rule repeated in 73 folders, A/B test |
| `guia/` | the PT/EN/ES guide (GitHub Pages) |

### Tests

```bash
python3 -m unittest discover -s tests
```

## The process, start to finish

1. 🧠 You open Claude Code or Codex and paste the request above.
2. 🤖 The AI downloads the kit: `git clone https://github.com/inematds/um-agente-so ~/um-agente-so`.
3. ⚙️ Map (read-only): `python3 mapa.py --raiz ~/projetos --md mapa.md`.
4. 🤖 The AI reads `mapa.md` and follows `prompts/juntar-agentes.txt`: groups, proposed skills, rules that become one global line.
5. 🧠 You approve (or cut) the plan. Nothing is deleted or moved before that.
6. 🧠🤖 A new task becomes a skill: `prompts/faca-uma-vez.txt` + Skill Creator; the `modelos/` serve as a starting point.
7. ⚙️ Blind test of a task: `python3 ab.py "<task>" --pasta <project>` (two responses through the subscription).
8. 🧠 You read A and B, choose and write down why; only then `python3 ab.py --chave resultado-ab`.
9. ⚙️ Pruning (read-only): `python3 podar.py <pasta-de-skills>` points out the steps that a new model may already do on its own.
10. 🧠 A skill that ties or loses in `ab.py`: cut the steps and keep data, brand, definitions, and corrections; or remove the skill. Repeat from time to time, with each new model.

## Based on (Anthropic)

- Anthropic talk "Don't Build Agents, Build Skills Instead" (Barry Zhang and Mahesh Murag, AI Engineer Code Summit 2025): https://www.ai.engineer/talks/agent-skills
- Anthropic, "Equipping agents for the real world with Agent Skills": https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Anthropic, open standard donated to the Agentic AI Foundation: https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation
- Anthropic, "The new rules of context engineering for Claude 5 generation models": https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models

An INEMA kit, not official from Anthropic.

## Sibling kits

- [Ensine Uma Vez](https://inematds.github.io/ensine-uma-vez/guia/) (in Portuguese): from a conversation that worked to a procedure the AI repeats.
- [Auditar Skills](https://inematds.github.io/auditar-skills/guia/) (in Portuguese): checks each skill against 46 rules.
- [Jogue fora os seus skills](https://github.com/inematds/jogue-fora-skills) (in Portuguese): cleanup of the skills that no longer earn their place.

Free projects and courses: https://inema.club
