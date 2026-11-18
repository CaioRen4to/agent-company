---
name: padroes-de-engenharia-ecc
description: Procedimentos de implementação, resolução de erros de build, refatoração limpa, otimização de desempenho, acessibilidade web e automação idempotente para Arquiteto, Pixel, Bento, Atlas e Fluxo.
---

# padroes-de-engenharia-ecc

Consolida as práticas operacionais dos papéis de engenharia (`planner`, `architect`, `pixel`, `a11y-architect`, `react-build-resolver`, `bento`, `build-error-resolver`, `refactor-cleaner`, `performance-optimizer`, `atlas` e `fluxo`).

## 1. Isolamento de escopo por camada
- **Arquiteto:** entrega plano verificável, arquivos afetados, riscos, dependências e critérios de aceite antes da codificação pesada.
- **Pixel (Frontend):** altera apenas UI/componentes/estilos; garante navegação por teclado, contraste, estados de erro/loading e build limpo do frontend.
- **Bento (Backend):** altera apenas rotas, serviços e regras de negócio; garante validação de payload, autenticação, logs claros e resolução de erros de build/importação.
- **Atlas (Dados):** altera apenas schemas, migrações, queries e índices; toda mudança estrutural exige integridade referencial (`FOREIGN KEY`, `CHECK`), índices e instrução de reversão (rollback).
- **Fluxo (Automação):** desenha workflows e webhooks com chave de idempotência (evitar disparo duplicado), timeout, retry com backoff e registro de falha.

## 2. Higiene de código e entrega
- Corrija a causa raiz de erros de build ou tipagem; nunca silencie warnings críticos com `@ts-ignore` ou `noqa` sem justificativa técnica documentada.
- Remova código morto, imports não utilizados e logs temporários antes de devolver a tarefa ao Maestro.
- No relatório de retorno ao Maestro, informe: arquivos alterados, comandos de verificação executados, resultado obtido e qualquer limitação residual.
