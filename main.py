import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox, simpledialog
from psycare.psycare import PsyCare
from psycare.usuario import Usuario
from psycare.historico import Historico
from psycare.aprender import Aprender

root = tk.Tk()
root.title("PsyCare Chatbot")
root.geometry("600x600")

# --- Área superior: nome e modo ---
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

# Nome
tk.Label(frame_top, text="Digite seu nome:").grid(row=0, column=0, padx=5, sticky="w")
nome_var = tk.StringVar()
entrada_nome = tk.Entry(frame_top, textvariable=nome_var)
entrada_nome.grid(row=0, column=1, padx=5)

# Seleção de modo
tk.Label(frame_top, text="Modo de conversa:").grid(row=1, column=0, padx=5, sticky="w")
modo_var = tk.StringVar()
modo_select = ttk.Combobox(frame_top, textvariable=modo_var, state="readonly")
modo_select["values"] = ("Formal", "Amigavel", "Direto")
modo_select.grid(row=1, column=1, padx=5)

# --- Estatísticas (top 3 perguntas históricas) ---
frame_stats = tk.Frame(root)
frame_stats.pack(padx=10, pady=5, fill=tk.X)

tk.Label(frame_stats, text="Top 3 perguntas (histórico):").pack(anchor="w")
list_top3 = tk.Listbox(frame_stats, height=3)
list_top3.pack(fill=tk.X)

def atualizar_top3():
    """Atualiza a lista com as 3 perguntas mais frequentes de todos os runs (persistidas)."""
    list_top3.delete(0, tk.END)
    # usa as estatísticas globais carregadas em PsyCare.estatisticas
    try:
        counter = PsyCare.estatisticas.perguntas
    except Exception:
        counter = None
    if not counter:
        list_top3.insert(tk.END, "Nenhuma pergunta registrada")
        return
    top3 = counter.most_common(3)
    if not top3:
        list_top3.insert(tk.END, "Nenhuma pergunta registrada")
        return
    for i, (pergunta, freq) in enumerate(top3, 1):
        display = f"{i}. {pergunta} ({freq})"
        list_top3.insert(tk.END, display)

# --- Área de conversa ---
caixa_conversa = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
caixa_conversa.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# --- Área de entrada de mensagem ---
entrada_texto = tk.Entry(root, state="disabled")  # desabilitado até iniciar
entrada_texto.pack(padx=10, pady=5, fill=tk.X)

# --- Inicialização ---
pessoa = None
historico = None
bot = None
aprendizado = Aprender()

# Atualizar chat
def atualizar_chat(mensagem):
    caixa_conversa.config(state='normal')
    caixa_conversa.insert(tk.END, mensagem + "\n")
    caixa_conversa.config(state='disabled')
    caixa_conversa.yview(tk.END)

# Iniciar chat (só quando nome e modo estiverem preenchidos)
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
    
    # Cria usuário, histórico e bot
    pessoa = Usuario(nome)
    historico = Historico(pessoa)
    bot = PsyCare(modo)
    bot.estatisticas.adicionar_uso_personalidade(modo)
    
    # Atualiza display das top3 (histórico)
    atualizar_top3()
    
    # Libera entrada de texto
    entrada_texto.config(state="normal")
    botao_enviar.config(state="normal")
    botao_iniciar.config(state="disabled")
    
    # 🔒 Travar o campo do nome (só digita uma vez)
    entrada_nome.config(state="disabled")
    
    # Se quiser travar o modo também, basta descomentar a linha abaixo:
    # modo_select.config(state="disabled")
    
    # Mostra histórico (se existir)
    historico_texto = historico.ler()
    if historico_texto:
        atualizar_chat(historico_texto)
    
    atualizar_chat(f"PsyCare: Olá {pessoa.nome}, modo {modo.capitalize()} ativado. Como posso ajudar?")

# Enviar mensagem
def enviar():
    user_input = entrada_texto.get().strip()
    if not user_input:
        return
    entrada_texto.delete(0, tk.END)
    
    if user_input.lower() == "sair":
        bot.estatisticas.exibir_estatisticas()
        bot.estatisticas.salvar_estatisticas()
        bot.estatisticas.salvar_relatorio()
        atualizar_chat("PsyCare: Até logo!")
        root.quit()
        return
    
    atualizar_chat(f"{pessoa.nome}: {user_input}")
    bot.estatisticas.adicionar_pergunta(user_input)
    
    # atualizar o painel de top3 após registrar a pergunta
    atualizar_top3()
    
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

# --- Botões ---
frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=5)

botao_iniciar = tk.Button(frame_botoes, text="Iniciar Chat", command=iniciar_chat)
botao_iniciar.pack(side=tk.LEFT, padx=5)

botao_enviar = tk.Button(frame_botoes, text="Enviar", command=enviar, state="disabled")
botao_enviar.pack(side=tk.LEFT, padx=5)

# Enter envia mensagem
entrada_texto.bind("<Return>", lambda event: enviar())

root.mainloop()
