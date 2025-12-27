import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox, simpledialog, Toplevel
import tkinter.font as tkfont
import datetime
import random

from psycare.psycare import PsyCare
from psycare.usuario import Usuario
from psycare.historico import Historico
from psycare.aprender import Aprender
from psycare.estatisticas import Estatisticas

Estatisticas.data_dir("") 


root = tk.Tk()
root.title("PsyCare")
root.geometry("900x640")
root.minsize(780, 520)
root.configure(bg="#f4f7fb")

style = ttk.Style(root)
style.theme_use('clam')
PRIMARY = "#2b6cb0"
ACCENT = "#2dd4bf"
BG = "#f4f7fb"
CARD = "#ffffff"
TEXT = "#243444"
MUTED = "#6b7280"
BTN = "#1f6aa5"

font_header = tkfont.Font(family="Segoe UI", size=16, weight="bold")
font_sub = tkfont.Font(family="Segoe UI", size=10)
font_chat = tkfont.Font(family="Segoe UI", size=11)

sidebar_w = 280
frame_sidebar = tk.Frame(root, bg=BG, width=sidebar_w)
frame_sidebar.pack(side=tk.LEFT, fill=tk.Y)
frame_main = tk.Frame(root, bg=BG)
frame_main.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

card = tk.Frame(frame_sidebar, bg=CARD, bd=0, relief=tk.FLAT)
card.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.94)

lbl_title = tk.Label(card, text="PsyCare", bg=CARD, fg=PRIMARY, font=font_header)
lbl_title.pack(anchor="nw", padx=16, pady=(14, 4))

lbl_sub = tk.Label(card, text="Acolhendo e informando.", bg=CARD, fg=MUTED, font=font_sub)
lbl_sub.pack(anchor="nw", padx=16)

frm_inputs = tk.Frame(card, bg=CARD)
frm_inputs.pack(fill=tk.X, padx=12, pady=12)

tk.Label(frm_inputs, text="Nome", bg=CARD, fg=TEXT, font=font_sub).grid(row=0, column=0, sticky="w")
nome_var = tk.StringVar()
entrada_nome = ttk.Entry(frm_inputs, textvariable=nome_var, width=24)
entrada_nome.grid(row=1, column=0, sticky="w", pady=(4,8))

tk.Label(frm_inputs, text="Modo", bg=CARD, fg=TEXT, font=font_sub).grid(row=2, column=0, sticky="w")
modo_var = tk.StringVar()
modo_select = ttk.Combobox(frm_inputs, textvariable=modo_var, state="readonly", width=22)
modo_select["values"] = ("Formal", "Amigavel", "Direto")
modo_select.grid(row=3, column=0, sticky="w", pady=(4,8))

frm_buttons = tk.Frame(card, bg=CARD)
frm_buttons.pack(fill=tk.X, padx=12, pady=(0,12))

botao_iniciar = tk.Button(frm_buttons, text="Iniciar Chat", bg=BTN, fg="white", relief=tk.FLAT, command=lambda: iniciar_chat(), padx=8, pady=6)
botao_iniciar.pack(fill=tk.X, pady=(0,8))

botao_historico = tk.Button(frm_buttons, text="Últimas 5 Interações", bg="#eef3fb", fg=PRIMARY, relief=tk.FLAT, command=lambda: mostrar_ultimas_interacoes())
botao_historico.pack(fill=tk.X, pady=(0,8))

botao_sair = tk.Button(frm_buttons, text="Sair", bg="#ffe9e9", fg="#b02a2a", relief=tk.FLAT, command=lambda: sair())
botao_sair.pack(fill=tk.X)

frm_top3 = tk.Frame(card, bg=CARD)
frm_top3.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

tk.Label(frm_top3, text="Perguntas frequentes:", bg=CARD, fg=TEXT, font=font_sub).pack(anchor="w")
list_top3 = tk.Listbox(frm_top3, height=3, bg="#fbfdff", bd=0, highlightthickness=0, fg=TEXT)
list_top3.pack(fill=tk.X, pady=(6,0))

def atualizar_top3():
    list_top3.delete(0, tk.END)
    try:
        counter = PsyCare.estatisticas.perguntas
    except Exception:
        counter = None
    if not counter or not getattr(counter, "most_common", None):
        list_top3.insert(tk.END, "Nenhuma pergunta registrada")
        return
    top3 = counter.most_common(3)
    if not top3:
        list_top3.insert(tk.END, "Nenhuma pergunta registrada")
        return
    for i, (pergunta, freq) in enumerate(top3, 1):
        display = f"{i}. {pergunta} ({freq})"
        list_top3.insert(tk.END, display)

chat_card = tk.Frame(frame_main, bg=CARD)
chat_card.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.94)

hdr = tk.Frame(chat_card, bg=CARD)
hdr.pack(fill=tk.X, pady=(10,6), padx=12)
lbl_chat_title = tk.Label(hdr, text="Conversa", bg=CARD, fg=TEXT, font=font_header)
lbl_chat_title.pack(side=tk.LEFT)
lbl_clock = tk.Label(hdr, text="", bg=CARD, fg=MUTED, font=font_sub)
lbl_clock.pack(side=tk.RIGHT)

def tick_clock():
    lbl_clock.config(text=datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))
    lbl_clock.after(10000, tick_clock)
tick_clock()

caixa_conversa = scrolledtext.ScrolledText(chat_card, wrap=tk.WORD, state='disabled', bg="#fbfdff", fg=TEXT, font=font_chat, bd=0)
caixa_conversa.pack(padx=12, pady=(0,8), fill=tk.BOTH, expand=True)

