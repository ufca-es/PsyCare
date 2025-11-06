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
        self.modo = None
        self.dados = None
        self._set_modo(modo)

    def _normalize_modo(self, modo):
        if not isinstance(modo, str):
            return None
        p = modo.lower().strip()
        p = p.replace('á','a').replace('à','a').replace('ã','a').replace('â','a')
        p = p.replace('é','e').replace('è','e').replace('ê','e')
        p = p.replace('í','i').replace('ï','i')
        p = p.replace('ó','o').replace('ô','o').replace('õ','o').replace('ö','o')
        p = p.replace('ú','u').replace('ç','c').replace('ñ','n')
        if p.startswith('form'):
            return 'formal'
        if p.startswith('amig'):
            return 'amigavel'
        if p.startswith('dir'):
            return 'direto'
        return None

    def _set_modo(self, modo):
        """Define o modo do bot e recarrega o arquivo json correspondente."""
        chave = self._normalize_modo(modo)
        if chave is None:
            return False
        self.modo = chave
        arquivo = {
            'formal': FORMAL_JSON,
            'amigavel': AMIGAVEL_JSON,
            'direto': DIRETO_JSON
        }.get(chave)
        try:
            if arquivo:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    self.dados = json.load(f)
            else:
                self.dados = None
        except FileNotFoundError:
            self.dados = None
        return True

    def _tratar_texto(self, text):
        """Normaliza: remove acentos, pontuação, passa para minúsculas e limpa espaços."""
        if not isinstance(text, str):
            return ""
        text = unicodedata.normalize('NFKD', text)
        text = text.encode('ASCII', 'ignore').decode('utf-8', 'ignore')
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
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

        seq_ratio = SequenceMatcher(None, t1, t2).ratio()

        tokens1 = t1.split()
        tokens2 = t2.split()
        jacc = self._jaccard(tokens1, tokens2)

        combined = 0.55 * seq_ratio + 0.45 * jacc
        return combined

    def responder(self, user_input):
        """Processa entrada do usuário e escolhe a melhor resposta.
           Se a entrada for um comando para mudar o modo, faz a troca e retorna confirmação.
        """
        texto_raw = user_input if isinstance(user_input, str) else ""
        texto = self._tratar_texto(texto_raw)

        target = None
        m = re.search(r'(?:mudar\s+para|trocar\s+para|mudar\s+modo\s+para|modo:|modo\s+para)\s*(formal|amigavel|amigavel|amig|amigavel|amigável|direto)\b', texto)
        if not m:
            m2 = re.search(r'\bmodo\b.*\b(formal|amigavel|amigavel|amig|amigavel|amigável|direto)\b', texto)
            if m2:
                m = m2
        if not m:
            if texto.strip() in ('formal','amigavel','amigavel','amigavel','amigável','direto','amig'):
                target = texto.strip()
        if m and not target:
            target = m.group(1)

        if target:
            if self._set_modo(target):
                return f"Modo alterado para {self.modo.capitalize()}."
            else:
                return "Modo inválido. Use: formal, amigavel ou direto."

        PsyCare.estatisticas.adicionar_pergunta(user_input)
        PsyCare.estatisticas.adicionar_uso_personalidade(self.modo)

        if not self.dados or "respostas" not in self.dados:
            return None

        texto_usuario = texto
        if not texto_usuario:
            return None

        melhor_resposta = None
        melhor_score = 0.45 

        for intent in self.dados.get("respostas", []):
            entradas = intent.get("entradas", [])
            saidas = intent.get("saidas", [])
            for entrada in entradas:
                entrada_tratada = self._tratar_texto(entrada)
                if texto_usuario == entrada_tratada:
                    return random.choice(saidas) if saidas else None
                score = self._calcular_similaridade(texto_usuario, entrada_tratada)
                if score > melhor_score and score > melhor_score - 0.0001:
                    melhor_score = score
                    melhor_resposta = saidas

        if melhor_resposta:
            return random.choice(melhor_resposta) if melhor_resposta else None

        return None