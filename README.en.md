# Um Agente Só — One Agent Only

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![One Agent Only](guia/assets/banner-en.jpg)](https://inematds.github.io/um-agente-so/guia/en/)

## What it is

One Agent Only is an open kit for people who use Claude Code (or Codex) and have been creating one agent for each task: a folder for sales, another for support, another for content, each with its own rules and its own memory. Anthropic itself now recommends the opposite: **one general agent and many skills**. The model is the processor, the agent is the operating system and skills are the apps; to do something new you install an app, you don't buy another computer. The kit shows how many "agents" you have already created, which rules repeat across them, what types your skills are, and runs a blind test of whether a skill still helps or whether the new model already does better without it.

## 📖 User guide

Full guide (landing + step by step): **https://inematds.github.io/um-agente-so/guia/en/**

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

### What's in here

| file | what |
|---|---|
| `mapa.py` | counts the folders with CLAUDE.md/AGENTS.md (your "agents"), lists skills by type, finds descriptions that are too short and rules repeated across folders. Read-only, no AI and no internet |
| `ab.py` | runs the same task with your skills and with `--disable-slash-commands` (no skills), randomizes A/B and stores the key separately |
| `modelos/` | the 4 types of skill: procedure, database (points to your data), artifact (brand and layout) and definition (one sentence) |
| `prompts/juntar-agentes.txt` (in Portuguese) | plan to replace several agent folders with one main agent + skills (deletes nothing) |
| `prompts/faca-uma-vez.txt` (in Portuguese) | do the task once with Claude and turn the session into a skill with skill-creator |
| `prompts/conferir-skill-de-fora.txt` (in Portuguese) | before installing a third-party skill: what it does, whether it accesses the internet or passwords, or deletes files |
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
9. 🧠 A skill that ties or loses: rewrite it or remove it. Repeat from time to time, with each new model.

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
