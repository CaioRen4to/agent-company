# Stack de Economia Máxima de Tokens, Plugins & MCPs

> Guia prático para manter **demandas grandes** dentro de **janelas curtas de cota (ex.: limite de 5 horas)** sem degradar a qualidade técnica.

---

## 1. Por que a cota de 5 horas acaba rápido?

Quatro gargalos costumam multiplicar o consumo de tokens em sessões longas:

1. **Saídas brutas no contexto:** despejar logs de testes, `git diff`, HTML, arquivos longos ou respostas de API diretamente na conversa.
2. **Janela gigante antes de compactar (`autoCompactWindow` alto):** esperar até `400k` tokens para compactar significa reenviar `200k–400k` tokens de histórico a cada novo turno.
3. **Excesso de schemas MCP *eager* e skills globais:** cada servidor MCP com dezenas de ferramentas carregadas em todos os agentes (ex.: mídia + deploy + design em agentes de banco de dados ou revisão) infla todos os turnos.
4. **Esforço máximo (`xhigh` / `high`) em tarefas simples e código verborrágico:** usar raciocínio máximo em checks rápidos de CLI ou gerar abstrações e explicações desnecessárias.

---

## 2. Stack de Economia e Projetos Upstream Utilizados

| Camada | Ferramenta / Repositório | Papel na Economia de Tokens |
|---|---|---|
| **Sandbox & Busca FTS5** | [Context Mode (`mksglu/context-mode`)](https://github.com/mksglu/context-mode) | Executa comandos, parsing e leitura de arquivos grandes em sandbox local com índice SQLite FTS5/BM25 (`ctx_execute`, `ctx_search`, `ctx_batch`), mantendo saídas brutas fora da janela de contexto. |
| **Código Enxuto & YAGNI** | [Ponytail (`DietrichGebert/ponytail`)](https://github.com/DietrichGebert/ponytail) | Ativa modo *senior dev* objetivo (`lite`, `full`, `ultra`): menor diff que resolve o problema por completo com verificação proporcional ao risco e respostas curtas. |
| **Grafo de Código** | Graphify (`safishamsi`) *(opcional)* | Constrói grafo de conhecimento do repositório (`graphify-out/`) para consultar relações e arquitetura sem abrir dezenas de arquivos crus. |
| **Base de Padrões & Papéis** | [Everything Claude Code (`affaan-m/everything-claude-code`)](https://github.com/affaan-m/everything-claude-code) | Origem conceitual dos papéis de engenharia, revisão multistack, testes e segurança, aqui consolidados em **8 Core Skills** modulares em vez de dezenas de prompts sempre ativos. |
| **Conselho Cego** | [Conselho dos Anciões (`gabrielcoutinhoDL/claude-skill-conselho-dos-ancioes`)](https://github.com/gabrielcoutinhoDL/claude-skill-conselho-dos-ancioes) | Referência para 1ª rodada cega independente com duas famílias distintas (`Claude` × `Gemini`) e trava SQL *Fail-Closed*. |
| **Memória Seletiva** | `obsidian-triagem` + `memoria-auditavel-obsidian-pena` | Lê primeiro apenas o manifesto/índice (`00-INDICE.md` / `context-manifest.json`) antes de abrir notas específicas, e grava com *read-back* verificável. |
| **Documentação Atualizada** | Context7 (`anthropics/claude-plugins-official`) | Consulta trechos exatos de documentação oficial sob demanda em vez de copiar páginas inteiras. |
| **Orquestração Multi-CLI** | `Alethe` *(opcional)* & `Addy Osmani Agent Skills` | Roteamento de subtarefas delimitadas por cota e checklists práticos de engenharia. |

---

## 3. Regras Práticas de Configuração (OpenBot & Claude Code)

### 3.1 Isolamento de MCPs por Agente
Use o template [`configs/mcp-servers.example.json`](../configs/mcp-servers.example.json) como referência:
- **Universais (engenharia/pesquisa/memória):** `context-mode` (e `obsidian` para quem lê/grava memória).
- **Sob demanda:** `context7` (pesquisa/arquitetura/backend/frontend/estudos), `github` (Maestro/Porteiro/Revisor).
- **Restritos ao departamento:** `elevenlabs` apenas em Mídia (`AI Content Factory`, `Publicador`); `vercel` apenas em `Pixel`/`Porteiro`. Nunca deixe 50+ tools *eager* ligadas em todos os 21 agentes.

### 3.2 Ajustes no Claude Code (`settings.json`)
Use [`configs/claude-settings.economy.example.json`](../configs/claude-settings.economy.example.json):
- Mantenha **`autoCompactWindow`** entre **`120000` e `150000`** (evite `400000` em uso contínuo para não multiplicar o custo de entrada por turno).
- Reserve **`effortLevel: "medium"`** como padrão e suba para `high` apenas em decisões críticas.
- Deixe habilitados apenas os plugins realmente usados na rotina diária (`context-mode`, `ponytail`, `ecc`, `context7`, `security-guidance`), evitando carregar 15–20 plugins sincronizados simultaneamente.

### 3.3 Limpeza de Orçamento de Skills no Orquestrador
- Não instale skills de especialistas (`frontend-design`, `mentor-estudo-80-20`) no agente coordenador (`JARVIS`), pois ele já delega aos donos da camada — isso evita que skills críticas como `context-mode` sejam cortadas do prompt por limite de orçamento.
- Instale `ponytail` nos executores de código/CLI (`Arquiteto`, `Pixel`, `Bento`, `Atlas`, `Fluxo`, `Sentinela`, `Revisor ECC`, `Guardião`, `Porteiro`), mantendo **`Mentor de Estudos`** (explicações didáticas) e **`Conselheiros`** (parecer completo) sem corte de verbosidade didática.
- Rebaixe o esforço de raciocínio de agentes puramente operacionais (`Porteiro`, `Pesquisador`, `Pena`, `Publicador`) para `medium` ou `low`.

---

## 4. Verificação Rápida

1. No terminal/MCP, confirme que **Node `>= 24.15.0`** está ativo para `context-mode v2.2+` e execute `ctx_doctor` para validar todas as 9 ferramentas (`ctx_execute`, `ctx_batch`, `ctx_index`, `ctx_search`, `ctx_resume`, `ctx_stats`, `ctx_doctor`, `ctx_upgrade`, `ctx_purge`).
2. Rode `python bench/measure_repo.py` neste repositório para validar manifesto, skills e schema SQLite *Fail-Closed*.
