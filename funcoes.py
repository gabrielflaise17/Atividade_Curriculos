import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from fpdf import FPDF

class Candidato:
    def __init__(self, nome, telefone, minibio, entrevista, teste_teorico, teste_pratico, soft_skills):
        self.nome = nome
        self.telefone = telefone
        self.minibio = minibio
        self.entrevista = entrevista
        self.teste_teorico = teste_teorico
        self.teste_pratico = teste_pratico
        self.soft_skills = soft_skills

class GerenciadorCurriculos:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
        )
        self.cursor = self.conexao.cursor()

        self.cursor.execute("CREATE DATABASE IF NOT EXISTS curriculos")
        self.conexao.commit()

        # Agora, conecte ao banco de dados 'curriculos'
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="curriculos"
        )
        self.cursor = self.conexao.cursor()

        # Crie a tabela se não existir
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidatos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255),
                telefone VARCHAR(20),
                minibio TEXT,
                entrevista FLOAT,
                teste_teorico FLOAT,
                teste_pratico FLOAT,
                soft_skills FLOAT
            )
        """)
        self.conexao.commit()
        self.inserir_dados()

    def inserir_dados(self):
        query = "TRUNCATE TABLE candidatos"
        self.cursor.execute(query)
        self.conexao.commit()

        query = """
        INSERT INTO candidatos (id, nome, telefone, minibio, entrevista, teste_teorico, teste_pratico, soft_skills)
        VALUES
        (1, 'Carlos Silva', '15981001090', 'Olá, busco oportunidades na área de Desenvolvimento Web', 8, 7, 9, 8),
        (2, 'Fernanda Oliveira', '15999999999', 'Olá, tenho interesse em atuar na área de Marketing Digital', 7, 8, 8, 7),
        (3, 'André Santos', '15999999999', 'Oi, gostaria de contribuir na área de Engenharia Civil', 9, 8, 9, 8),
        (4, 'Juliana Lima', '15999999999', 'Oi, sou apaixonada por Design Gráfico e procuro oportunidades nessa área', 8, 9, 7, 8),
        (5, 'Ricardo Almeida', '15999999999', 'Olá, quero me dedicar à área de Agricultura Sustentável', 9, 6, 8, 7),
        (6, 'Patricia Costa', '15999999999', 'Oi, busco oportunidades em Desenvolvimento Web e Design UI/UX', 7, 9, 8, 9),
        (7, 'Roberto Oliveira', '15999999999', 'Oi, tenho paixão pela área de Saúde e procuro oportunidades na Enfermagem', 8, 7, 9, 8),
        (8, 'Camila Santos', '15999999999', 'Olá, busco oportunidades na área de Educação e Pedagogia', 9, 8, 7, 9),
        (9, 'Vinícius Pereira', '15999999999', 'Oi, interessado em oportunidades na área de Logística e Supply Chain', 7, 9, 8, 9),
        (10, 'Luciana Mendes', '15999999999', 'Oi, tenho interesse em atuar na área esportiva como treinadora', 8, 8, 9, 7),
        (11, 'José Silva', '15999999999', 'Olá, busco oportunidades em Desenvolvimento Web e Engenharia de Software', 9, 9, 8, 7),
        (12, 'Raquel Oliveira', '15999999999', 'Oi, tenho interesse em trabalhar com entregas e logística', 7, 8, 8, 9),
        (13, 'Gabriela Fernandes', '15999999999', 'Olá, busco oportunidades na área de Compras e Suprimentos', 8, 7, 6, 7),
        (14, 'Márcio Alves', '15999999999', 'Olá, tenho interesse em atuar na área de Mecânica Automotiva', 6, 8, 7, 6),
        (15, 'Aline Costa', '15999999999', 'Olá, tenho paixão por esportes e procuro oportunidades nessa área', 9, 7, 8, 7),
        (16, 'Natália Pereira', '15999999999', 'Oi, busco oportunidades na área educacional e de Pedagogia', 8, 8, 9, 8),
        (17, 'Guilherme Santos', '15999999999', 'Oi, tenho interesse em atuar na área Administrativa e Financeira', 7, 9, 8, 6),
        (18, 'Renata Hessel', '15999999999', 'Oi, interessada em oportunidades na área Administrativa', 7, 7, 8, 8),
        (19, 'Thiago Antunes', '15999999999', 'Olá, busco oportunidades em Desenvolvimento Web e Engenharia de Software', 9, 8, 7, 8),
        (20, 'Helena Camargo', '15999999999', 'Olá, tenho interesse em atuar na área de Vendas e Atendimento ao Cliente', 8, 7, 6, 8);
        """
        self.cursor.execute(query)
        self.conexao.commit()

    def cadastrar_candidato(self, candidato):
        sql = """
            INSERT INTO candidatos 
            (nome, telefone, minibio, entrevista, teste_teorico, teste_pratico, soft_skills) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        valores = (candidato.nome, candidato.telefone, candidato.minibio,
                   candidato.entrevista, candidato.teste_teorico, candidato.teste_pratico, candidato.soft_skills)
        self.cursor.execute(sql, valores)
        self.conexao.commit()

    def buscar_candidatos_compativeis(self, requisitos):
        sql = """
            SELECT nome, entrevista, teste_teorico, teste_pratico, soft_skills 
            FROM candidatos 
            WHERE entrevista >= %s AND teste_teorico >= %s AND teste_pratico >= %s AND soft_skills >= %s
        """
        valores = (requisitos['entrevista'], requisitos['teste_teorico'], requisitos['teste_pratico'], requisitos['soft_skills'])
        self.cursor.execute(sql, valores)
        return self.cursor.fetchall()

    def gerar_relatorio_completo(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        self.cursor.execute("SELECT * FROM candidatos")
        candidatos = self.cursor.fetchall()

        for candidato in candidatos:
            pdf.cell(200, 10, txt=f"Nome: {candidato[1]}", ln=True)
            pdf.cell(200, 10, txt=f"Telefone: {candidato[2]}", ln=True)
            pdf.cell(200, 10, txt=f"Minibio: {candidato[3]}", ln=True)
            pdf.cell(200, 10, txt=f"Entrevista: {candidato[4]}", ln=True)
            pdf.cell(200, 10, txt=f"Teste Teórico: {candidato[5]}", ln=True)
            pdf.cell(200, 10, txt=f"Teste Prático: {candidato[6]}", ln=True)
            pdf.cell(200, 10, txt=f"Avaliação de Soft Skills: {candidato[7]}", ln=True)
            pdf.ln(10)

        pdf.output("relatorio_completo.pdf")

    def gerar_relatorio_resumido(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        self.cursor.execute("SELECT nome, entrevista, teste_teorico, teste_pratico, soft_skills FROM candidatos")
        candidatos = self.cursor.fetchall()

        for candidato in candidatos:
            pdf.cell(200, 10, txt=f"Nome: {candidato[0]}", ln=True)
            pdf.cell(200, 10, txt=f"Entrevista: {candidato[1]}", ln=True)
            pdf.cell(200, 10, txt=f"Teste Teórico: {candidato[2]}", ln=True)
            pdf.cell(200, 10, txt=f"Teste Prático: {candidato[3]}", ln=True)
            pdf.cell(200, 10, txt=f"Avaliação de Soft Skills: {candidato[4]}", ln=True)
            pdf.ln(10)

        pdf.output("relatorio_resumido.pdf")


class InterfaceGrafica:
    def __init__(self, root, gerenciador):
        self.root = root
        self.gerenciador = gerenciador

        self.root.title("Gerenciamento de Currículos")

        self.label_nome = ttk.Label(root, text="Nome:")
        self.entry_nome = ttk.Entry(root)

        self.label_telefone = ttk.Label(root, text="Telefone:")
        self.entry_telefone = ttk.Entry(root)

        self.label_minibio = ttk.Label(root, text="Minibio:")
        self.entry_minibio = tk.Text(root, width=30, height=5)

        self.label_entrevista = ttk.Label(root, text="Entrevista:")
        self.entry_entrevista = ttk.Entry(root)

        self.label_teste_teorico = ttk.Label(root, text="Teste Teórico:")
        self.entry_teste_teorico = ttk.Entry(root)

        self.label_teste_pratico = ttk.Label(root, text="Teste Prático:")
        self.entry_teste_pratico = ttk.Entry(root)

        self.label_soft_skills = ttk.Label(root, text="Avaliação de Soft Skills:")
        self.entry_soft_skills = ttk.Entry(root)

        self.btn_cadastrar = ttk.Button(root, text="Cadastrar", command=self.cadastrar_candidato)
        self.btn_gerar_relatorio_completo = ttk.Button(root, text="Relatório Completo", command=self.gerar_relatorio_completo)
        self.btn_gerar_relatorio_resumido = ttk.Button(root, text="Relatório Resumido", command=self.gerar_relatorio_resumido)

        self.label_nome.grid(row=0,

 column=0, sticky=tk.W, pady=5, padx=5)
        self.entry_nome.grid(row=0, column=1, pady=5, padx=5)
        self.label_telefone.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.entry_telefone.grid(row=1, column=1, pady=5, padx=5)
        self.label_minibio.grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.entry_minibio.grid(row=2, column=1, pady=5, padx=5)
        self.label_entrevista.grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.entry_entrevista.grid(row=3, column=1, pady=5, padx=5)
        self.label_teste_teorico.grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)
        self.entry_teste_teorico.grid(row=4, column=1, pady=5, padx=5)
        self.label_teste_pratico.grid(row=5, column=0, sticky=tk.W, pady=5, padx=5)
        self.entry_teste_pratico.grid(row=5, column=1, pady=5, padx=5)
        self.label_soft_skills.grid(row=6, column=0, sticky=tk.W, pady=5, padx=5)
        self.entry_soft_skills.grid(row=6, column=1, pady=5, padx=5)
        self.btn_cadastrar.grid(row=7, column=0, columnspan=2, pady=10)
        self.btn_gerar_relatorio_completo.grid(row=8, column=0, pady=10)
        self.btn_gerar_relatorio_resumido.grid(row=8, column=1, pady=10)

    def cadastrar_candidato(self):
        nome = self.entry_nome.get()
        telefone = self.entry_telefone.get()
        minibio = self.entry_minibio.get("1.0", tk.END)
        entrevista = float(self.entry_entrevista.get())
        teste_teorico = float(self.entry_teste_teorico.get())
        teste_pratico = float(self.entry_teste_pratico.get())
        soft_skills = float(self.entry_soft_skills.get())

        candidato = Candidato(nome, telefone, minibio, entrevista, teste_teorico, teste_pratico, soft_skills)
        self.gerenciador.cadastrar_candidato(candidato)
        messagebox.showinfo("Sucesso", "Candidato cadastrado com sucesso!")

    def gerar_relatorio_completo(self):
        self.gerenciador.gerar_relatorio_completo()
        messagebox.showinfo("Sucesso", "Relatório completo gerado com sucesso!")

    def gerar_relatorio_resumido(self):
        self.gerenciador.gerar_relatorio_resumido()
        messagebox.showinfo("Sucesso", "Relatório resumido gerado com sucesso!")