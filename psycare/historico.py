from datetime import datetime

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