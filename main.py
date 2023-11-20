import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from fpdf import FPDF
from funcoes import Candidato
from funcoes import GerenciadorCurriculos
from funcoes import InterfaceGrafica

if __name__ == "__main__":
    root = tk.Tk()
    gerenciador = GerenciadorCurriculos()
    app = InterfaceGrafica(root, gerenciador)
    root.mainloop()