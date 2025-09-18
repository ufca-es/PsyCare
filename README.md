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

## 🛠️ Personalidades

- **Formal:** Utilizando uma linguagem culta e objetiva, destacando todos as informações e pontos de atenção;
- **Amigável:** Linguagem mais acolhedora, trazendo uma abordagem mais leve para o usuário;
- **Direto:** Linguagem com respostas mais curtas e diretas, focando nas informações principais.

## 👤 Membros

- Icaro;
- Heberthy;
- José Welton;
- Joaquim Arthur.

### Professor:

- Williamson Silva.
