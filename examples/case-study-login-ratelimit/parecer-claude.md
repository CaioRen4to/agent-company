# Parecer Independente — Família Claude (1ª Rodada Cega)

**Missão:** `PILOTO-CASE-LOGIN-001` | **Veredito:** `REPROVA`

## Achados Convergentes (Confirmados na Síntese)
1. **Escopo do contador indefinido:** não especifica se o limite é por conta, por IP ou combinado (só por IP permite *password spraying*; só por conta facilita bloqueio malicioso de terceiros).
2. **Janela temporal ausente:** não define em quanto tempo as 10 tentativas são contabilizadas nem quando o contador zera.
3. **Ação ao atingir o limite indefinida:** não informa se ocorre bloqueio temporário, permanente ou atraso, nem a duração.
4. **Sem controles compensatórios:** dobrar tentativas sem *backoff* progressivo ou CAPTCHA amplia a superfície de força bruta.
5. **Ausência de monitoramento:** faltam logs estruturados e alertas para picos de falhas de autenticação.

## Apontamentos Exclusivos desta Família
- Ausência de verificação contra senhas comprometidas (*Have I Been Pwned / HIBP*).
- Falta de limite mais restrito e MFA obrigatório para contas administrativas.
- Ausência de critérios de aceite e casos de teste automatizados para o bloqueio e desbloqueio.
