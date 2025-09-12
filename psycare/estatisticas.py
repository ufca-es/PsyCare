import json
from collections import Counter

class Estatisticas:
    def __init__(self):
        self.total_interacoes = 0
        self.perguntas = Counter()
        self.uso_personalidades = {
            'formal': 0,
            'amigavel': 0,
            'direto': 0
        }
        self.carregar_estatisticas()
    
    def adicionar_pergunta(self, pergunta):
        self.perguntas[pergunta] += 1
        self.total_interacoes += 1
        
    def adicionar_uso_personalidade(self, personalidade):
        self.uso_personalidades[personalidade] += 1
        
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
        except FileNotFoundError:
            pass
            
    def obter_pergunta_mais_frequente(self):
        if not self.perguntas:
            return "Nenhuma pergunta registrada"
        return self.perguntas.most_common(1)[0]
        
    def exibir_estatisticas(self):
        print("\n=== Estatísticas ===")
        print(f"Total de interações: {self.total_interacoes}")
        if self.perguntas:
            pergunta, freq = self.obter_pergunta_mais_frequente()
            print(f"Pergunta mais frequente: '{pergunta}' ({freq} vezes)")
        print("\nUso de personalidades:")
        for modo, quantidade in self.uso_personalidades.items():
            print(f"- {modo.capitalize()}: {quantidade}")
        print("==================")