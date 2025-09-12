import json
import random
import re
from .estatisticas import Estatisticas
from .constants import FORMAL_JSON, AMIGAVEL_JSON, DIRETO_JSON, APRENDIZADO_JSON

class PsyCare:
    estatisticas = Estatisticas()
    
    def __init__(self, modo):
        self.modo = modo
        
        if modo == 'formal':
            arquivo_json = FORMAL_JSON
        elif modo == 'amigável' or modo == 'amigavel':
            arquivo_json = AMIGAVEL_JSON
        elif modo == 'direto':
            arquivo_json = DIRETO_JSON
        else:
            arquivo_json = FORMAL_JSON
        
        if arquivo_json:
            with open(arquivo_json,'r', encoding='utf-8') as f:
                self.dados =  json.load(f)
        else:
            self.dados = {"respostas": []}

        try:
            with open(APRENDIZADO_JSON, "r", encoding="utf-8") as f:
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