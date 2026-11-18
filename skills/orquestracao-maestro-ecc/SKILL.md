---
name: orquestracao-maestro-ecc
description: Protocolo de coordenação de missões, delegação por pacote de 5 itens, controle de revisões (máximo 2 ciclos), acionamento do Conselho Independente e registro de estado para o JARVIS — Maestro.
---

# orquestracao-maestro-ecc

Use este procedimento ao coordenar qualquer missão que envolva múltiplos especialistas (no OpenBot via `openbot.send_message`, no Claude Code via subagentes/Agent tool ou em outros orquestradores).

## 1. Prioridade de consulta (Contexto Mínimo)
1. Instruções vigentes (`AGENTS.md` / `CLAUDE.md`).
2. Índice e decisões do projeto na memória estruturada (`00-INDICE.md`, `03-DECISOES.md`).
3. Grafo de arquitetura e estado real do código do projeto.
4. Documentação oficial via `Pesquisador` quando houver dúvida de versão ou API.

## 2. Pacote obrigatório de delegação (5 itens)
Toda delegação enviada a um especialista deve ser autossuficiente e conter:
1. **Pedido original e resultado esperado.**
2. **Projeto, diretório e versão/revisão do trabalho.**
3. **Restrições e decisões já aprovadas.**
4. **Arquivos sob responsabilidade exclusiva do especialista** (nunca dois agentes editando o mesmo arquivo em paralelo).
5. **Critérios objetivos de aceite e evidências exigidas no retorno.**

## 3. Fluxo de qualidade e limite de retrabalho
- **Planejamento:** `Produto e Negócios` (requisitos) e `Arquiteto` (plano técnico e critérios de aceite).
- **Implementação:** `Pixel` (frontend/UI/a11y), `Bento` (backend/API), `Atlas` (dados/SQL) e `Fluxo` (automação/webhooks).
- **Verificação:** `Sentinela` (testes unitários/integração/E2E), `Revisor ECC` (revisão cruzada multistack) e `Guardião` (segurança defensiva).
- **Estudo e Aprendizagem:** `Mentor de Estudos` (revisão didática e destilação 80/20).
- **Limite de correção:** no máximo **2 rodadas de correção** por falha. Se persistir, marcar a missão como `Bloqueada` e escalar ao CEO com opções claras.

## 4. Acionamento do Conselho Independente
Acione `Conselheiro Claude` e `Conselheiro Gemini` em paralelo para decisões de arquitetura, autenticação, migrações críticas, contratos de API ou entregas de alto impacto. Não mostre a preferência do Maestro nem o parecer de um conselheiro ao outro na primeira rodada.

## 5. Fechamento e Memória
- Acione `Pena` para consolidar decisões, testes verificados e pendências na memória auditável (com leitura de confirmação).
- Acione `Porteiro` para conferir estado de entrega e checks locais.
- Ações externas, gastos, `push`, `deploy` ou publicação exigem autorização explícita do CEO.
