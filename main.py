from psycare.psycare import PsyCare
from psycare.usuario import Usuario
from psycare.historico import Historico
from psycare.aprender import Aprender

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
print(PsyCare.estatisticas.top3_perguntas())

while True:
    user_input = input(f"{pessoa.nome}: ")
    texto = bot._tratar_texto(user_input)
    if user_input.lower() == 'sair':

        bot.estatisticas.exibir_estatisticas()
        bot.estatisticas.salvar_estatisticas()
        bot.estatisticas.salvar_relatorio()

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