import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import messagebox
from datetime import datetime
from main import gerar_agenda
import os

# Carrega variáveis de ambiente (se quiser)
from dotenv import load_dotenv
load_dotenv()
URL = os.getenv("URL")
URL_AGENDA = os.getenv("URL_AGENDA")


def iniciar_gui():
    app = ctk.CTk()
    app.title("Coleta de Agenda")
    app.geometry("480x350")
    app.resizable(False, False)

    # Usuário e senha
    ctk.CTkLabel(app, text="Usuário (E-mail):").pack(pady=(20, 0))
    entry_usuario = ctk.CTkEntry(app, width=200)
    entry_usuario.pack()

    ctk.CTkLabel(app, text="Senha:").pack(pady=(10, 0))
    entry_senha = ctk.CTkEntry(app, width=200, show="*")
    entry_senha.pack()

    # Datas
    ctk.CTkLabel(app, text="Data de Início:").pack(pady=(20, 0))
    cal_inicio = DateEntry(app, width=16, background='darkblue',
                           foreground='white', borderwidth=2, date_pattern='dd/MM/yyyy')
    cal_inicio.pack()

    ctk.CTkLabel(app, text="Data Final:").pack(pady=(20, 0))
    cal_fim = DateEntry(app, width=16, background='darkblue',
                        foreground='white', borderwidth=2, date_pattern='dd/MM/yyyy')
    cal_fim.pack()

    # Função do botão
    def acao_gerar():
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        data_inicio = cal_inicio.get_date()
        data_fim = cal_fim.get_date()

        if data_inicio > data_fim:
            messagebox.showerror(
                "Erro", "Data inicial não pode ser maior que a final.")
            return
        try:
            arquivo = gerar_agenda(
                usuario, senha, data_inicio, data_fim, URL, URL_AGENDA)
            messagebox.showinfo("Sucesso", f"Arquivo gerado: {arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar arquivo:\n{str(e)}")

    btn_gerar = ctk.CTkButton(app, text="Gerar Arquivo", command=acao_gerar)
    btn_gerar.pack(pady=(20, 0))

    app.mainloop()


if __name__ == "__main__":
    iniciar_gui()
