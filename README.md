# 🧠 Psycare

Um chatbot simples desenvolvido em Python, o qual visa informar, acolher e ajudar o usuário com sua saúde mental.

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

## 🛠️ Funcionalidades

O projeto é composto por um chat onde o usuário pode digitar o que deseja conversar com o bot, onde a resposta dependerá da escolha do usuário a partir de três personalidades diferentes, que poderá ser definida na execução do bot e alterado no meio da conversa. 
O bot também possui a função de histórico, que mostrará as cinco últimas interações no chat, assim como, as funcionalidades de um relatório escrito e estatíscicas que poderão ser acessados pelo usuário após a finalização da sessão e que trará dados sobre a sessão mais recente e sobre os aspectos geral das interações que houver no chat.

### Personalidades
>  - **Formal:** Utilizando uma linguagem culta e objetiva, destacando todos as informações e pontos de atenção;
>  - **Amigável:** Linguagem mais acolhedora, trazendo uma abordagem mais leve para o usuário;
>  - **Direto:** Linguagem com respostas mais curtas e diretas, focando nas informações principais.

### Histórico
>  - O chatbot possui uma função voltada ao salvamento e mostra do histórico referente à sessões anteriores e que será exibido ao usuário a partir da próxima execução do código, visando trazer ao usuário a facilidade de poder compartilhar sua experiência com o projeto.

### Perguntas frequentes
>  - O chatbot também analisará suas interações com o usuário e armazenará os inputs mais frequentemente usados para fim de facilitar e ajudar a guiar as interações futuras com o usuário.

### Relatório e estatísticas
>  - Tanto por sessão quanto no uso geral do bot, serão fornecidas ao final da execução relatórios e estatísticas que mostrarão ao usuário o número de usos de cada personalidade, assim como o número de interações no total com o bot, o número de mudança de personalidades e as perguntas mais frequentes da sessão.

## 👤 Membros

- Icaro;
- Heberthy;
- José Welton;
- Joaquim Arthur.

### Professor:

- Williamson Silva.
