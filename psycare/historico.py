from datetime import datetime

class Historico:
    def __init__(self, usuario): 
        self.usuario = usuario

    def salvar(self, user_input, resposta):
        timestamp = datetime.now().strftime("%A %d/%m/%Y %H:%M")
        with open(r"data\historico.txt", 'a', encoding='utf-8') as g:
            g.write(f"{timestamp} - {self.usuario.nome}: {user_input}\n")
            g.write(f"{timestamp} - PsyCare: {resposta}\n")

    def ler(self, last_n=5):
        """
        Retorna uma string com as últimas `last_n` interações (pergunta + resposta).
        Cada interação é o par de linhas gravadas por `salvar`.
        Retorna None se não houver arquivo.
        """
        try:
            with open(r"data\historico.txt", "r", encoding="utf-8") as f:
                lines = [l.rstrip("\n") for l in f if l.strip()]
        except FileNotFoundError:
            return None

        interactions = []
        i = 0
        while i < len(lines):
            if i + 1 < len(lines):
                interactions.append(lines[i] + "\n" + lines[i + 1])
                i += 2
            else:
                interactions.append(lines[i])
                i += 1

        if not interactions:
            return None

        last = interactions[-last_n:]
        return "\n\n".join(last)