caixa_conversa.tag_configure("user", foreground="#0b5fa5", justify="right")
caixa_conversa.tag_configure("bot", foreground="#136f63", justify="left")
caixa_conversa.tag_configure("meta", foreground=MUTED, font=font_sub)

frm_entry = tk.Frame(chat_card, bg=CARD)
frm_entry.pack(fill=tk.X, padx=12, pady=8)

entrada_texto = ttk.Entry(frm_entry, state="disabled")
entrada_texto.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,8))

botao_enviar = tk.Button(frm_entry, text="Enviar", bg=PRIMARY, fg="white", relief=tk.FLAT, state="disabled")
botao_enviar.pack(side=tk.RIGHT)

pessoa = None
historico = None
bot = None
aprendizado = Aprender()

def atualizar_chat(mensagem, autor="meta"):
    caixa_conversa.config(state='normal')
    if autor == "user":
        caixa_conversa.insert(tk.END, f"{mensagem}\n", "user")
    elif autor == "bot":
        caixa_conversa.insert(tk.END, f"{mensagem}\n", "bot")
    else:
        caixa_conversa.insert(tk.END, f"{mensagem}\n", "meta")
    caixa_conversa.config(state='disabled')
    caixa_conversa.yview(tk.END)

def iniciar_chat():
    global pessoa, historico, bot
    nome = nome_var.get().strip()
    modo = modo_var.get().lower().strip()

    if not nome:
        messagebox.showwarning("Aviso", "Digite seu nome antes de continuar!")
        return
    if not modo:
        messagebox.showwarning("Aviso", "Selecione um modo antes de continuar!")
        return

    pessoa = Usuario(nome)
    historico = Historico(pessoa)
    bot = PsyCare(modo)

    entrada_texto.config(state="normal")
    botao_enviar.config(state="normal")
    botao_iniciar.config(state="disabled")
    entrada_nome.config(state="disabled")
    modo_select.config(state="disabled")

    atualizar_top3()
    atualizar_chat(f"Olá {pessoa.nome}, modo {modo.capitalize()} ativado. Como posso ajudar?", "meta")

def enviar(event=None):
    global bot
    if not bot:
        messagebox.showinfo("Aviso", "Inicie o chat primeiro.")
        return
    user_input = entrada_texto.get().strip()
    if not user_input:
        return
    entrada_texto.delete(0, tk.END)
    if user_input.lower() == "sair":
        sair()
        return

    atualizar_chat(f"{pessoa.nome}: {user_input}", "user")
    resposta = bot.responder(user_input)

    atualizar_top3()

    if resposta:
        atualizar_chat(f"PsyCare: {resposta}", "bot")
        try:
            historico.salvar(user_input, resposta)
        except Exception:
            pass
    else:
        atualizar_chat("PsyCare: Não entendi... Quer me ensinar?", "bot")
        escolha = simpledialog.askstring("Aprender", "Digite 'sim' para ensinar ou qualquer outra coisa para ignorar:")
        if escolha and escolha.lower() == "sim":
            nova_saida = simpledialog.askstring("Aprender", "Qual deveria ser minha resposta?")
            if nova_saida:
                aprendizado.salvar(user_input, nova_saida, bot)
                atualizar_chat("PsyCare: Aprendi! Pode testar novamente.", "bot")
    return

botao_enviar.config(command=enviar)
entrada_texto.bind("<Return>", lambda e: enviar())

def mostrar_ultimas_interacoes():
    if not historico:
        messagebox.showinfo("Histórico", "Nenhuma sessão iniciada ainda.")
        return
    ultimas = historico.ler(last_n=5)
    if not ultimas:
        ultimas = "Nenhuma interação encontrada."
    janela = Toplevel(root)
    janela.title("Últimas 5 interações")
    janela.geometry("560x340")
    txt = scrolledtext.ScrolledText(janela, wrap=tk.WORD)
    txt.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
    txt.insert(tk.END, ultimas)
    txt.config(state="disabled")

def mostrar_relatorio(auto=False):
    if not bot:
        return
    if auto:
        root.withdraw()
    janela = Toplevel(root)
    janela.title("Relatório do PsyCare")
    janela.geometry("560x420")
    try:
        with open(r"data\relatorio.txt", "r", encoding="utf-8") as f:
            conteudo = f.read()
    except FileNotFoundError:
        conteudo = "Nenhum relatório encontrado. Interaja com o chatbot primeiro."

    try:
        if bot.estatisticas.perguntas_sessao:
            pergunta_frequente, freq = bot.estatisticas.perguntas_sessao.most_common(1)[0]
            import re
            conteudo = re.sub(
                r'(mensagem mais frequente inserida pelo usuário: ).*',
                f'\\1\"{pergunta_frequente}\", aparecendo {freq} vezes na conversa.',
                conteudo
            )
    except Exception:
        pass

    texto = scrolledtext.ScrolledText(janela, wrap=tk.WORD)
    texto.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    estatisticas_texto = bot.estatisticas.exibir_estatisticas(retornar_texto=True)
    texto.insert(tk.END, estatisticas_texto + "\n\n" + conteudo)
    texto.config(state="disabled")
    janela.protocol("WM_DELETE_WINDOW", lambda: root.destroy())

def sair():
    if bot:
        try:
            bot.estatisticas.salvar_estatisticas()
            bot.estatisticas.salvar_relatorio()
        except Exception:
            pass
        atualizar_chat("PsyCare: Até logo!", "meta")
        mostrar_relatorio(auto=True)
    else:
        root.quit()

entrada_nome.focus_set()
atualizar_chat("PsyCare pronto. Digite seu nome e escolha o modo para começar.", "meta")
atualizar_top3()

root.mainloop()
