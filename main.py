import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox, simpledialog, Toplevel
from psycare.psycare import PsyCare
from psycare.usuario import Usuario
from psycare.historico import Historico
from psycare.aprender import Aprender

root = tk.Tk()
root.title("PsyCare Chatbot")
root.geometry("600x600")

# Frames principais
frame_top = tk.Frame(root)  # vai para o topo depois do início
frame_middle = tk.Frame(root)  # aparece no meio antes de iniciar
frame_middle.pack(pady=50)

# Entrada de nome + modo (início)
tk.Label(frame_middle, text="Digite seu nome:").grid(row=0, column=0, padx=5, sticky="e")
nome_var = tk.StringVar()
entrada_nome = tk.Entry(frame_middle, textvariable=nome_var)
entrada_nome.grid(row=0, column=1, padx=5)

tk.Label(frame_middle, text="Modo de conversa:").grid(row=0, column=2, padx=5, sticky="e")
modo_var = tk.StringVar()
modo_select = ttk.Combobox(frame_middle, textvariable=modo_var, state="readonly")
modo_select["values"] = ("Formal", "Amigavel", "Direto")
modo_select.grid(row=0, column=3, padx=5)

# Área de conversa
caixa_conversa = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
caixa_conversa.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entrada_texto = tk.Entry(root, state="disabled")
entrada_texto.pack(padx=10, pady=5, fill=tk.X)

# Variáveis globais
pessoa = None
historico = None
bot = None
aprendizado = Aprender()

# Funções
def atualizar_chat(mensagem):
    caixa_conversa.config(state='normal')
    caixa_conversa.insert(tk.END, mensagem + "\n")
    caixa_conversa.config(state='disabled')
    caixa_conversa.yview(tk.END)

def iniciar_chat():
    global pessoa, historico, bot

    nome = nome_var.get().strip()
    modo = modo_var.get().lower()

    if not nome:
        messagebox.showwarning("Aviso", "Digite seu nome antes de continuar!")
        return
    if not modo:
        messagebox.showwarning("Aviso", "Selecione um modo antes de continuar!")
        return

    pessoa = Usuario(nome)
    historico = Historico(pessoa)
    bot = PsyCare(modo)
    bot.estatisticas.adicionar_uso_personalidade(modo)

    entrada_texto.config(state="normal")
    botao_enviar.config(state="normal")
    botao_iniciar.config(state="disabled")
    entrada_nome.config(state="disabled")
    modo_select.config(state="disabled")

    # Mover frame_middle para o topo (frame_top)
    frame_middle.pack_forget()
    frame_top.pack(pady=5, fill=tk.X)

    # Mostrar Top 3 perguntas
    atualizar_chat("=== Top 3 Perguntas ===")
    atualizar_chat(bot.estatisticas.top3_perguntas())

    atualizar_chat(f"PsyCare: Olá {pessoa.nome}, modo {modo.capitalize()} ativado. Como posso ajudar?")

def enviar():
    user_input = entrada_texto.get().strip()
    if not user_input:
        return
    entrada_texto.delete(0, tk.END)

    if user_input.lower() == "sair":
        bot.estatisticas.salvar_estatisticas()
        bot.estatisticas.salvar_relatorio()
        atualizar_chat("PsyCare: Até logo!")
        mostrar_relatorio(auto=True)  # mostra relatório e fecha a janela principal
        return



    atualizar_chat(f"{pessoa.nome}: {user_input}")
    bot.estatisticas.adicionar_pergunta(user_input)

    resposta = bot.responder(user_input)

    if resposta:
        atualizar_chat(f"PsyCare: {resposta}")
        historico.salvar(user_input, resposta)
    else:
        atualizar_chat("PsyCare: Não entendi... Quer me ensinar?")
        escolha = simpledialog.askstring("Aprender", "Digite 'sim' para ensinar ou qualquer outra coisa para ignorar:")
        if escolha and escolha.lower() == "sim":
            nova_saida = simpledialog.askstring("Aprender", "Qual deveria ser minha resposta?")
            if nova_saida:
                aprendizado.salvar(user_input, nova_saida, bot)
                atualizar_chat("PsyCare: Aprendi! Pode testar novamente.")

def mostrar_ultimas_interacoes():
    try:
        with open("historico.txt", "r", encoding="utf-8") as f:
            linhas = f.readlines()
            ultimas = linhas[-5:] if len(linhas) >= 5 else linhas
    except FileNotFoundError:
        ultimas = ["Nenhum histórico encontrado."]

    # Criar janela para exibir
    janela = Toplevel(root)
    janela.title("Últimas 5 interações")
    janela.geometry("500x300")

    texto = scrolledtext.ScrolledText(janela, wrap=tk.WORD, state="normal")
    texto.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    texto.insert(tk.END, "".join(ultimas))
    texto.config(state="disabled")

def mostrar_relatorio(auto=False):
    if not bot:
        return

    # Se for auto (ao digitar sair), esconde a janela principal
    if auto:
        root.withdraw()

    # Criar janela do relatório
    janela = Toplevel(root)
    janela.title("Relatório do PsyCare")
    janela.geometry("500x400")

    # Ler conteúdo antigo do relatorio.txt
    try:
        with open("relatorio.txt", "r", encoding="utf-8") as f:
            conteudo = f.read()
    except FileNotFoundError:
        conteudo = "Nenhum relatório encontrado. Interaja com o chatbot primeiro."

    # Substituir a pergunta mais frequente pelo da sessão atual
    if bot.estatisticas.perguntas_sessao:
        pergunta_frequente, freq = bot.estatisticas.perguntas_sessao.most_common(1)[0]
        import re
        conteudo = re.sub(
            r'(mensagem mais frequente inserida pelo usuário: ).*',
            f'\\1"{pergunta_frequente}", aparecendo {freq} vezes na conversa.',
            conteudo
        )

    # Área de texto para exibir o relatório
    texto = scrolledtext.ScrolledText(janela, wrap=tk.WORD, state="normal")
    texto.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    # Adicionar estatísticas da sessão atual
    estatisticas_texto = bot.estatisticas.exibir_estatisticas(retornar_texto=True)
    texto.insert(tk.END, estatisticas_texto + "\n" + conteudo)
    texto.config(state="disabled")

# Botões principais
# ----------------------
frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=5)

botao_iniciar = tk.Button(frame_botoes, text="Iniciar Chat", command=iniciar_chat)
botao_iniciar.pack(side=tk.LEFT, padx=5)

botao_enviar = tk.Button(frame_botoes, text="Enviar", command=enviar, state="disabled",)
botao_enviar.pack(side=tk.LEFT, padx=5)
entrada_texto.bind("<Return>", lambda event: enviar())

botao_historico = tk.Button(frame_botoes, text="Histórico", command=mostrar_ultimas_interacoes, state="normal")
botao_historico.pack(side=tk.LEFT, padx=5)

root.mainloop()
