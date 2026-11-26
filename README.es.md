# Um Agente Só — Un Solo Agente

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![Un Solo Agente](guia/assets/banner-es.jpg)](https://inematds.github.io/um-agente-so/guia/es/)

## Qué es

Un Solo Agente es un kit abierto para quien usa Claude Code (o Codex) y fue creando un agente para cada tarea: una carpeta para ventas, otra para soporte, otra para contenido, cada una con sus propias reglas y su propia memoria. La propia Anthropic pasó a recomendar lo contrario: **un agente general y muchas skills**. El modelo es el procesador, el agente es el sistema operativo y las skills son las aplicaciones; para hacer algo nuevo instalas una app, no compras otro ordenador. El kit muestra cuántos "agentes" has creado ya, qué reglas se repiten entre ellos, de qué tipo son tus skills y comprueba, a ciegas, si una skill todavía ayuda o si el modelo nuevo ya lo hace mejor sin ella.

## 📖 Guía de uso

Guía completa (landing + paso a paso): **https://inematds.github.io/um-agente-so/guia/es/**

🎬 Video: [Ver en YouTube](https://www.youtube.com/watch?v=s2ve490BUl8)

## Empieza sin instalar nada a mano

Abre Claude Code o Codex y pega:

```text
Lee el kit "Un Solo Agente" en https://github.com/inematds/um-agente-so (README, prompts/ y modelos/).
Quiero trabajar con UN agente principal y muchas skills, en vez de una carpeta de agente por tarea.
1. Descarga el kit y ejecuta mapa.py sobre mis carpetas de proyectos (solo lee). Dime en lenguaje
   sencillo: cuántas carpetas de agente (CLAUDE.md/AGENTS.md) tengo, cuántas skills y de qué tipo,
   qué descripciones son demasiado cortas y qué reglas se repiten en varias carpetas.
2. Sigue prompts/juntar-agentes.txt: agrupa los agentes por tema y propón las skills que quedan en
   su lugar, y las reglas repetidas que se convierten en UNA línea en el CLAUDE.md principal.
3. No borres, no muevas y no edites nada. Solo muéstrame el plan y espera mi sí.
4. Si quiero la prueba a ciegas (ab.py), pregúntame antes qué tarea probar: usa dos
   respuestas de mi suscripción de Claude.
```

No hay versión en línea: el mapa necesita mirar las carpetas de tu ordenador. Para descargar los archivos: [ZIP del kit](https://github.com/inematds/um-agente-so/archive/refs/heads/main.zip).

## Las 4 ideas, en orden

1. **Menos agentes.** Cada carpeta de agente hay que entrenarla y mantenerla. Junta el trabajo en un agente principal.
2. **Más skills.** Una skill es una carpeta con un `SKILL.md`. El nombre y la descripción de arriba deciden si Claude abre la skill; escribe la descripción diciendo CUÁNDO usarla.
3. **La skill nace del trabajo.** Haz la tarea una vez con Claude, corrige como corregirías a un becario y pide que se convierta en skill (`prompts/faca-uma-vez.txt` (en portugués)). Una skill no tiene por qué ser una lista de pasos: puede ser una base de datos, un material de marca o una frase.
4. **Prueba sin skills de vez en cuando.** El equipo de Claude Code quitó más del 80% del prompt de sistema en los modelos nuevos sin perder calidad. Una instrucción antigua puede frenar al modelo nuevo. `ab.py` muestra si tu skill todavía gana.

## La prueba (máquina de INEMA, 26/11/2026)

| | |
|---|---|
| carpetas de agente (CLAUDE.md/AGENTS.md) | **525** |
| skills instaladas | **119** (herramienta 61, procedimiento 28, artefacto 26, base 4) |
| skills con descripción demasiado corta | **51** |
| la misma regla repetida | en **65 a 73** carpetas |

Prueba A/B a ciegas (notas de reunión, `claude-sonnet-5-5`): con skills 12,1 s y 160 palabras; sin ninguna skill 10,6 s y 112 palabras. Las dos entregaron quién hace qué y el plazo, y la skill antigua (`ata-reuniao`) ni siquiera se siguió. Detalles en [`exemplos/prova-real.md`](exemplos/prova-real.md) (en portugués).

---

## Instalación técnica

Requisitos previos: Python 3.8+ (solo biblioteca estándar). Para `ab.py`, Claude Code instalado y con sesión iniciada (`claude`), mediante la suscripción.

```bash
git clone https://github.com/inematds/um-agente-so ~/um-agente-so
cd ~/um-agente-so
python3 mapa.py --raiz ~/projetos --md mapa.md     # solo lee: agentes, skills y reglas repetidas
```

Opciones de `mapa.py`: `--raiz` (por defecto `~`), `--profundidade` (por defecto 3), `--md <archivo>`. También lee las carpetas de skills estándar (`~/.claude/skills`, `~/.agents/skills`, `~/.codex/skills`).

Después, la prueba con y sin skills (usa tu `claude` con la sesión ya iniciada, mediante la suscripción):

```bash
python3 ab.py "la tarea que haces cada semana" --pasta ~/seu-projeto
python3 ab.py --chave resultado-ab                 # solo después de elegir la mejor
```

Opciones de `ab.py`: `--tarefa-arquivo`, `--pasta`, `--saida` (por defecto `resultado-ab`), `--modelo`, `--teto` (segundos por ronda, por defecto 600), `--semente`, `--chave <carpeta>`.

### Qué hay aquí

| archivo | qué es |
|---|---|
| `mapa.py` | cuenta las carpetas con CLAUDE.md/AGENTS.md (tus "agentes"), lista las skills por tipo, encuentra descripciones demasiado cortas y reglas repetidas entre carpetas. Solo lectura, sin IA y sin internet |
| `ab.py` | ejecuta la misma tarea con tus skills y con `--disable-slash-commands` (ninguna skill), sortea A/B y guarda la clave aparte |
| `modelos/` | los 4 tipos de skill: procedimiento, base (apunta a tus datos), artefacto (marca y diseño) y definición (una frase) |
| `prompts/juntar-agentes.txt` (en portugués) | plan para cambiar varias carpetas de agente por un agente principal + skills (no borra nada) |
| `prompts/faca-uma-vez.txt` (en portugués) | haz la tarea una vez con Claude y convierte la sesión en skill con skill-creator |
| `prompts/conferir-skill-de-fora.txt` (en portugués) | antes de instalar una skill de terceros: qué hace, si accede a internet o a contraseñas, o si borra archivos |
| `exemplos/prova-real.md` (en portugués) | el kit ejecutado en la máquina de INEMA: 525 carpetas de agente, 119 skills, regla repetida en 73 carpetas, prueba A/B |
| `guia/` | la guía PT/EN/ES (GitHub Pages) |

### Pruebas

```bash
python3 -m unittest discover -s tests
```

## El proceso, de principio a fin

1. 🧠 Abres Claude Code o Codex y pegas la petición de arriba.
2. 🤖 La IA descarga el kit: `git clone https://github.com/inematds/um-agente-so ~/um-agente-so`.
3. ⚙️ Mapa (solo lectura): `python3 mapa.py --raiz ~/projetos --md mapa.md`.
4. 🤖 La IA lee `mapa.md` y sigue `prompts/juntar-agentes.txt` (en portugués): grupos, skills propuestas, reglas que se convierten en una línea global.
5. 🧠 Apruebas (o recortas) el plan. Nada se borra ni se mueve antes de eso.
6. 🧠🤖 Una tarea nueva se convierte en skill: `prompts/faca-uma-vez.txt` (en portugués) + Skill Creator; los `modelos/` sirven de punto de partida.
7. ⚙️ Prueba a ciegas de una tarea: `python3 ab.py "<tarea>" --pasta <proyecto>` (dos respuestas mediante la suscripción).
8. 🧠 Lees A y B, eliges y anotas el porqué; solo después `python3 ab.py --chave resultado-ab`.
9. 🧠 Skill que empata o pierde: reescríbela o quítala. Repítelo de vez en cuando, con cada modelo nuevo.

## Basado en (Anthropic)

- Charla de Anthropic "Don't Build Agents, Build Skills Instead" (Barry Zhang y Mahesh Murag, AI Engineer Code Summit 2025): https://www.ai.engineer/talks/agent-skills
- Anthropic, "Equipping agents for the real world with Agent Skills": https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Anthropic, estándar abierto donado a la Agentic AI Foundation: https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation
- Anthropic, "The new rules of context engineering for Claude 5 generation models": https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models

Kit de INEMA, no oficial de Anthropic.

## Kits hermanos

- [Ensine Uma Vez](https://inematds.github.io/ensine-uma-vez/guia/): de una conversación que salió bien a un procedimiento que la IA repite.
- [Auditar Skills](https://inematds.github.io/auditar-skills/guia/): revisa cada skill según 46 reglas.
- [Jogue fora os seus skills](https://github.com/inematds/jogue-fora-skills) (en portugués): limpieza de las skills que ya no se ganan su sitio.

Proyectos y cursos gratuitos: https://inema.club
