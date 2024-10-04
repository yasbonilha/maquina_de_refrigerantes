import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Alfabeto
I = ['m25', 'm50', 'm100', 'b']

# Tabela de estados
T = {
    # Estado s0
    ('s0', 'b'): ('s0', 'n'), 
    ('s0', 'm25'): ('s1', 'n'),
    ('s0', 'm50'): ('s2', 'n'),
    ('s0', 'm100'): ('s4', 'n'),

    # Estado s1
    ('s1', 'b'): ('s1', 'n'),
    ('s1', 'm25'): ('s2', 'n'),
    ('s1', 'm50'): ('s3', 'n'),
    ('s1', 'm100'): ('s5', 'n'),

    # Estado s2
    ('s2', 'b'): ('s2', 'n'),
    ('s2', 'm25'): ('s3', 'n'),
    ('s2', 'm50'): ('s4', 'n'),
    ('s2', 'm100'): ('s6', 'n'),

    # Estado s3
    ('s3', 'b'): ('s3', 'n'),
    ('s3', 'm25'): ('s4', 'n'),
    ('s3', 'm50'): ('s5', 'n'),
    ('s3', 'm100'): ('s7', 'n'),

    # Estado s4
    ('s4', 'b'): ('s4', 'n'),
    ('s4', 'm25'): ('s5', 'n'),
    ('s4', 'm50'): ('s6', 'n'),
    ('s4', 'm100'): ('s8', 'n'),

    # Estado s5
    ('s5', 'b'): ('s5', 'n'),
    ('s5', 'm25'): ('s6', 'n'),
    ('s5', 'm50'): ('s7', 'n'),
    ('s5', 'm100'): ('s8', 't25'),  

    # Estado s6
    ('s6', 'b'): ('s6', 'n'),
    ('s6', 'm25'): ('s7', 'n'),
    ('s6', 'm50'): ('s8', 'n'),
    ('s6', 'm100'): ('s8', 't50'),  

    # Estado s7
    ('s7', 'b'): ('s7', 'n'),
    ('s7', 'm25'): ('s8', 'n'),
    ('s7', 'm50'): ('s8', 't25'),
    ('s7', 'm100'): ('s8', 't75'),

    # Estado s8
    ('s8', 'b'): ('s0', 'r'), 
    ('s8', 'm25'): ('s8', 't25'),
    ('s8', 'm50'): ('s8', 't50'),
    ('s8', 'm100'): ('s8', 't100')
}

formatacao_saida = {
    'n': '',
    'm25': 'R$0,25',
    'm50': 'R$0,50',
    'm100': 'R$1,00',
    'r': '',
    't25': 'R$0,25',
    't50': 'R$0,50',
    't75': 'R$0,75',
    't100': 'R$1,00'
}

formatacao_saldo = {
    's0': 'R$0,00',
    's1': 'R$0,25',
    's2': 'R$0,50',
    's3': 'R$0,75',
    's4': 'R$1,00',
    's5': 'R$1,25',
    's6': 'R$1,50',
    's7': 'R$1,75',
    's8': 'R$2,00'
}

def proximo_estado(estado, entrada):
    if entrada not in I:
        return ("Entrada inválida", None)
    return T.get((estado, entrada), ("Transição não definida", None))

class MaquinaDeVenda(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Máquina de Venda")
        self.geometry("1000x1000")

        imagem_fundo = Image.open("fundo_maquina.png") 
        imagem_fundo = imagem_fundo.resize((1000, 1000), Image.Resampling.LANCZOS) 
        self.imagem_fundo = ImageTk.PhotoImage(imagem_fundo)
        
        self.estado_atual = 's0'

        fundo_label = tk.Label(self, image=self.imagem_fundo)
        fundo_label.place(x=0, y=0, relwidth=1, relheight=1) 
        
        container_frame = tk.Frame(self, bg="#7d2423")
        container_frame.pack(side="right", padx=85, pady=85, anchor="e")

        self.label_estado = tk.Label(container_frame, text="Estado: s0", font=("Poppins", 18, "bold"), bg="#7d2423", fg="#f9e4d2")
        self.label_estado.pack(pady=10)

        self.label_saldo = tk.Label(container_frame, text="Saldo: ", font=("Poppins", 18, "bold"), bg="#7d2423", fg="#f9e4d2")
        self.label_saldo.pack(pady=10)

        self.label_saida = tk.Label(container_frame, text="Troco: ", font=("Poppins", 18, "bold"), bg="#7d2423", fg="#f9e4d2")
        self.label_saida.pack(pady=10)

        botao_frame = tk.Frame(container_frame, bg="#7d2423")
        botao_frame.pack(pady=20)

        self.moeda_25 = tk.Button(botao_frame, text="R$0,25", font=("Poppins", 12), width=30, height=2, bg="#f9e4d2", fg="#333", command=lambda: self.adicionar_moeda('m25'))
        self.moeda_25.grid(row=0, column=0, padx=10, pady=5)

        self.moeda_50 = tk.Button(botao_frame, text="R$0,50", font=("Poppins", 12), width=30, height=2, bg="#f9e4d2", fg="#333", command=lambda: self.adicionar_moeda('m50'))
        self.moeda_50.grid(row=1, column=0, padx=10, pady=5)

        self.moeda_100 = tk.Button(botao_frame, text="R$1,00", font=("Poppins", 12), width=30, height=2, bg="#f9e4d2", fg="#333", command=lambda: self.adicionar_moeda('m100'))
        self.moeda_100.grid(row=2, column=0, padx=10, pady=5)

        botao_refrigerante = tk.Button(container_frame, text="Comprar", font=("Poppins", 14, "bold"), width=10, height=1, bg="#101010", fg="#f9e4d2", command=lambda: self.adicionar_moeda('b'))
        botao_refrigerante.pack(pady=20)

    def atualizar_interface(self, saida):
        saida_formatada = formatacao_saida.get(saida, "Saída desconhecida")
        saldo_formatado = formatacao_saldo.get(self.estado_atual)
        self.label_estado.config(text=f"Estado: {self.estado_atual}")
        self.label_saldo.config(text=f"Saldo: {saldo_formatado}")
        self.label_saida.config(text=f"Troco: {saida_formatada}")
        print(f"Estado Atual: {self.estado_atual}, Troco: {saida_formatada}")

    def adicionar_moeda(self, entrada):
        print(f"Tentando adicionar moeda: {entrada}")
        self.estado_atual, saida = proximo_estado(self.estado_atual, entrada)
        print(f"Novo Estado: {self.estado_atual}, Saída: {saida}")
        self.atualizar_interface(saida)
        if saida == 'r':
            messagebox.showinfo("Info", "Seu produto foi lançado! Máquina reiniciada, pronta para nova operação.")
        elif saida == 'n' and entrada == 'b':
            messagebox.showinfo("Info", "Saldo insuficiente.")

if __name__ == "__main__":
    app = MaquinaDeVenda()
    app.mainloop()