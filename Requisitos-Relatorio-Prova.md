# Prova — Relatório de Pentest (XSS) — TechNow

## O que é entregue

Um **relatório de teste de intrusão**, no formato **`.pdf`**, documentando a exploração de vulnerabilidades de Cross-Site Scripting encontradas na aplicação TechNow (`Lab-XSS-TechNow`).

Não é entregue código, script de automação nem a flag "solta" — o que vale nota é o **relatório**, como se fosse o entregável de um engajamento real de pentest para um cliente.

## Requisito mínimo

Documentar, **de forma completa**, pelo menos **2 vulnerabilidades de XSS exploradas com sucesso, sendo 1 refletida e 1 armazenada**, entre as 6 existentes no lab (3 refletidas e 3 armazenadas). Não há lista de onde cada uma está — encontrá-las faz parte da avaliação, assim como no reconhecimento de qualquer engajamento real.

Documentar mais de 2 é permitido e bem-vindo, mas não aumenta a nota além do máximo (10) — o foco é a **qualidade e completude** de cada uma, não a quantidade.

## Estrutura obrigatória do relatório

### 1. Identificação

- Nome do aluno
- Data da execução
- Alvo testado: `TechNow` (`http://localhost:8082`, ambiente local via Docker)

### 2. Metodologia (breve)

Um parágrafo descrevendo a abordagem geral: reconhecimento manual da aplicação, identificação do contexto de reflexão de cada entrada, e exploração manual dos pontos encontrados. Ferramentas utilizadas (ex: navegador, DevTools, Burp Suite).

### 3. Um bloco por vulnerabilidade documentada

Repita esta estrutura para **cada** vulnerabilidade (mínimo 2 blocos, 1 refletida e 1 armazenada):

#### 3.X. [Refletido ou Armazenado] — [rota/campo afetado]

**a) Reconhecimento**
Como você chegou até esse ponto: qual página, formulário ou parâmetro, e como ele devolve a entrada na resposta.

**b) Identificação da vulnerabilidade**
O que indicou que o campo era injetável (ex: a entrada aparece sem nenhuma codificação no HTML da resposta). Print do teste inicial que confirmou a suspeita (ex: injetar uma tag inofensiva e ver que ela não foi escapada).

**c) Exploração / Prova de Conceito (PoC)**
- O payload final utilizado, formatado como código.
- Print de tela mostrando o payload sendo enviado (requisição/formulário) e o script sendo executado na página (ex: console do navegador, ou o valor do cookie lido).
- Se for armazenada, mostre que o payload persiste e executa novamente em uma nova visita à página (sem reenviar o formulário).

**d) Resultado obtido**
A flag extraída, em destaque, e o print de onde/como ela foi obtida (ex: valor do cookie exibido no console após a execução do script injetado).

**e) Recomendação de correção**
Como a vulnerabilidade deveria ser corrigida (ex: encoding de saída no contexto correto, Content Security Policy, sanitização de entrada, atributo `HttpOnly` em cookies sensíveis). Específico para o ponto em questão, não uma resposta genérica de "usar boas práticas".

**f) Referência**
Ao menos uma referência externa relevante para a técnica (ex: OWASP XSS, um CWE, PortSwigger Web Security Academy). Link ou citação.

### 4. Conclusão (opcional)

Um parágrafo curto resumindo o risco geral encontrado e a criticidade das vulnerabilidades exploradas.

## Regras sobre as evidências

- As capturas de tela devem ser **suas**, da sua própria execução do laboratório (`docker compose up --build`) — a flag capturada é única da sua execução, então cole ela como saiu, não copie de colegas.
- Prints devem ser legíveis e mostrar o necessário (payload + execução + flag), sem cortar informação relevante.
- Payloads devem estar em texto (não só na imagem), para facilitar a leitura e a correção.

## Como você será avaliado

A nota (0 a 10) é a soma de 5 critérios — **reconhecimento, identificação/exploração, PoC documentada, recomendação de correção e referência** — aplicados a cada vulnerabilidade que você documentar, até o teto de 10 pontos. Ou seja, 1 vulnerabilidade refletida + 1 armazenada, ambas completas (5 critérios cada), já garantem a nota máxima.
