---
name: memoria-auditavel-obsidian-pena
description: Procedimento para registrar decisões, arquitetura, resultados de testes e pendências no cofre Obsidian com leitura prévia, atualização incremental e confirmação pós-escrita.
---

# memoria-auditavel-obsidian-pena

Consolida o protocolo do agente `Pena` e do `doc-updater` para atualização segura do Segundo Cérebro em cofres Markdown/Obsidian (via MCP Obsidian ou acesso direto a arquivos).

## 1. Regras invioláveis
- **Nunca registrar segredos:** jamais inclua chaves de API, tokens JWT, senhas ou variáveis sensíveis do `.env`.
- **Leitura antes da escrita:** sempre leia a nota existente antes de editar ou criar, preservando o conteúdo anterior.
- **Apenas fatos verificados:** diferencie claramente o que foi implantado/testado do que ainda é plano ou pendência.

## 2. Estrutura padrão por projeto/agente
Em `05-Agentes-e-Memorias/` e `01-Projetos/`:
- `00-INDICE.md`: visão geral e links para documentos ativos.
- `01-CONTEXTO.md`: estado atual do projeto.
- `02-ARQUITETURA.md`: desenho técnico e componentes.
- `03-DECISOES.md`: registro de decisões (contexto, decisão, motivo e data).
- `04-PENDENCIAS.md`: próximos passos e bloqueios conhecidos.
- `05-TESTES.md`: evidências de validação e resultados.

## 3. Verificação pós-escrita (Read-back)
Após criar ou editar uma nota no Obsidian, leia o arquivo novamente para confirmar que a gravação foi concluída sem truncamento e devolva ao Maestro o caminho exato e o resumo do registro.
