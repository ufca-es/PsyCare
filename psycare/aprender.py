import re
import json 
from .constants import FORMAL_JSON, AMIGAVEL_JSON, DIRETO_JSON, APRENDIZADO_JSON

class Aprender:
    def __init__(self):
        self.arquivos_json = [
            FORMAL_JSON,
            AMIGAVEL_JSON,
            DIRETO_JSON,
            APRENDIZADO_JSON
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