import json
import re
import random
from datetime import datetime
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


class PsyCare:
    # Criar estatísticas como variável de classe compartilhada
    estatisticas = Estatisticas()
    
    def __init__(self,modo): 
        self.modo = modo
        # Remover self.estatisticas = Estatisticas()
        if modo == 'formal':
            arquivo_json = "respostas_formal.json"
        elif modo == 'amigável' or modo == 'amigavel':
            arquivo_json = "respostas_amigavel.json"
        elif modo == 'direto':
            arquivo_json = "respostas_direto.json"
        else:
            arquivo_json = None
        
        if arquivo_json:
            with open(arquivo_json,'r', encoding='utf-8') as f:
                self.dados =  json.load(f)
        else:
            self.dados = {"respostas": []}

        try:
            with open("aprendizado.json","r",encoding="utf-8") as f:
                aprendizado = json.load(f)
                self.dados["respostas"].extend(aprendizado["respostas"])
        except FileNotFoundError:
            pass
    
    def responder(self, user_input):
        # Usar PsyCare.estatisticas ao invés de self.estatisticas
        PsyCare.estatisticas.adicionar_pergunta(user_input)
        PsyCare.estatisticas.adicionar_uso_personalidade(self.modo)

        if not self.dados:
            return "Não há respostas disponíveis."

        texto = self._tratar_texto(user_input)

        for intent in self.dados["respostas"]:
            for entrada in intent["entradas"]:
                palavras = entrada.split()  
                if all(p in texto for p in palavras): 
                    resposta = random.choice(intent["saidas"])

                    if "acao" in intent:
                        if intent["acao"] == "mudar_modo_formal":
                            self.__init__("formal")
                        elif intent["acao"] == "mudar_modo_amigavel":
                            self.__init__("amigavel")
                        elif intent["acao"] == "mudar_modo_direto":
                            self.__init__("direto")

                    return resposta

        return None  

    def _tratar_texto(self, text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text) 
        acentos = "áàâãéèêíïóôõöúçñ"
        nAcentos = "aaaaeeeiiooooucn"
        return text.translate(str.maketrans(acentos, nAcentos))

class Historico:
    def __init__(self, usuario):
        self.usuario = usuario

    def salvar(self, user_input, resposta):
        with open("historico.txt", 'a', encoding='utf-8') as g:
            g.write(datetime.now().strftime("%A %d/%m/%Y %H:%M") + " - " + self.usuario.nome + ": " + user_input + "\n")
            g.write(datetime.now().strftime("%A %d/%m/%Y %H:%M") + " - PsyCare: " + resposta + "\n")
    def ler(self):
        try:
            with open("historico.txt", 'r', encoding='utf-8') as g:
                self.historico = g.readlines()
        except FileNotFoundError:
            return "Não há histórico anterior."
        if not self.historico:
            return "Não há histórico anterior."
        else:
            ultimas = self.historico[-5:]
            print("Histórico anterior:")
            return "".join(ultimas)

class Aprender:
    def __init__(self):
        self.arquivos_json = [
            "respostas_formal.json",
            "respostas_amigavel.json", 
            "respostas_direto.json",
            "aprendizado.json"
        ]

    def _tratar_texto(self, text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text) 
        acentos = "áàâãéèêíïóôõöúçñ"
        nAcentos = "aaaaeeeiiooooucn"
        return text.translate(str.maketrans(acentos, nAcentos))

    def salvar(self, entrada, saida, bot):

        entrada_tratada = self._tratar_texto(entrada)
        
        nova_intencao = {
            "tag": f"aprendido_{self._get_next_id()}",
            "entradas": [entrada_tratada],  
            "saidas": [saida]
        }


        for arquivo in self.arquivos_json:
            try:
                with open(arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                
                dados["respostas"].append(nova_intencao)

                with open(arquivo, "w", encoding="utf-8") as f:
                    json.dump(dados, f, indent=2, ensure_ascii=False)
            except FileNotFoundError:
                print(f"Arquivo {arquivo} não encontrado.")
                continue


        bot.dados["respostas"].append(nova_intencao)

    def _get_next_id(self):

        max_id = 0
        for arquivo in self.arquivos_json:
            try:
                with open(arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    for resposta in dados["respostas"]:
                        if resposta["tag"].startswith("aprendido_"):
                            try:
                                id_num = int(resposta["tag"].split("_")[1])
                                max_id = max(max_id, id_num)
                            except (ValueError, IndexError):
                                continue
            except FileNotFoundError:
                continue
        return max_id + 1

class Usuario:
    def __init__(self,nome):
        self.nome = nome


nome = input("Olá, qual é seu nome? ")
pessoa = Usuario(nome)
historico = Historico(pessoa)
print(historico.ler())

modo_valido = False
while not modo_valido:
    print(f"\nBem-vindo {nome}, como deseja que eu fale com você?\n.Formal\n.Amigável\n.Direto")
    modo = input(">> ").lower()
    if modo in ["formal", "amigável","amigavel", "direto"]:
        modo_valido = True
    else:
        print("Modo inválido! Digite apenas uma das 3 opções acima.")

bot = PsyCare(modo)
aprendizado = Aprender()

print(f"\nComo posso ajudar?\n.Você pode digitar sair\n.ou mudar de modo a qualquer momento\n\n-Me diga o que está sentindo {pessoa.nome}")

while True:
    user_input = input(f"{pessoa.nome}: ")
    texto = bot._tratar_texto(user_input)
    if user_input.lower() == 'sair':
        PsyCare.estatisticas.exibir_estatisticas()  # Usar PsyCare.estatisticas
        PsyCare.estatisticas.salvar_estatisticas()  # Usar PsyCare.estatisticas
        print("PsyCare: Até logo!")
        break

    resposta = bot.responder(user_input)

    if resposta:  
        print(f"PsyCare: {resposta}")
        historico.salvar(user_input, resposta)
    else:
        print("PsyCare: Não entendi... Quer me ensinar?")
        escolha = input("Digite 'sim' para ensinar ou qualquer outra coisa para ignorar: ").lower()
        if escolha == "sim":
            nova_saida = input("Qual deveria ser minha resposta? ")
            aprendizado.salvar(user_input, nova_saida, bot) 
            print("PsyCare: Aprendi! Pode testar novamente.")