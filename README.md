# Um Agente Só

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![Um Agente Só](guia/assets/banner.jpg)](https://inematds.github.io/um-agente-so/guia/)

## O que é

Um Agente Só é um kit aberto para quem usa o Claude Code (ou o Codex) e foi criando um agente para cada tarefa: uma pasta para vendas, outra para suporte, outra para conteúdo, cada uma com as suas regras e a sua memória. A própria Anthropic passou a recomendar o contrário: **um agente geral e muitas skills**. O modelo é o processador, o agente é o sistema operacional e as skills são os aplicativos; para fazer algo novo você instala um app, não compra outro computador. O kit mostra quantos "agentes" você já criou, quais regras se repetem entre eles, de que tipo são as suas skills e testa, às cegas, se uma skill ainda ajuda ou se o modelo novo já faz melhor sem ela.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/um-agente-so/guia/**

🎬 Vídeo: [Assistir no YouTube](https://www.youtube.com/watch?v=s2ve490BUl8)

## Comece sem instalar nada à mão

Abra o Claude Code ou o Codex e cole:

```text
Leia o kit "Um Agente Só" em https://github.com/inematds/um-agente-so (README, prompts/ e modelos/).
Quero trabalhar com UM agente principal e muitas skills, em vez de uma pasta de agente por tarefa.
1. Baixe o kit e rode o mapa.py sobre as minhas pastas de projetos (ele só lê). Me diga em linguagem
   simples: quantas pastas de agente (CLAUDE.md/AGENTS.md) eu tenho, quantas skills e de que tipo,
   quais descrições estão curtas demais e quais regras se repetem em várias pastas.
2. Siga prompts/juntar-agentes.txt: agrupe os agentes por assunto e proponha as skills que ficam no
   lugar deles, e as regras repetidas que viram UMA linha no CLAUDE.md principal.
3. Não apague, não mova e não edite nada. Só me mostre o plano e espere o meu sim.
4. Se eu quiser o teste às cegas (ab.py), me pergunte antes qual tarefa testar: ele usa duas
   respostas da minha assinatura do Claude.
```

Não há versão online: o mapa precisa olhar as pastas do seu computador. Para baixar os arquivos: [ZIP do kit](https://github.com/inematds/um-agente-so/archive/refs/heads/main.zip).

## As 4 ideias, em ordem

1. **Menos agentes.** Cada pasta de agente precisa ser treinada e mantida. Junte o trabalho num agente principal.
2. **Mais skills.** Skill é uma pasta com um `SKILL.md`. O nome e a descrição no topo decidem se o Claude abre a skill; escreva a descrição dizendo QUANDO usar.
3. **Skill nasce do trabalho.** Faça a tarefa uma vez com o Claude, corrija como corrigiria um estagiário e peça para virar skill (`prompts/faca-uma-vez.txt`). Skill não precisa ser lista de passos: pode ser um banco de dados, um material de marca ou uma frase.
4. **Teste sem skills de tempos em tempos.** A equipe do Claude Code tirou mais de 80% do prompt de sistema nos modelos novos sem perder qualidade. Instrução antiga pode segurar o modelo novo. `ab.py` mostra se a sua skill ainda ganha.

## A prova (máquina do INEMA, 26/11/2026)

| | |
|---|---|
| pastas de agente (CLAUDE.md/AGENTS.md) | **525** |
| skills instaladas | **119** (ferramenta 61, procedimento 28, artefato 26, banco 4) |
| skills com descrição curta demais | **51** |
| mesma regra repetida | em **65 a 73** pastas |

Teste A/B às cegas (notas de reunião, `claude-sonnet-5-5`): com skills 12,1 s e 160 palavras; sem nenhuma skill 10,6 s e 112 palavras. As duas entregaram quem faz o quê e o prazo, e a skill antiga (`ata-reuniao`) nem foi seguida. Detalhes em [`exemplos/prova-real.md`](exemplos/prova-real.md).

---

## Instalação técnica

Pré-requisitos: Python 3.8+ (só biblioteca padrão). Para o `ab.py`, o Claude Code instalado e logado (`claude`), pela assinatura.

```bash
git clone https://github.com/inematds/um-agente-so ~/um-agente-so
cd ~/um-agente-so
python3 mapa.py --raiz ~/projetos --md mapa.md     # só lê: agentes, skills e regras repetidas
```

Opções do `mapa.py`: `--raiz` (padrão `~`), `--profundidade` (padrão 3), `--md <arquivo>`. Ele também lê as pastas de skills padrão (`~/.claude/skills`, `~/.agents/skills`, `~/.codex/skills`).

Depois, o teste com e sem skills (usa o seu `claude` já logado, pela assinatura):

```bash
python3 ab.py "a tarefa que você faz toda semana" --pasta ~/seu-projeto
python3 ab.py --chave resultado-ab                 # só depois de escolher a melhor
```

Opções do `ab.py`: `--tarefa-arquivo`, `--pasta`, `--saida` (padrão `resultado-ab`), `--modelo`, `--teto` (segundos por rodada, padrão 600), `--semente`, `--chave <pasta>`.

### O que tem aqui

| arquivo | o quê |
|---|---|
| `mapa.py` | conta as pastas com CLAUDE.md/AGENTS.md (seus "agentes"), lista as skills por tipo, acha descrições curtas demais e regras repetidas entre pastas. Só leitura, sem IA e sem internet |
| `ab.py` | roda a mesma tarefa com as suas skills e com `--disable-slash-commands` (nenhuma skill), sorteia A/B e guarda a chave à parte |
| `modelos/` | os 4 tipos de skill: procedimento, banco (aponta para os seus dados), artefato (marca e layout) e definição (uma frase) |
| `prompts/juntar-agentes.txt` | plano para trocar várias pastas de agente por um agente principal + skills (não apaga nada) |
| `prompts/faca-uma-vez.txt` | faça a tarefa uma vez com o Claude e transforme a sessão em skill com o skill-creator |
| `prompts/conferir-skill-de-fora.txt` | antes de instalar skill de terceiros: o que ela faz, se acessa internet, senhas ou apaga arquivos |
| `exemplos/prova-real.md` | o kit rodado na máquina do INEMA: 525 pastas de agente, 119 skills, regra repetida em 73 pastas, teste A/B |
| `guia/` | o guia PT/EN/ES (GitHub Pages) |

### Testes

```bash
python3 -m unittest discover -s tests
```

## O processo, do início ao fim

1. 🧠 Você abre o Claude Code ou o Codex e cola o pedido acima.
2. 🤖 A IA baixa o kit: `git clone https://github.com/inematds/um-agente-so ~/um-agente-so`.
3. ⚙️ Mapa (só leitura): `python3 mapa.py --raiz ~/projetos --md mapa.md`.
4. 🤖 A IA lê o `mapa.md` e segue `prompts/juntar-agentes.txt`: grupos, skills propostas, regras que viram uma linha global.
5. 🧠 Você aprova (ou corta) o plano. Nada é apagado nem movido antes disso.
6. 🧠🤖 Tarefa nova vira skill: `prompts/faca-uma-vez.txt` + Skill Creator; os `modelos/` servem de ponto de partida.
7. ⚙️ Teste às cegas de uma tarefa: `python3 ab.py "<tarefa>" --pasta <projeto>` (duas respostas pela assinatura).
8. 🧠 Você lê A e B, escolhe e anota o porquê; só depois `python3 ab.py --chave resultado-ab`.
9. 🧠 Skill que empata ou perde: reescreva ou tire. Repita de tempos em tempos, a cada modelo novo.

## Baseado em (Anthropic)

- Palestra da Anthropic "Don't Build Agents, Build Skills Instead" (Barry Zhang e Mahesh Murag, AI Engineer Code Summit 2025): https://www.ai.engineer/talks/agent-skills
- Anthropic, "Equipping agents for the real world with Agent Skills": https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Anthropic, padrão aberto doado à Agentic AI Foundation: https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation
- Anthropic, "The new rules of context engineering for Claude 5 generation models": https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models

Kit do INEMA, não oficial da Anthropic.

## Kits irmãos

- [Ensine Uma Vez](https://inematds.github.io/ensine-uma-vez/guia/): de conversa que deu certo a procedimento que a IA repete.
- [Auditar Skills](https://inematds.github.io/auditar-skills/guia/): confere cada skill contra 46 regras.
- [Jogue fora os seus skills](https://github.com/inematds/jogue-fora-skills): faxina das skills que não ganham mais a vaga.

Projetos e cursos gratuitos: https://inema.club
