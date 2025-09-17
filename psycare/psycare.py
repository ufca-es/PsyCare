import json
import re
import random
import unicodedata
from difflib import SequenceMatcher
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
            arquivo_json = None

        try:
            if arquivo_json:
                with open(arquivo_json, 'r', encoding='utf-8') as f:
                    self.dados = json.load(f)
            else:
                self.dados = None
        except FileNotFoundError:
            self.dados = None

    def _tratar_texto(self, text):
        """Normaliza: remove acentos, pontuação, passa para minúsculas e limpa espaços."""
        if not isinstance(text, str):
            return ""
        # remover acentos
        text = unicodedata.normalize('NFKD', text)
        text = text.encode('ASCII', 'ignore').decode('utf-8', 'ignore')
        text = text.lower()
        # remover pontuação (mantém letras e números e espaços)
        text = re.sub(r'[^\w\s]', ' ', text)
        # reduzir múltiplos espaços
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _tokenize(self, text):
        t = self._tratar_texto(text)
        if not t:
            return []
        return t.split()

    def _jaccard(self, s1_tokens, s2_tokens):
        a = set(s1_tokens)
        b = set(s2_tokens)
        if not a and not b:
            return 0.0
        inter = a.intersection(b)
        union = a.union(b)
        return len(inter) / len(union) if union else 0.0

    def _calcular_similaridade(self, texto1, texto2):
        """
        Combina SequenceMatcher (ordem/estrutura) com Jaccard (sobreposição de tokens)
        para medir similaridade entre frases.
        Retorna valor entre 0 e 1.
        """
        t1 = self._tratar_texto(texto1)
        t2 = self._tratar_texto(texto2)
        if not t1 or not t2:
            return 0.0

        # similaridade estrutural (ordem e caracteres)
        seq_ratio = SequenceMatcher(None, t1, t2).ratio()

        # similaridade por tokens (palavras)
        tokens1 = t1.split()
        tokens2 = t2.split()
        jacc = self._jaccard(tokens1, tokens2)

        # combinar: dar peso ligeiramente maior à estrutura, mas considerar sobreposição de palavras
        combined = 0.55 * seq_ratio + 0.45 * jacc
        return combined

    def responder(self, user_input):
        """Processa entrada do usuário e escolhe a melhor resposta baseada em similaridade de frases."""
        # atualizar estatísticas
        PsyCare.estatisticas.adicionar_pergunta(user_input)
        PsyCare.estatisticas.adicionar_uso_personalidade(self.modo)

        if not self.dados or "respostas" not in self.dados:
            return None

        texto_usuario = self._tratar_texto(user_input)
        if not texto_usuario:
            return None

        melhor_resposta = None
        melhor_score = 0.45  # limiar inicial; ajuste conforme necessário

        for intent in self.dados.get("respostas", []):
            entradas = intent.get("entradas", [])
            saidas = intent.get("saidas", [])
            for entrada in entradas:
                entrada_tratada = self._tratar_texto(entrada)
                # correspondência exata (após normalização) tem prioridade máxima
                if texto_usuario == entrada_tratada:
                    return random.choice(saidas) if saidas else None
                score = self._calcular_similaridade(texto_usuario, entrada_tratada)
                if score > melhor_score and score > melhor_score - 0.0001:  # estabilidade
                    melhor_score = score
                    melhor_resposta = saidas

        if melhor_resposta:
            return random.choice(melhor_resposta) if melhor_resposta else None

        return None