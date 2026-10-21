# Lab: Cross-Site Scripting — TechNow — Instruções de Acesso

## Repositório

```
https://github.com/pj0natha/lab-xss-technow
```

## Contexto

A TechNow é um portal de notícias de tecnologia fictício. Você foi contratado(a) para um teste de intrusão na aplicação web. O escopo é a aplicação completa disponível em `http://localhost:8082` — nenhuma área está fora de escopo.

> ⚠️ **Este laboratório é a prova avaliatória.** Ele não é só um exercício de treino — o que você produz aqui vale nota. O entregável não é a flag em si, é um **relatório de pentest**. A especificação completa e obrigatória do relatório está em [`Requisitos-Relatorio-Prova.md`](Requisitos-Relatorio-Prova.md) — leia esse documento **antes** de começar a explorar, porque ele define que evidências você precisa capturar durante o processo (prints, comandos, etc.), não só ao final.

## Objetivo

A aplicação tem **6 pontos de Cross-Site Scripting**: 3 refletidos (o payload vem da própria requisição e é devolvido na resposta, sem persistir) e 3 armazenados (o payload é salvo pela aplicação e passa a ser exibido para qualquer visitante). Não há lista de onde cada um está — parte do trabalho é reconhecimento: navegar pela aplicação e identificar, por conta própria, quais entradas são refletidas sem tratamento.

Cada ponto, quando explorado com sucesso, entrega uma flag no formato `flag{...}`. As flags **não aparecem em texto visível na página nem no código-fonte HTML** — elas só são acessíveis via JavaScript (por exemplo, lendo `document.cookie` a partir do script injetado). Ou seja: a prova de exploração aqui é a execução real do seu script na página, não só encontrar onde o campo é refletido.

**Requisito mínimo da prova:** identificar e explorar com sucesso **pelo menos 1 vulnerabilidade refletida e 1 armazenada**, com documentação completa de cada uma (reconhecimento, identificação, PoC, resultado, recomendação de correção e referência — ver `Requisitos-Relatorio-Prova.md`). Explorar mais de 2 é permitido e pode enriquecer seu relatório, mas o mínimo para a nota máxima já é essas 2, uma de cada categoria.

Todas as rotas envolvidas são alcançáveis pela navegação normal do site — não é necessário fuzzing aqui. O trabalho é entender o contexto de saída de cada campo (HTML, atributo, etc.) e montar o payload adequado.

## Pré-requisitos

- Docker e Docker Compose instalados
- Navegador com DevTools (para inspecionar cookies e console)
- Opcional: Burp Suite ou extensão de interceptação para montar os payloads

## Como subir o ambiente

```bash
git clone https://github.com/pj0natha/lab-xss-technow.git
cd lab-xss-technow
docker compose up --build
```

A aplicação estará disponível em:

```
http://localhost:8082
```

Para derrubar o ambiente ao final:

```bash
docker compose down
```

> **Atenção:** as flags são geradas automaticamente quando o container sobe, e são únicas para a sua execução — elas não são as mesmas que aparecem em capturas de tela ou anotações de outros colegas. Evite derrubar o container no meio do exercício: reiniciar gera flags novas.

## Roteiro sugerido

1. **Reconhecimento manual** — navegue por toda a aplicação, mapeando todas as páginas, formulários e parâmetros que aceitam entrada do usuário.
2. **Identificação** — para cada ponto, teste como a entrada é refletida de volta: em qual contexto HTML ela cai (texto, atributo, etc.) e se há algum tipo de filtro.
3. **Exploração** — monte um payload que execute JavaScript no contexto da página e leia o cookie correspondente àquele ponto para obter a flag.

Os 6 cenários são independentes entre si; não é necessário resolvê-los em ordem.

## O entregável

Não existe entrega de código, script ou flag "solta" — a prova é corrigida pelo **relatório de pentest** que você produzir, em `.pdf`.

Enquanto explora cada técnica, já vá capturando o que o relatório vai exigir (ver [`Requisitos-Relatorio-Prova.md`](Requisitos-Relatorio-Prova.md) para a estrutura completa e os critérios de nota):

- Como você encontrou o ponto de injeção
- O teste que confirmou a suspeita de vulnerabilidade
- O payload final usado, com print da requisição/resposta e do script sendo executado
- A flag obtida
- Como a vulnerabilidade deveria ser corrigida
- Uma referência externa sobre a técnica (OWASP, CWE, PortSwigger, etc.)

Capturar essas evidências **durante** a exploração é muito mais fácil do que tentar reconstruir tudo depois — o container é derrubado ao final e cada execução gera flags novas, então não há como "voltar" para pegar um print que faltou.

Bom hunting!
