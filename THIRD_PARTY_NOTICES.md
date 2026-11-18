# Third-Party Notices & Attributions

Este projeto consolida, adapta e estende padrões arquiteturais de iniciativas open-source e documenta integrações externas opcionais utilizadas no ambiente de referência.

## 1. Projetos Referenciados e Inspiração Arquitetural

### Everything Claude Code (ECC)
- **Repositório:** `affaan-m/everything-claude-code` / `affaan-m/ECC` ([GitHub](https://github.com/affaan-m/everything-claude-code))
- **Licença e Copyright:** MIT License — `Copyright (c) 2026 Affaan Mustafa`
- **Uso neste repositório:** Consolidação conceitual de papéis (`planner`, `architect`, `build-error-resolver`, `refactor-cleaner`, `performance-optimizer`, `tdd-guide`, `e2e-runner`, `code-reviewer`, `security-reviewer`, `doc-updater`) em *Core Skills* modulares em Português (PT-BR).

### Conselho dos Anciões (`claude-skill-conselho-dos-ancioes`)
- **Repositório:** `gabrielcoutinhoDL/claude-skill-conselho-dos-ancioes` ([GitHub](https://github.com/gabrielcoutinhoDL/claude-skill-conselho-dos-ancioes))
- **Licença e Copyright:** MIT License — `Copyright (c) 2026 Gabriel Coutinho de Lima`
- **Uso neste repositório:** Inspiração para a skill `conselho-independente-dupla-familia` (1ª rodada cega entre famílias distintas de modelos, separação de convergências vs. exclusividades e estudo de caso de autenticação). Nesta arquitetura, o protocolo foi redesenhado para agentes permanentes nativos e governança SQL (`v_validacao_conselho`) com regra *Fail-Closed* (`CONSELHO INCOMPLETO`).

### Texto Integral da Licença MIT (Aplicável às Origens Acima)

```text
MIT License

Copyright (c) 2026 Affaan Mustafa (affaan-m/everything-claude-code)
Copyright (c) 2026 Gabriel Coutinho de Lima (gabrielcoutinhoDL/claude-skill-conselho-dos-ancioes)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 2. Plugins, MCPs e Ferramentas Externas do Ecossistema (Não Empacotadas)

As ferramentas abaixo compõem o stack completo documentado em [`docs/stack-plugins-mcps-economia.md`](docs/stack-plugins-mcps-economia.md) e nos exemplos em `configs/`, mas são projetos independentes instalados diretamente de seus repositórios oficiais:

- **OpenBot** — Runtime desktop *local-first* para agentes persistentes e comunicação inter-agentes.
- **Context Mode** (`mksglu/context-mode`, licença `Elastic-2.0`) — Servidor MCP de sandbox local e busca FTS5/BM25 para economia de janela de contexto.
- **Ponytail** (`DietrichGebert/ponytail`, licença `MIT`, `Copyright Dietrich Gebert`) — Modo *lazy senior dev* para diffs mínimos, verificação proporcional e respostas concisas.
- **Graphify** (`safishamsi`) — Geração de grafos de conhecimento de base de código.
- **Addy Osmani Agent Skills** (`addyosmani/agent-skills`) — Coleção complementar de skills de engenharia.
- **Anthropic Official Plugins** (`anthropics/claude-plugins-official`) — Plugins oficiais opcionais (`context7`, `security-guidance`, `frontend-design`, `playwright`).
- **Obsidian MCP** — Leitura e escrita estruturada em cofres Markdown locais.
- **yt-dlp** — Extração de legendas/transcrições públicas para o fluxo `mentor-estudo-80-20`.
