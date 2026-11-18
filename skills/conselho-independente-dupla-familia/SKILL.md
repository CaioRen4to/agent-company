---
name: conselho-independente-dupla-familia
description: Protocolo de parecer técnico independente inspirado no Conselho dos Anciões, com avaliação cega entre famílias de modelos (Claude e Gemini), classificação de convergências/exclusividades e veredito estruturado.
---

# conselho-independente-dupla-familia

Inspirado em `gabrielcoutinhoDL/claude-skill-conselho-dos-ancioes` (licença MIT) e redesenhado para execução nativa com agentes permanentes de famílias distintas (`Conselheiro Claude` e `Conselheiro Gemini`) e governança SQL *Fail-Closed* (`v_validacao_conselho`).

## 1. Regras para o Conselheiro (Claude / Gemini)
- Avalie **exclusivamente** o pacote recebido (**pedido original do CEO + `diff` real ou artefatos integrais**, restrições e evidências — nunca apenas um resumo opinativo).
- Primeira rodada cega: não consulte o outro conselheiro nem altere arquivos do projeto.
- Estruture a resposta obrigatoriamente em:
  1. **Veredito:** `APROVA`, `APROVA COM RESSALVAS`, `REPROVA` ou `INCONCLUSIVO`.
  2. **Achados principais:** problema, gravidade (`CRÍTICO`, `ALTO`, `MÉDIO`, `BAIXO`), evidência no material e correção sugerida.
  3. **Riscos e incertezas:** o que não pôde ser comprovado pelo pacote enviado.
  4. **Condições para aprovação:** critérios objetivos para sanar bloqueios.

## 2. Regras de síntese para o Maestro (Foco em Divergências)
- **Divergência e Exclusividade primeiro:** destaque ao CEO onde as duas famílias discordaram ou o que **apenas uma família enxergou** (para expor pontos cegos sem repetir texto redundante).
- **Convergência:** pontos que ambos os conselheiros apontaram de forma independente.
- **Complemento exclusivo:** pontos levantados por apenas um modelo (listar separadamente identificando a origem: Claude ou Gemini; exclusividade não é automaticamente conflito).
- **Conflito real:** quando um aprova e outro reprova a mesma decisão ou propõem caminhos incompatíveis.
- **Conselho incompleto (Fail-Closed):** validado também pela view SQL `v_validacao_conselho` — se menos de 2 famílias distintas responderem na rodada, declarar `CONSELHO INCOMPLETO` (nunca presumir aprovação unânime).
- **Limites:** concordância dos dois modelos não substitui testes reais nem autoriza gasto, publicação ou ação irreversível sem o CEO.
