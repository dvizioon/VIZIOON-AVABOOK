from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QListView
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5 import QtGui,QtCore
from PyQt5.QtCore import QObject, pyqtSignal
import sqlite3
import time

from .BuscarMaterialHand import BuscarLivroHand
app = QApplication([])


# Conecta ao banco de dados
conn = sqlite3.connect('./Database/avaBook.db')
c = conn.cursor()

def queryDb(option,usuario,senha):
    if(option == "Consulta"):
        c.execute("SELECT * FROM materias")
        resultados = c.fetchall()
        return resultados
    elif(option == "UsuarioSave"):
        # Verifica se o nome já existe no banco de dados
        c.execute("SELECT * FROM usuario WHERE nome = ? and senha = ?", (usuario,senha))
        data = c.fetchone()
        # Se 'data' for None, o nome não existe no banco de dados e pode ser inserido
        if data is None:
            c.execute("INSERT INTO usuario (nome,senha) VALUES (?,?)", (usuario,senha))
                # Salva as alterações
            conn.commit()
    elif(option == "ListUsuario"):
        c.execute("SELECT * FROM usuario")
        resultados = c.fetchall()
        return resultados


def templateRendeComponents(resultado, list_view):
    list_view.setStyleSheet("color: blue;")  # Definindo a cor do texto como verde
    labelSucesso = QLabel(f"================================\n >>> Materias Encontradas \n================================\n")
    model = QStandardItemModel()
    item = QStandardItem(labelSucesso.text())
    model.appendRow(item)  # Adiciona o item ao modelo
    # print(resultado)
    for idx, tupla in enumerate(resultado):
        materia = tupla[1]
        item = QStandardItem(f"📌 ( {idx+1} ) {materia}")  # Adiciona o índice antes do item
        model.appendRow(item)
        list_view.setModel(model)

    list_view.setModel(model)



def varredura_sistema(usuario, senha, list_view,janela_principal):
    if usuario == "" or senha == "":
        QMessageBox.warning(None, 'Varredura do Sistema', 'Usuário ou senha inválidos.')
    else:
        queryDb("UsuarioSave",usuario,senha)
        
        resultado, loading = BuscarLivroHand(usuario, senha)
        if resultado == False:
            model = list_view.model()  # Obtém o modelo atual
            model.clear()  # Limpa o modelo
            list_view.setStyleSheet("color: red;")  # Definindo a cor do texto como verde
            labelErro = QLabel(f"Erro Consulta: \nMatricula não Existe\nUsuário:{usuario}\nStatus:[401] ")
            item = QStandardItem(labelErro.text())
            model.appendRow(item)  # Adiciona o item ao modelo
        else:
            list_view.setStyleSheet("color: green;")  # Definindo a cor do texto como verde
            labelSucesso = QLabel(f"================================\n >>> Materias Pesquisadas \n================================\n")
            model = QStandardItemModel()
            item = QStandardItem(labelSucesso.text())
            model.appendRow(item)  # Adiciona o item ao modelo
            # print(resultado)
            for idx, materia in enumerate(resultado):
                item = QStandardItem(f"✅ ( {idx+1} ) {materia}")  # Adiciona o índice antes do item
                model.appendRow(item)
                list_view.setModel(model)

            list_view.setModel(model)
            
            # time.sleep(3)
            # QMessageBox.information(None, 'Sucesso', 'Busca Realizada Com Sucesso , Enviando Pacote <SKC4>')
            # janela_principal.close()
            # print(resultado)


def Janela_Busca():

    janela_principal = QWidget()
    janela_principal.setWindowTitle('Janela de Busca')
    janela_principal.setFixedWidth(300)
    janela_principal.setFixedHeight(400)
    
    layout = QVBoxLayout()
    
    campo_usuario = QLineEdit()
    campo_usuario.setPlaceholderText('Usuário')
    campo_senha = QLineEdit()
    campo_senha.setPlaceholderText('Senha')
    campo_senha.setEchoMode(QLineEdit.Password)
    
    label_user = QLabel('Usuário Ava')
    layout.addWidget(label_user)
    layout.addWidget(campo_usuario)
        
    label_senha = QLabel('Senha Ava')
    layout.addWidget(label_senha)
    layout.addWidget(campo_senha)
    
    # # Cria um novo QComboBox
    
    def atualizar_campos(index):
        if index > 0:  # Ignora o item "Usuario Recentes..."
            tupla = usuariosRecente[index - 1]
            campo_usuario.setText(tupla[1])
            campo_senha.setText(tupla[2])

    combo = QComboBox()
    usuariosRecente = queryDb("ListUsuario","","")
    # print(usuariosRecente)
    combo.addItem("Usuario Recentes...")
    for idx, tupla in enumerate(usuariosRecente):
        usuario = tupla[1]
        combo.addItem(usuario)

    combo.currentIndexChanged.connect(atualizar_campos)
    layout.addWidget(combo)
    # combo.hide()
    if len(usuariosRecente) == 0:
        combo.hide()
    else:
        combo.show()

    list_view = QListView()
    layout.addWidget(list_view)
    list_view.setStyleSheet("color: green;")  # Definindo a cor do texto como verde

    botao_handles = QPushButton('Pesquisar -- Modo Socket')
    botao_handles.setStyleSheet("background-color: blue; color: white; padding: 10px;")
    botao_handles.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # Mudar cursor para mãozinha
    botao_handles.setStyleSheet("""
        QPushButton {
            background-color: rgb(5, 111, 176);
            color: white;
            padding: 10px;
            border-radius: 5px;
            border: none;
        }
        QPushButton:hover {
             background-color: rgb(5, 80, 176);

        }
    """)
    
    layout.addWidget(botao_handles)
    
    botao_handles.clicked.connect(lambda: varredura_sistema(campo_usuario.text(), campo_senha.text(), list_view,janela_principal))
    
    templateRendeComponents(queryDb("Consulta","",""), list_view)
    
    janela_principal.setLayout(layout)
    janela_principal.show()
    # Connect the signal to a slot in the other module
    

    return janela_principal


# app = QApplication([])
# janela = Janela_Busca()
# app.exec_()
