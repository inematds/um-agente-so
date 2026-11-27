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

## Los 6 niveles para dar skills a tu agente

| nivel | qué hacer | archivo del kit |
|---|---|---|
| 1 | Pídele a Claude que escriba la skill con skill-creator (la skill oficial de Anthropic) y adjunta 2 o 3 ejemplos tuyos. Pon en las instrucciones generales: "usa siempre skill-creator cuando te pida una skill". | `prompts/nivel1-peca-ao-claude.txt` |
| 2 | **El más recomendado.** Haz la tarea una vez con Claude, corrígelo como corregirías a un practicante y al final pídele "convierte esta sesión en una skill". ¿Hay una regla nueva? Pídele que actualice la skill. | `prompts/faca-uma-vez.txt` · `exemplos/seis-niveis/email-cliente-v1` → `email-cliente-v2` |
| 3 | Graba la pantalla mientras haces la tarea y di qué haces y por qué (Win+G u OBS, gratis). Entrega el video, o la transcripción con tiempos, y pide la skill. | `prompts/nivel3-grave-a-tela.txt` |
| 4 | Guarda el contexto una sola vez, en skills pequeñas: datos, marca, definiciones. Las skills de trabajo citan esas piezas, como LEGO: si cambia el logo, lo cambias en un solo lugar. | `exemplos/seis-niveis/marca`, `definicoes`, `proposta-curta` · `modelos/` |
| 5 | Usa skills de otras personas: el formato es un estándar abierto ([agentskills.io](https://agentskills.io)) y suele funcionar en varias herramientas. Solo de fuentes confiables, y pídele a Claude que las revise antes. | `prompts/conferir-skill-de-fora.txt` |
| 6 | Haz una poda de vez en cuando. Corta los PASOS (el "cómo hacerlo", que el modelo nuevo ya hace solo) y guarda lo que no tiene forma de saber: tus datos, tu marca, tus definiciones y tus correcciones. Prueba antes de cortar. | `podar.py` + `ab.py` |

`podar.py` solo lee: separa, en cada `SKILL.md`, lo que es paso (candidato a cortar) de lo que es contexto (guardar). Ejecutado en la skill inflada de ejemplo (`python3 podar.py exemplos/seis-niveis/relatorio-inchado/SKILL.md`, salida congelada en [`exemplos/seis-niveis/saida-podar.txt`](exemplos/seis-niveis/saida-podar.txt)):

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

La prueba tiene la última palabra: ejecuta la misma tarea con y sin la skill en `ab.py`. Si el resultado sale igual o mejor sin los pasos, corta los pasos.

Límite: las listas de palabras de `podar.py` están en portugués, para skills escritas en frases. Ejecutado en las 70 skills de esta máquina, terminó sin errores, pero en una skill en inglés o llena de código la mayor parte de las líneas cae en datos (cualquier número, ruta o nombre) o en neutro. Ahí solo sirve para encontrar los pasos obvios.

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

Para ver qué podar en una skill (solo lee, no cambia nada):

```bash
python3 podar.py ~/.claude/skills/minha-skill/SKILL.md
python3 podar.py ~/.claude/skills --json          # todas las skills de la carpeta, en JSON
```

Opciones de `podar.py`: uno o más `SKILL.md` o carpetas, `--json`, `--max <n>` (fragmentos por lista, 6 por defecto), `--todos`.

### Qué hay aquí

| archivo | qué es |
|---|---|
| `mapa.py` | cuenta las carpetas con CLAUDE.md/AGENTS.md (tus "agentes"), lista las skills por tipo, encuentra descripciones demasiado cortas y reglas repetidas entre carpetas. Solo lectura, sin IA y sin internet |
| `podar.py` | lee uno o más `SKILL.md` y separa PASO (el "cómo hacerlo", candidato a cortar) de GUARDAR (datos, marca, definiciones, correcciones). Solo lectura, sin IA y sin internet. La heurística está explicada al inicio del archivo |
| `ab.py` | ejecuta la misma tarea con tus skills y con `--disable-slash-commands` (ninguna skill), sortea A/B y guarda la clave aparte |
| `modelos/` | los 4 tipos de skill: procedimiento, base (apunta a tus datos), artefacto (marca y diseño) y definición (una frase) |
| `prompts/juntar-agentes.txt` (en portugués) | plan para cambiar varias carpetas de agente por un agente principal + skills (no borra nada) |
| `prompts/nivel1-peca-ao-claude.txt` (en portugués) | nivel 1: pide la skill a skill-creator y adjunta 2 o 3 ejemplos tuyos |
| `prompts/nivel3-grave-a-tela.txt` (en portugués) | nivel 3: graba la pantalla mientras haces la tarea, narra el porqué y entrégaselo a Claude |
| `prompts/faca-uma-vez.txt` (en portugués) | haz la tarea una vez con Claude y convierte la sesión en skill con skill-creator |
| `prompts/conferir-skill-de-fora.txt` (en portugués) | antes de instalar una skill de terceros: qué hace, si accede a internet o a contraseñas, o si borra archivos |
| `exemplos/seis-niveis/` | ejemplos de los niveles: e-mail v1 → v2 (correcciones acumuladas), marca + definiciones + propuesta que cita las dos (LEGO), una skill inflada y la salida de `podar.py` |
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
9. ⚙️ Poda (solo lectura): `python3 podar.py <pasta-de-skills>` señala los pasos que el modelo nuevo quizá ya haga solo.
10. 🧠 Si una skill empata o pierde en `ab.py`: corta los pasos y guarda datos, marca, definiciones y correcciones; o quita la skill. Repite de vez en cuando, con cada modelo nuevo.

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
