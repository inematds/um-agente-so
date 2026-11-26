# Um Agente Só

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

Um Agente Só é um kit aberto para quem usa o Claude Code (ou o Codex) e foi criando um agente para cada tarefa: uma pasta para vendas, outra para suporte, outra para conteúdo, cada uma com as suas regras e a sua memória. A própria Anthropic passou a recomendar o contrário: **um agente geral e muitas skills**. O modelo é o processador, o agente é o sistema operacional e as skills são os aplicativos; para fazer algo novo você instala um app, não compra outro computador. O kit mostra quantos "agentes" você já criou, quais regras se repetem entre eles, de que tipo são as suas skills e testa, às cegas, se uma skill ainda ajuda ou se o modelo novo já faz melhor sem ela.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/um-agente-so/guia/**

## Comece em três comandos

```bash
git clone https://github.com/inematds/um-agente-so ~/um-agente-so
cd ~/um-agente-so
python3 mapa.py --raiz ~/projetos --md mapa.md     # só lê: agentes, skills e regras repetidas
```

Depois, o teste com e sem skills (usa o seu `claude` já logado, pela assinatura):

```bash
python3 ab.py "a tarefa que você faz toda semana" --pasta ~/seu-projeto
python3 ab.py --chave resultado-ab                 # só depois de escolher a melhor
```

## O que tem aqui

| arquivo | o quê |
|---|---|
| `mapa.py` | conta as pastas com CLAUDE.md/AGENTS.md (seus "agentes"), lista as skills por tipo, acha descrições curtas demais e regras repetidas entre pastas. Só leitura, sem IA e sem internet |
| `ab.py` | roda a mesma tarefa com as suas skills e com `--disable-slash-commands` (nenhuma skill), sorteia A/B e guarda a chave à parte |
| `modelos/` | os 4 tipos de skill: procedimento, banco (aponta para os seus dados), artefato (marca e layout) e definição (uma frase) |
| `prompts/juntar-agentes.txt` | plano para trocar várias pastas de agente por um agente principal + skills (não apaga nada) |
| `prompts/faca-uma-vez.txt` | faça a tarefa uma vez com o Claude e transforme a sessão em skill com o skill-creator |
| `prompts/conferir-skill-de-fora.txt` | antes de instalar skill de terceiros: o que ela faz, se acessa internet, senhas ou apaga arquivos |
| `exemplos/prova-real.md` | o kit rodado na máquina do INEMA: 525 pastas de agente, 119 skills, regra repetida em 73 pastas, teste A/B |

## As 4 ideias, em ordem

1. **Menos agentes.** Cada pasta de agente precisa ser treinada e mantida. Junte o trabalho num agente principal.
2. **Mais skills.** Skill é uma pasta com um `SKILL.md`. O nome e a descrição no topo decidem se o Claude abre a skill; escreva a descrição dizendo QUANDO usar.
3. **Skill nasce do trabalho.** Faça a tarefa uma vez com o Claude, corrija como corrigiria um estagiário e peça para virar skill (`prompts/faca-uma-vez.txt`). Skill não precisa ser lista de passos: pode ser um banco de dados, um material de marca ou uma frase.
4. **Teste sem skills de tempos em tempos.** A equipe do Claude Code tirou mais de 80% do prompt de sistema nos modelos novos sem perder qualidade. Instrução antiga pode segurar o modelo novo. `ab.py` mostra se a sua skill ainda ganha.

## Fontes

- Palestra da Anthropic "Don't Build Agents, Build Skills Instead" (Barry Zhang e Mahesh Murag): https://www.ai.engineer/talks/agent-skills
- Anthropic, "Equipping agents for the real world with Agent Skills": https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Anthropic, padrão aberto doado à Agentic AI Foundation: https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation
- Anthropic, "The new rules of context engineering for Claude 5 generation models": https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models

## Kits irmãos

- [Ensine Uma Vez](https://inematds.github.io/ensine-uma-vez/guia/): de conversa que deu certo a procedimento que a IA repete.
- [Auditar Skills](https://inematds.github.io/auditar-skills/guia/): confere cada skill contra 46 regras.
- [Jogue fora os seus skills](https://github.com/inematds/jogue-fora-skills): faxina das skills que não ganham mais a vaga.

## Testes

```bash
python3 -m unittest discover -s tests
```

Projetos e cursos gratuitos: https://inema.club
