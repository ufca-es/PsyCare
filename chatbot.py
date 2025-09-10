import json
import re
import random
from datetime import datetime

class PsyCare:
    def __init__(self,modo):
        self.modo = modo
        if modo == 'formal':
            print("Vou ser mais formal a partir de agora")
            arquivo_json = "respostas_formal.json"
        elif modo == 'amigável' or modo == 'amigavel':
            print("Vou ser mais amigável a partir de agora")
            arquivo_json = "respostas_amigavel.json"
        elif modo == 'direto':
            print("Vou ser mais direto a partir de agora")
            arquivo_json = "respostas_direto.json"
        else:
            arquivo_json = None
        
        if arquivo_json:
            with open(arquivo_json,'r', encoding='utf-8') as f:
                self.dados =  json.load(f)
        else:
            self.dados = {}
    
    def responder(self, user_input):
        if not self.dados:
            return "Não há respostas disponíveis."

        texto = self._tratar_texto(user_input)

        for intent in self.dados["respostas"]:
            for entrada in intent["entradas"]:
                palavras = entrada.split()  
                if all(p in texto for p in palavras):  
                    resposta = (intent["saidas"][0])

                    return resposta
                    self.I


        return "Desculpe, não entendi. Pode reformular?"

    def _tratar_texto(self, text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)  
        acentos = "áàâãéèêíïóôõöúçñ"
        nAcentos = "aaaaeeeiiooooucn"
        return text.translate(str.maketrans(acentos, nAcentos))



class Usuario:
    def __init__(self,nome):
        self.nome = nome

nome = input("Olá, qual é seu nome? ")
pessoa = Usuario(nome)
modo_valido = False
while not modo_valido:
    print(f"\nBem-vindo {nome}, como deseja que eu fale com você?\n.Formal\n.Amigável\n.Direto")
    modo = input(">> ").lower()
    if modo in ["formal", "amigável","amigavel", "direto"]:
        modo_valido = True
    else:
        print("Modo inválido! Digite apenas uma das 3 opções acima.")
bot = PsyCare(modo)
print(f"\nComo posso ajudar?\n.Você pode digitar sair\n.ou mudar de modo a qualquer momento\n\n-Me diga o que está sentindo {pessoa.nome}")
while True:
    user_input = input(f"{pessoa.nome}: ")
    texto = bot._tratar_texto(user_input)
    if user_input.lower() == 'sair':
        print("PsyCare: Até logo!")
        break
    resposta = bot.responder(user_input)
    print(f"PsyCare: {resposta}")


