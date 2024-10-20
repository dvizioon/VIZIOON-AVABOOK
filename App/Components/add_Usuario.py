from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox
from PyQt5 import QtGui, QtCore
import sqlite3

# Conecta ao banco de dados
conn = sqlite3.connect('./Database/avaBook.db')
c = conn.cursor()

def queryDb(option, usuario="", senha=""):
    if option == "UsuarioSave":
        # Verifica se o nome já existe no banco de dados
        c.execute("SELECT * FROM usuario WHERE nome = ? AND senha = ?", (usuario, senha))
        data = c.fetchone()
        # Se 'data' for None, o nome não existe no banco de dados e pode ser inserido
        if data is None:
            c.execute("INSERT INTO usuario (nome, senha) VALUES (?, ?)", (usuario, senha))
            # Salva as alterações
            conn.commit()
            return True
        else:
            return False
    elif option == "ListUsuario":
        c.execute("SELECT * FROM usuario")
        resultados = c.fetchall()
        return resultados

def adicionar_usuario(usuario, senha, janela_principal):
    if usuario == "" or senha == "":
        QMessageBox.warning(janela_principal, 'Erro', 'Usuário ou senha não podem estar vazios.')
    else:
        sucesso = queryDb("UsuarioSave", usuario, senha)
        if sucesso:
            QMessageBox.information(janela_principal, 'Sucesso', 'Usuário adicionado com sucesso.')
        else:
            QMessageBox.warning(janela_principal, 'Erro', 'Usuário já existe.')

def Janela_Adicionar_Usuario():
    janela_principal = QWidget()
    janela_principal.setWindowTitle('Adicionar Usuário')
    janela_principal.setFixedWidth(300)
    janela_principal.setFixedHeight(200)

    layout = QVBoxLayout()

    campo_usuario = QLineEdit()
    campo_usuario.setPlaceholderText('Usuário')
    campo_senha = QLineEdit()
    campo_senha.setPlaceholderText('Senha')
    campo_senha.setEchoMode(QLineEdit.Password)

    label_user = QLabel('Nome de Usuário')
    layout.addWidget(label_user)
    layout.addWidget(campo_usuario)

    label_senha = QLabel('Senha')
    layout.addWidget(label_senha)
    layout.addWidget(campo_senha)

    botao_adicionar = QPushButton('Adicionar Usuário')
    botao_adicionar.setStyleSheet("background-color: green; color: white; padding: 10px;")
    layout.addWidget(botao_adicionar)

    # Conecta o botão à função de adicionar usuário e passa a janela como argumento
    botao_adicionar.clicked.connect(lambda: adicionar_usuario(campo_usuario.text(), campo_senha.text(), janela_principal))

    janela_principal.setLayout(layout)
    janela_principal.show()

    return janela_principal

# Inicialização do aplicativo
# app = QApplication([])
# janela = Janela_Adicionar_Usuario()
# app.exec_()
