# 🧠 PsyCare

> Um chatbot simples desenvolvido em Python, o qual visa informar, acolher e ajudar o usuário com sua saúde mental.

## 📕 Sobre

- O PsyCare é um projeto da disciplina de Introdução a Programação da Universidade Federal do Cariri (UFCA), a qual é ministrada pelos professores Jayr Pereira e Williamson Silva. O objetivo do projeto é desenvolver um ChatBot usando a linguagem de programação Python (A qual foi usada durante toda disciplina), integrando conceitos fundamentais de programação, listas, funções, dicionários, manipulação de arquivos e organização modular com uso de classes. O domínio escolhido pela equipe foi o da Saúde, mais especificamente da Saúde Mental. Portanto o PsyCare visa ter um primeiro contato com o usuário, podendo acolher em momentos de crise (os quais podem acontecer a qualquer hora do dia), informar sobre exercicios para se acalmar e manter uma boa saúde mental, recomendar o melhor profissional para tratar da situação e fazer relatórios para ajudar os profissionais a tratar o paciente.

## 🎯 Objetivos de aprendizagem
- Consolidar o uso de listas, dicionários, estruturas condicionais e de repetição.
- Praticar a modularização de códigos com uso de funções e classes.
- Aprender a separar lógica de negócio da interface com o usuário.
- Ler e gravar dados em arquivos textos.
- Utilizar Git e GitHub para documentação e controle de versão do projeto.
- Desenvolver habilidades de projeto em equipe e resolução de problemas reais.

## 📋 Pré-requisitos

- Python 3

## 🚀 Como executar

1. Clone o repositório;

2. Execute o chatbot:
```bash
python main.py
```

## 📦 Estrutura do projeto

```
PsyCare/
├── main.py                      # Arquivo principal do chatbot
|
├── data
|   ├── estatisticas.txt         # Arquivo txt das estatísticas
|   ├── historico.txt            # Arquivo txt do histórico
|   └── relatorio.txt            # Arquivo txt do relatório
|
├── config
|   ├── respostas_formal.json    # Arquivo json da personalidade formal
|   ├── respostas_direto.json    # Arquivo json da personalidade direto
|   ├── respostas_amigavel.json  # Arquivo json da personalidade amigável
|   └── aprendizado.json         # Arquivo json de aprendizado
|
├── psycare
|   ├── __init__.py              # Arquivo que transforma a pasta em um pacote
|   ├── constants.py             # Arquivo que contém os caminhos dos outros arquivos
|   ├── aprender.py              # Classe utilizada para o aprendizado do bot
|   ├── estatisticas.py          # Classe utilizada para as estatísticas do bot
|   ├── usuario.py               # Classe utilizada para o usuário do bot
|   └── historico.py             # Classe utilizada para o histórico do bot
|
└── README.md                    # Este arquivo
```

## 🛠️ Uso e funcionalidades

O projeto é composto por um chat onde o usuário pode digitar o que deseja conversar com o bot, onde a resposta dependerá da escolha do usuário a partir de três personalidades diferentes, que poderá ser definida na execução do bot e alterado no meio da conversa. Quando o ChatBot recebe as mensagens do usuário, ele retorna uma resposta a partir da palavra-chave que está na mensagem enviada. Tanto as palavras-chave, quanto as respostas estão dentro dos .json dentro da página config. A interface foi feita com a biblioteca nativa do Python Tkinter.
O bot também possui a função de histórico, que mostrará as cinco últimas interações no chat, assim como, as funcionalidades de um relatório escrito e estatíscicas que poderão ser acessados pelo usuário após a finalização da sessão e que trará dados sobre a sessão mais recente e sobre os aspectos geral das interações que houver no chat.

### 🎭 Personalidades
>  - **Formal:** Utilizando uma linguagem culta e objetiva, destacando todos as informações e pontos de atenção;
>  - **Amigável:** Linguagem mais acolhedora, trazendo uma abordagem mais leve para o usuário;
>  - **Direto:** Linguagem com respostas mais curtas e diretas, focando nas informações principais.

### 📜 Histórico
> O chatbot possui uma função voltada ao salvamento e mostra do histórico referente à sessões anteriores e que será exibido ao usuário a partir da próxima execução do código, visando trazer ao usuário a facilidade de poder compartilhar sua experiência com o projeto.

### 🤔 Perguntas frequentes
> O chatbot também analisará suas interações com o usuário e armazenará os inputs mais frequentemente usados para fim de facilitar e ajudar a guiar as interações futuras com o usuário.

### 📉 Relatório e estatísticas
> Tanto por sessão quanto no uso geral do bot, serão fornecidas ao final da execução relatórios e estatísticas que mostrarão ao usuário o número de usos de cada personalidade, assim como o número de interações no total com o bot, o número de mudança de personalidades e as perguntas mais frequentes da sessão.

## 👤 Membros

### Contribuidores 🧑‍🎓:

- Icaro Cavalcante;
- Heberthy Samir;
- José Welton;
- Joaquim Arthur.

### Professor Orientador 👨‍🏫:

- Williamson Silva.
