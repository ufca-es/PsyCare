import json
from collections import Counter

class Estatisticas:
    def __init__(self):
        self.total_interacoes = 0
        self.perguntas = Counter()  # contador total
        self.perguntas_sessao = Counter()  # novo contador para sessão atual
        self.uso_personalidades = {
            'formal': 0,
            'amigavel': 0,
            'direto': 0
        }
        self.carregar_estatisticas()

    def adicionar_pergunta(self, pergunta):
        self.perguntas[pergunta] += 1
        self.perguntas_sessao[pergunta] += 1  # incrementa contador da sessão
        self.total_interacoes += 1

    def adicionar_uso_personalidade(self, personalidade):
        self.uso_personalidades[personalidade] += 1

    def top3_perguntas(self):
        if not self.perguntas:
            return "Sem perguntas registradas ainda."
        
        top3 = self.perguntas.most_common(3)
        saida = "Top 3 perguntas mais frequentes:\n"
        for i, (pergunta, _) in enumerate(top3, 1):  
            saida += f"{i}. {pergunta}\n"
        return saida.strip()

    def salvar_estatisticas(self):
        dados = {
            'total_interacoes': self.total_interacoes,
            'perguntas': dict(self.perguntas),
            'uso_personalidades': self.uso_personalidades
        }
        with open('estatisticas.txt', 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

    def salvar_relatorio(self):
        pergunta, freq = self.obter_pergunta_mais_frequente()
        with open('relatorio.txt', 'w', encoding='utf-8') as g:
            g.write(f'RELATÓRIO DO CHATBOT PSYCARE:\n\n1. INTERAÇÕES:\n    - A conversa com o chatbot obteve um total de {self.total_interacoes} interações entre o usuário e o chatbot.')
            if self.perguntas:
                g.write(f'\n    - A mensagem mais frequente inserida pelo usuário: "{pergunta}", aparecendo {freq} vezes na conversa.\n')
            g.write('\n2. QUANTIDADE DE MENSAGENS POR PERSONALIDADES:')
            for modo, quantidade in self.uso_personalidades.items():
                g.write(f"\n    - Modo {modo.capitalize()}: {quantidade}")

    def carregar_estatisticas(self):
        try:
            with open('estatisticas.txt', 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.total_interacoes = dados['total_interacoes']
                self.perguntas = Counter(dados['perguntas'])
                self.uso_personalidades = dados['uso_personalidades']
        except:
            pass
            
    def obter_pergunta_mais_frequente(self):
        if not self.perguntas:
            return "Nenhuma pergunta registrada"
        return self.perguntas.most_common(1)[0]
        

    def exibir_estatisticas(self):
        print("\n=== Estatísticas da Sessão Atual ===")
        print(f"Total de interações: {self.total_interacoes}")
        
        if self.perguntas_sessao:  # usar perguntas_sessao ao invés de perguntas
            pergunta_frequente = self.perguntas_sessao.most_common(1)[0]
            print(f"Pergunta mais frequente desta sessão: '{pergunta_frequente[0]}' ({pergunta_frequente[1]} vezes)")
        
        print("\nUso de personalidades:")
        for modo, quantidade in self.uso_personalidades.items():
            print(f"- {modo.capitalize()}: {quantidade}")
        print("==================")