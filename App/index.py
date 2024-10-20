from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QMainWindow,QMessageBox
from PyQt5.QtCore import pyqtSignal
import sys
import sqlite3
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox
import requests
import re
import threading
import time
import queue


#importação dos components necessarios

from Components.Avamonitor import LogMonitorWindow
from Modules.LimparLogs import limpar_arquivo_log
from Components.AvaBuscarMateria import Janela_Busca
from Server.MaquinaSCKT import iniciarMaquina
from Components.AvaConfig import Janela_Config
from Components.AvaBuscarLivro import Janela_Busca_livro
from Components.add_Usuario import Janela_Adicionar_Usuario
# from Components.AvaWebEngineView import CriarWebEngine #Modulo Retirado na v1

tamanho_tab = 550
largura_tab = 440

conn = sqlite3.connect('./Database/avaBook.db')
c = conn.cursor()

def EscolherMetodo(opcao):
        if(opcao == "consulta"):
                c.execute("SELECT * FROM materias")
                resultados = c.fetchall()
                return resultados
        elif(opcao == "ListUsuario"):
                c.execute("SELECT * FROM usuario")
                resultados = c.fetchall()
                return resultados

# Carrgar Dados do Banco
buscaMateriais = EscolherMetodo("consulta")

iniciarMaquina("Start")


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(840, 530)
        self.ContainerConfig = QtWidgets.QFrame(Dialog)
        self.ContainerConfig.setEnabled(True)
        self.ContainerConfig.setGeometry(QtCore.QRect(10, 10, 251, 441))
        self.ContainerConfig.setStyleSheet("background-color: rgba(255, 255, 255, 0.95);\n"
"")
        self.ContainerConfig.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ContainerConfig.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ContainerConfig.setObjectName("ContainerConfig")
        self.Logo = QtWidgets.QLabel(self.ContainerConfig)
        self.Logo.setGeometry(QtCore.QRect(20, 10, 231, 131))
        self.Logo.setObjectName("Logo")
        self.frame = QtWidgets.QFrame(self.ContainerConfig)
        self.frame.setEnabled(True)
        self.frame.setGeometry(QtCore.QRect(10, 150, 221, 5))
        self.frame.setStyleSheet("background-color: rgb(199, 199, 199);\n"
"border-radius:50px;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.ContainerConfig)
        self.frame_2.setEnabled(True)
        self.frame_2.setGeometry(QtCore.QRect(10, 260, 221, 5))
        self.frame_2.setStyleSheet("background-color: rgb(199, 199, 199);\n"
"border-radius:50px;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.buscar_materia = QtWidgets.QPushButton(self.ContainerConfig)
        self.buscar_materia.setGeometry(QtCore.QRect(10, 280, 121, 31))
        self.buscar_materia.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buscar_materia.setStyleSheet("background-color: rgb(5, 111, 176);\n"
"border-radius:2px;\n"
"color:#fff;\n"
"\n"
"QPushButton::hover {\n"
"    background-color: rgb(74, 101, 255);\n"
"}\n"
"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./App/Assets/Seach.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buscar_materia.setIcon(icon)
        self.buscar_materia.setObjectName("buscar_materia")
        self.config = QtWidgets.QPushButton(self.ContainerConfig)
        self.config.setGeometry(QtCore.QRect(140, 280, 91, 31))
        self.config.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.config.setStyleSheet("background-color: rgb(5, 111, 176);\n"
"border-radius:2px;\n"
"color:#fff;\n"
"\n"
"QPushButton::hover {\n"
"    background-color: rgb(74, 101, 255);\n"
"}\n"
"")
        self.config.setObjectName("config")
        self.selecionar_materia = QtWidgets.QComboBox(self.ContainerConfig)
        self.selecionar_materia.setGeometry(QtCore.QRect(10, 340, 221, 31))
        self.selecionar_materia.setObjectName("selecionar_materia")
        
        #;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
        self.selecionar_materia = QtWidgets.QComboBox(self.ContainerConfig)
        self.selecionar_materia.setGeometry(QtCore.QRect(10, 340, 221, 31))
        self.selecionar_materia.setObjectName("selecionar_materia")
        # Definir o texto padrão para o item zero
        self.selecionar_materia.addItem("Escolha a Materia...")
        # Desabilitar o item zero
        self.selecionar_materia.setItemData(0, False)
        #;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
        
        self.iniciar = QtWidgets.QPushButton(self.ContainerConfig)
        self.iniciar.setGeometry(QtCore.QRect(10, 390, 221, 31))
        self.iniciar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.iniciar.setStyleSheet("background-color: rgb(5, 111, 176);\n"
"border-radius:2px;\n"
"color:#fff;\n"
"\n"
"QPushButton::hover {\n"
"    background-color: rgb(74, 101, 255);\n"
"}\n"
"")
        self.iniciar.setObjectName("iniciar")
        self.label_7 = QtWidgets.QLabel(self.ContainerConfig)
        self.label_7.setGeometry(QtCore.QRect(10, 320, 221, 20))
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.ContainerInputs = QtWidgets.QFrame(self.ContainerConfig)
        self.ContainerInputs.setGeometry(QtCore.QRect(10, 169, 221, 71))
        self.ContainerInputs.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ContainerInputs.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ContainerInputs.setObjectName("ContainerInputs")
        self.BoxUsername = QtWidgets.QFrame(self.ContainerInputs)
        self.BoxUsername.setGeometry(QtCore.QRect(0, 0, 221, 31))
        self.BoxUsername.setStyleSheet("border:1px solid rgb(209, 209, 209);")
        self.BoxUsername.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.BoxUsername.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BoxUsername.setObjectName("BoxUsername")
        self.campoUsuario = QtWidgets.QLineEdit(self.BoxUsername)
        self.campoUsuario.setGeometry(QtCore.QRect(40, 0, 181, 31))
        self.campoUsuario.setStyleSheet("border-color: rgb(209, 209, 209);")
        self.campoUsuario.setInputMask("")
        self.campoUsuario.setClearButtonEnabled(True)
        self.campoUsuario.setObjectName("campoUsuario")
        self.iconLabelUser = QtWidgets.QLabel(self.BoxUsername)
        self.iconLabelUser.setGeometry(QtCore.QRect(0, 0, 41, 31))
        self.iconLabelUser.setObjectName("iconLabelUser")
        self.BoxPassword = QtWidgets.QFrame(self.ContainerInputs)
        self.BoxPassword.setGeometry(QtCore.QRect(0, 40, 221, 31))
        self.BoxPassword.setStyleSheet("border:1px solid rgb(209, 209, 209);")
        self.BoxPassword.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.BoxPassword.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BoxPassword.setObjectName("BoxPassword")
        self.campoSenha = QtWidgets.QLineEdit(self.BoxPassword)
        self.campoSenha.setGeometry(QtCore.QRect(40, 0, 181, 31))
        self.campoSenha.setStyleSheet("border-color: rgb(209, 209, 209);")
        self.campoSenha.setInputMask("")
        self.campoSenha.setClearButtonEnabled(True)
        self.campoSenha.setObjectName("campoSenha")
        self.iconLabelSenha = QtWidgets.QLabel(self.BoxPassword)
        self.iconLabelSenha.setGeometry(QtCore.QRect(0, 0, 41, 31))
        self.iconLabelSenha.setObjectName("iconLabelSenha")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(270, 10, tamanho_tab, largura_tab))
        self.tabWidget.setObjectName("tabWidget")
        self.Navegador = QtWidgets.QWidget()
        self.Navegador.setObjectName("Navegador")
        self.ContainerWebEngine = QtWidgets.QFrame(self.Navegador)
        self.ContainerWebEngine.setEnabled(False)
        self.ContainerWebEngine.setGeometry(QtCore.QRect(-10, -10, tamanho_tab, 471))
        self.ContainerWebEngine.setStyleSheet("background-color: rgb(255, 255, 127);\n"
"")
        self.ContainerWebEngine.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ContainerWebEngine.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ContainerWebEngine.setObjectName("ContainerWebEngine")
        self.scrollArea = QtWidgets.QScrollArea(self.ContainerWebEngine)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, tamanho_tab, largura_tab))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 339, 409))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widget.setGeometry(QtCore.QRect(10, 10, tamanho_tab - 30, largura_tab - 200))
        self.widget.setStyleSheet("background-color: rgb(85, 255, 127);")
        self.widget.setObjectName("widget")
        self.frame_3 = QtWidgets.QFrame(self.widget)
        self.frame_3.setEnabled(False)
        self.frame_3.setGeometry(QtCore.QRect(0, 40, tamanho_tab, 5))
        self.frame_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius:50px;")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.titulo_card = QtWidgets.QLabel(self.widget)
        self.titulo_card.setGeometry(QtCore.QRect(10, 10, tamanho_tab, 21))
        self.titulo_card.setObjectName("titulo_card")
        self.data_card = QtWidgets.QLabel(self.widget)
        self.data_card.setGeometry(QtCore.QRect(240, 10, tamanho_tab, 21))
        self.data_card.setObjectName("data_card")
        self.uuid = QtWidgets.QLabel(self.widget)
        self.uuid.setGeometry(QtCore.QRect(10, 50, tamanho_tab, 21))
        self.uuid.setObjectName("uuid")
        self.email = QtWidgets.QLabel(self.widget)
        self.email.setGeometry(QtCore.QRect(10, 74, tamanho_tab, 22))
        self.email.setObjectName("email")
        self.id_atividade = QtWidgets.QLabel(self.widget)
        self.id_atividade.setGeometry(QtCore.QRect(10, 100, tamanho_tab, 22))
        self.id_atividade.setObjectName("id_atividade")
        self.nome_usuario = QtWidgets.QLabel(self.widget)
        self.nome_usuario.setGeometry(QtCore.QRect(10, 130, tamanho_tab, 20))
        self.nome_usuario.setObjectName("nome_usuario")
        self.downloadbookExport = QtWidgets.QPushButton(self.widget)
        self.downloadbookExport.setGeometry(QtCore.QRect(tamanho_tab - 200, 60, tamanho_tab - 400, 31))
        self.downloadbookExport.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.downloadbookExport.setStyleSheet("background-color: rgb(255, 170, 127);\n"
"border-radius:2px;\n"
"color: rgb(0, 0, 0);\n"
"\n"
"QPushButton::hover {\n"
"    background-color: rgb(74, 101, 255);\n"
"}\n"
"")
        self.downloadbookExport.setObjectName("downloadbookExport")
        self.downloadbookExport_2 = QtWidgets.QPushButton(self.widget)
        self.downloadbookExport_2.setGeometry(QtCore.QRect(tamanho_tab - 200, 100, tamanho_tab - 400, 31))
        self.downloadbookExport_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.downloadbookExport_2.setStyleSheet("background-color: rgb(255, 255, 127);\n"
"color: rgb(0, 0, 0);\n"
"border-radius:2px;\n"
"\n"
"\n"
"QPushButton::hover {\n"
"    background-color: rgb(74, 101, 255);\n"
"}\n"
"")
        self.downloadbookExport_2.setObjectName("downloadbookExport_2")
        self.downloadbookExport_3 = QtWidgets.QPushButton(self.widget)
        self.downloadbookExport_3.setGeometry(QtCore.QRect(tamanho_tab - 200, 140, tamanho_tab - 400, 31))
        self.downloadbookExport_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.downloadbookExport_3.setStyleSheet("background-color: rgb(0, 0, 255);\n"
"color: #fff;\n"
"border-radius:2px;\n"
"\n"
"\n"
"QPushButton::hover {\n"
"    background-color: rgb(74, 101, 255);\n"
"}\n"
"")
        self.downloadbookExport_3.setObjectName("downloadbookExport_3")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget.addTab(self.Navegador, "")
        self.Deploy = QtWidgets.QWidget()
        self.Deploy.setObjectName("Deploy")
        self.ContainerWebEngine_2 = QtWidgets.QFrame(self.Deploy)
        self.ContainerWebEngine_2.setEnabled(True)
        self.ContainerWebEngine_2.setGeometry(QtCore.QRect(0, 0,tamanho_tab, largura_tab))
        self.ContainerWebEngine_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.ContainerWebEngine_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ContainerWebEngine_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ContainerWebEngine_2.setObjectName("ContainerWebEngine_2")
        self.label_9 = QtWidgets.QLabel(self.ContainerWebEngine_2)
        self.label_9.setGeometry(QtCore.QRect(10, 10,tamanho_tab - 50, 16))
        self.label_9.setObjectName("label_9")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.ContainerWebEngine_2)
        self.scrollArea_2.setEnabled(True)
        self.scrollArea_2.setGeometry(QtCore.QRect(10, 40, tamanho_tab - 50, largura_tab - 200))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 319, 259))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        # Define as políticas de rolagem (opcional)
        
        self.scrollArea_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)  # Habilita barra de rolagem vertical
        self.scrollArea_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)  # Barra de rolagem horizontal se necessário
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.label_10 = QtWidgets.QLabel(self.ContainerWebEngine_2)
        self.label_10.setGeometry(QtCore.QRect(10, 390, 81, 16))
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        self.buttonLimparLogs = QtWidgets.QPushButton(self.ContainerWebEngine_2)
        self.buttonLimparLogs.setGeometry(QtCore.QRect(10, 310, 131, 31))
        self.buttonLimparLogs.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonLimparLogs.setEnabled(True)
        self.buttonLimparLogs.setStyleSheet("background-color: rgb(255, 99, 99);\n"
"border-radius:2px;\n"
"color: rgb(0, 0, 0);\n"
"QPushButton::hover {\n"
"    background-color: rgb(74, 101, 255);\n"
"}\n"
"")
        self.buttonLimparLogs.setObjectName("buttonLimparLogs")
        self.tabWidget.addTab(self.Deploy, "")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 460, 251, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(270, 460, 351, 51))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Logo.setText(_translate("Dialog", "<html><head/><body><p><img width=200 src='./App/Assets/Logo.png'/></p></body></html>"))
        self.buscar_materia.setText(_translate("Dialog", "Buscar Materia"))
        
        
       #;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;       
      
        def extrair_valores_conf(nome_arquivo):
                with open(nome_arquivo, 'r') as file:
                        linhas = file.readlines()  # Lê todas as linhas do arquivo
                        for linha in linhas:
                                if linha.startswith('host_servidor'):
                                        host_servidor = linha.split('=')[1].strip()  # Extrai o valor após o '='
                                elif linha.startswith('porta_servidor'):
                                        porta_servidor = int(linha.split('=')[1].strip())  # Extrai o valor após o '=' e converte para inteiro
                                elif linha.startswith('rota_oringi'):
                                        valor_path = linha.split('=')[1].strip()  # Extrai o valor após o '='
                                        rota_oringi = re.sub(r'["\[\]]', '', valor_path)
                                elif linha.startswith('time_requisao_pacotes'):
                                        requisicao_emisao_pacotes = int(linha.split('=')[1].strip()) 
                                elif linha.startswith('rota_user'):
                                        valor_path = linha.split('=')[1].strip()  # Extrai o valor após o '='
                                        rota_user = re.sub(r'["\[\]]', '', valor_path)
                                       
                return host_servidor, porta_servidor,rota_oringi, requisicao_emisao_pacotes,rota_user

        # Caminho para o arquivo .Conf
        caminho_arquivo = './App/Config/.Conf'
        #listar Usuários
        usuariosRecente = EscolherMetodo("ListUsuario")
        
        fila_dados_materia = queue.Queue()
        # Extraindo o host e a porta do servidor
        host_servidor, porta_servidor,rota_oringi, requisicao_emisao_pacotes,rota_user = extrair_valores_conf(caminho_arquivo)                
        
        def iniciarInputorSelect():
                verificar_usuarios = len(usuariosRecente)
                
                if verificar_usuarios == 0 or verificar_usuarios is None:
                        self.BoxUsername.show()
                        self.BoxPassword.show()
                else:
                        self.BoxUsername.hide()
                        self.BoxPassword.hide()
                        
                        self.labelUsuariosRecentes = QLabel(self.ContainerConfig)
                        self.labelUsuariosRecentes.setGeometry(QtCore.QRect(10, 160, 221, 31))
                        self.labelUsuariosRecentes.setObjectName("usuarios_recentes")
                        self.labelUsuariosRecentes.setText("Usuários Recentes")
                        self.labelUsuariosRecentes.setAlignment(QtCore.Qt.AlignCenter)
                        self.labelUsuariosRecentes.setStyleSheet("""
                        QLabel {
                                color: #333;
                                font-size: 18px; 
                                font-weight: bold;
                                padding-bottom: 5px;
                                border-bottom: 2px solid #333; 
                                text-align: center; /* Centraliza o texto */
                        }
                        """)
                        
                        self.selecionar_usuarios = QtWidgets.QComboBox(self.ContainerConfig)
                        self.selecionar_usuarios.setGeometry(QtCore.QRect(10, 190, 221, 31)) 
                        self.selecionar_usuarios.setObjectName("Selecione o Usuário...")
                        # Definir o texto padrão para o item zero
                        self.selecionar_usuarios.addItem("Escolha o usuário...")
                        # Desabilitar o item zero
                        # self.selecionar_usuarios.setItemData(0, False)  # Remove or comment out this line
                        
                        self.btn_config_usuarios = QtWidgets.QPushButton(self.ContainerConfig)
                        self.btn_config_usuarios.setText("Add Usuário")
                        self.btn_config_usuarios.setGeometry(QtCore.QRect(10, 230, 221, 31)) 
                        self.btn_config_usuarios.setObjectName("config_app")
                        self.btn_config_usuarios.setStyleSheet("""
                        background-color: rgb(5, 111, 176);
                        border-radius:2px;
                        color:#fff;

                        QPushButton::hover {
                                background-color: rgb(74, 101, 255);
                        }
                        """)
                        self.btn_config_usuarios.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                        
                        def atualizar_campos(index):
                                if index > 0:  # Ignore the item "Usuario Recentes..."
                                        selected_index = index - 1  # Adjust index to match the list
                                        tupla = usuariosRecente[selected_index]
                                        self.campoUsuario.setText(tupla[1])  # Set username
                                        self.campoSenha.setText(tupla[2])  # Set password
                                
                        for index, usuario in enumerate(usuariosRecente):
                                tuplaUsuario = usuario[1]
                                tuplaSenha = usuario[2]
                                self.selecionar_usuarios.addItem(tuplaUsuario)
                                
                                result = self.selecionar_usuarios.currentIndexChanged.connect(atualizar_campos)
                                
                        # print(f"Usuarios Encontrados usuario => {tuplaUsuario} senha => {tuplaSenha} ")

        iniciarInputorSelect()
        
        def obter_dados_materia():
                try:
                        response = requests.get(f'http://{host_servidor}:{porta_servidor}{rota_oringi}')
                        if response.status_code == 200:
                                print(f"Recebendo Sockets ... [{host_servidor}]:[{porta_servidor}]:[{rota_oringi}]")
                                dados = response.json()

                                # Remova todos os itens do ComboBox, exceto o primeiro item
                                for i in range(1, self.selecionar_materia.count()):
                                        self.selecionar_materia.removeItem(1)

                                
                                index = 0  
                                indexMarteria = 0  # Inicialize indexMateria como 0
                                for index,dadosMateria in enumerate(dados):
                                      
                                        if not dadosMateria or len(dadosMateria) == 0:  # Corrigindo a condição
                                                self.selecionar_materia.addItem("Sem Materias...")
                                        else: 
                                                self.selecionar_materia.addItem(dadosMateria[1])

                                if index == 0:
                                        indexMarteria = index
                                else:
                                        indexMarteria = index + 1  # Definindo indexMateria após o loop
                                
                                if indexMarteria:  # Verifique se indexMateria não é zero ou falso
                                        return indexMarteria
                                else:
                                        return 0
                                
                        else:
                                print("Materias do Banco")
                                
                                index = 0  # Inicialize index antes do loop
                                indexMarteria = 0  # Inicialize indexMateria como 0
                                
                                for i in range(1, self.selecionar_materia.count()):
                                        self.selecionar_materia.removeItem(1)
                        
                                for index, materias in enumerate(buscaMateriais):
                                        indexMarteria = index + 1
                                        if not materias or len(materias) == 0:  # Corrigindo a condição
                                                self.selecionar_materia.addItem("Sem Materias...")
                                        else:
                                                tuplaMaterias = materias[1:][0]
                                                self.selecionar_materia.addItem(tuplaMaterias)
                                print("Construindo Banco SQLITE")  # Movendo o print para fora do loop
                                if index == 0:
                                        indexMarteria = index
                                else:
                                        indexMarteria = index + 1  # Definindo indexMateria após o loop
                        if indexMarteria:  # Verifique se indexMateria não é zero ou falso
                                return indexMarteria
                        else:
                                return 0
                        
                except requests.exceptions.ConnectionError as e:
                        print("Erro de conexão: ", e)
                        return 0  # Retorna 0 em caso de erro de conexão

        # indexMateria = obter_dados_materia()
        
        # Cria uma fila para comunicar os dados da matéria entre as threads
                
        fila_dados_materia = queue.Queue()
        def temporizado(queue):
                while True:
                        
                        indexMateria = obter_dados_materia()
                        queue.put(indexMateria)  
                        time.sleep(requisicao_emisao_pacotes)  

        thread_temporizada = threading.Thread(target=temporizado,args=(fila_dados_materia,))
        thread_temporizada.daemon = True  
        thread_temporizada.start()
        
        #;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
        
        
        self.config.setText(_translate("Dialog", "Config"))
        self.iniciar.setText(_translate("Dialog", "Iniciar Transmissão"))
        self.label_7.setText(_translate("Dialog", "Escolher Materia"))
        self.campoUsuario.setText(_translate("Dialog", "Usuário Ava ..."))
        self.iconLabelUser.setText(_translate("Dialog", "<html><head/><body><p><img src='./App/Assets/User.png'/></p></body></html>"))
        self.campoSenha.setText(_translate("Dialog", "Senha Ava ..."))
        self.iconLabelSenha.setText(_translate("Dialog", "<html><head/><body><p><img src='./App/Assets/Pass.png'/></p></body></html>"))
        self.titulo_card.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">ANALISE ORIENTADA...</span></p></body></html>"))
        self.data_card.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">20/01/2024</span></p></body></html>"))
        self.uuid.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">UUID: XXX-XXX-XXX-XX</span></p></body></html>"))
        self.email.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">EMAIL: daniel@gmail.com</span></p></body></html>"))
        self.id_atividade.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">ID ATIVIDADE: 3925709</span></p></body></html>"))
        self.nome_usuario.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">NOME: Daniel</span></p></body></html>"))
        self.downloadbookExport.setText(_translate("Dialog", "Unificar Fragmentos"))
        self.downloadbookExport_2.setText(_translate("Dialog", "Zip Fragmentos"))
        self.downloadbookExport_3.setText(_translate("Dialog", "Vizualizar PDF"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Navegador), _translate("Dialog", "Navegador"))
        self.label_9.setText(_translate("Dialog", "Sockets Emitter"))
        self.buttonLimparLogs.setText(_translate("Dialog", "Limpar Logs"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Deploy), _translate("Dialog", "Sockets"))
        self.pushButton.setText(_translate("Dialog", "Contribuir no Projeto"))
        self.pushButton_2.setText(_translate("Dialog", "Doe para o Criador"))
         #Cria o QLabel para exibir a mensagem de logs limpos
        self.labelLogs = QtWidgets.QLabel(self.ContainerWebEngine_2)
        self.labelLogs.setGeometry(QtCore.QRect(180, 320, 200, 20))  # Defina a geometria adequada para o seu QLabel
        self.labelLogs.hide()  # Oculta o QLabel inicialmente
        
        # Evento para Limpar Logs
        self.buttonLimparLogs.clicked.connect(self.limpar_logs)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Deploy), _translate("Dialog", "Sockets"))
        
        #Evento para Atualizar o emitter Socket
        self.tabWidget.currentChanged.connect(self.on_tab_changed)
        
        
         # Conectando o botão ao método on_click
        self.btn_config_usuarios.clicked.connect(self.adicionarUsuario)
        self.buscar_materia.clicked.connect(self.abrir_Janela_Busca)
        self.config.clicked.connect(self.abrir_Janela_config)     
        self.iniciar.clicked.connect(self.Buscar_Livros_Ava_Open)

    def abrir_Janela_Busca(self):
        # Esta função cria uma nova janela e mantém uma referência a ela
        self.janela_de_busca = Janela_Busca()
        self.janela_de_busca.show()
        
    def adicionarUsuario(self):
           self.janela_de_usuario =  Janela_Adicionar_Usuario()
           self.janela_de_usuario =  self.janela_de_usuario.show()

    def Buscar_Livros_Ava_Open(self):
        
        # print(self.campoUsuario.text())
        # print(self.campoSenha.text())
        # QMessageBox.information(None, 'Sucesso', 'Busca Realizada Com Sucesso , Enviando Pacote <SKC4>')
        
        username = self.campoUsuario.text()
        password = self.campoSenha.text()
        materia  = self.selecionar_materia.currentText()

        if username == "Usuário Ava ..." or password == "Senha Ava ..." or  materia == "Escolha a Materia...":
                QMessageBox.critical(None, 'Campo Invalido', 'Erro Campos Vazios...')
        else:
                if username == "" or password == "" or  materia == "":
                        QMessageBox.critical(None, 'Campo Invalido', 'Erro Campos Vazios...')
                else:
                        Janela_livro = Janela_Busca_livro(Dialog,username,password,materia)
                        Janela_livro.exec_()
                        
        
    def limpar_logs(self):
        # Limpa o arquivo de log
        caminho_arquivo = './App/Logs/webdriver.log'
        limpar_arquivo_log(caminho_arquivo)
        self.labelLogs.setText("Logs Limpos com Sucesso")
        self.labelLogs.setStyleSheet("color: green;")  # Define o texto em verde
        # Mostra a mensagem de sucesso
        self.labelLogs.show()

        # Define um temporizador para ocultar a mensagem após 3 segundos
        QtCore.QTimer.singleShot(3000, self.labelLogs.hide)  # Oculta após 3 segundos

        
    def abrir_Janela_config(self):
        # Esta função cria uma nova janela e mantém uma referência a ela
        self.janela_de_configuracao = Janela_Config()
        self.janela_de_configuracao.show()
        
    
    def on_tab_changed(self,index):
        # Imprime o índice da aba selecionada
        # print(f"Aba {index} selecionada")
        
        if index == 0:
                print("Downloads")
              
        elif index == 1:
                # print("Logs")
               #Abriar arquvio de log no ./App/Logs/webdriver.log
                self.MonitorLogs = LogMonitorWindow(False,1000)  # Passe True para habilitarLogs para atualizar o log a cada segundo
                        # print(MonitorLogs)
                self.scrollArea_2.setWidget(self.MonitorLogs)  
        
        
        
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
