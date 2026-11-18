# Parecer Independente — Família Gemini (1ª Rodada Cega)

**Missão:** `PILOTO-CASE-LOGIN-001` | **Veredito:** `REPROVA`

## Achados Convergentes (Confirmados na Síntese)
1. **Escopo do contador indefinido:** sem distinção entre chave por IP, por conta ou par `(IP, conta)`.
2. **Janela temporal ausente:** sem janela deslizante ou fixa definida para expiração das tentativas.
3. **Ação ao atingir o limite indefinida:** falta definição de duração e política de bloqueio.
4. **Sem controles compensatórios:** aumento de tentativas sem *backoff* exponencial ou desafio antibot.
5. **Ausência de monitoramento:** sem telemetria nem alerta de anomalia em falhas consecutivas.

## Apontamentos Exclusivos desta Família
- Destacou o vetor de **negação de serviço direcionada (*Account Lockout DoS*)**: se o contador for apenas por conta sem recuperação segura, qualquer atacante pode travar o acesso de usuários legítimos de propósito.
- Recomendou fluxo de desbloqueio autônomo via e-mail verificado ou desafio MFA como mitigação direta.
