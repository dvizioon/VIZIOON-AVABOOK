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

from Components.Avamonitor import janelaMonitor
from Modules.LimparLogs import limpar_arquivo_log
from Components.AvaBuscarMateria import Janela_Busca
from Server.MaquinaSCKT import iniciarMaquina
from Components.AvaConfig import Janela_Config
from Components.AvaBuscarLivro import Janela_Busca_livro
# from Components.AvaWebEngineView import CriarWebEngine #Modulo Retirado na v1

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
        Dialog.resize(640, 517)
        self.ContainerConfig = QtWidgets.QFrame(Dialog)
        self.ContainerConfig.setEnabled(True)
        self.ContainerConfig.setGeometry(QtCore.QRect(10, 10, 251, 441))
        self.ContainerConfig.setStyleSheet("background-color: rgba(255, 255, 255, 0.95);\n"
"")
        
      
                        
        self.ContainerConfig.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ContainerConfig.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ContainerConfig.setObjectName("ContainerConfig")
        
        self.ContainerInputs = QtWidgets.QFrame(self.ContainerConfig)
        self.ContainerInputs.setGeometry(QtCore.QRect(10, 169, 221, 71))
        # self.ContainerInputs.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.ContainerInputs.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ContainerInputs.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ContainerInputs.setObjectName("ContainerInputs")
        
        
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
        self.BoxUsername = QtWidgets.QFrame(self.ContainerConfig)
        self.BoxUsername.setGeometry(QtCore.QRect(10, 170, 221, 31))
        self.BoxUsername.setStyleSheet("border:1px solid rgb(209, 209, 209);")
        self.BoxUsername.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.BoxUsername.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BoxUsername.setObjectName("BoxUsername")
        self.lineEdit = QtWidgets.QLineEdit(self.BoxUsername)
        self.lineEdit.setGeometry(QtCore.QRect(40, 0, 181, 31))
        self.lineEdit.setStyleSheet("border-color: rgb(209, 209, 209);")
        self.lineEdit.setInputMask("")
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(self.BoxUsername)
        self.label_3.setGeometry(QtCore.QRect(0, 0, 41, 31))
        self.label_3.setObjectName("label_3")
        self.BoxPassword = QtWidgets.QFrame(self.ContainerConfig)
        self.BoxPassword.setGeometry(QtCore.QRect(10, 210, 221, 31))
        self.BoxPassword.setStyleSheet("border:1px solid rgb(209, 209, 209);")
        self.BoxPassword.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.BoxPassword.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BoxPassword.setObjectName("BoxPassword")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.BoxPassword)
        self.lineEdit_2.setGeometry(QtCore.QRect(40, 0, 181, 31))
        self.lineEdit_2.setStyleSheet("border-color: rgb(209, 209, 209);")
        self.lineEdit_2.setInputMask("")
        self.lineEdit_2.setClearButtonEnabled(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_4 = QtWidgets.QLabel(self.BoxPassword)
        self.label_4.setGeometry(QtCore.QRect(0, 0, 41, 31))
        self.label_4.setObjectName("label_4")
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
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 119, 29))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.label_11 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_11.setGeometry(QtCore.QRect(0, 0, 121, 31))
        self.label_11.setToolTipDuration(7)
        self.label_11.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_11.setTextFormat(QtCore.Qt.RichText)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")

        self.selecionar_materia = QtWidgets.QComboBox(self.ContainerConfig)
        self.selecionar_materia.setGeometry(QtCore.QRect(10, 340, 221, 31))
        self.selecionar_materia.setObjectName("selecionar_materia")
        # Definir o texto padrão para o item zero
        self.selecionar_materia.addItem("Escolha a Materia...")
        # Desabilitar o item zero
        self.selecionar_materia.setItemData(0, False)
        
        
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
        self.label_7.setAlignment(Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(270, 80, 351, 371))
        self.tabWidget.setObjectName("tabWidget")
        self.Navegador = QtWidgets.QWidget()
        self.Navegador.setObjectName("Navegador")
        self.ContainerWebEngine = QtWidgets.QFrame(self.Navegador)
        # self.ContainerWebEngine.setEnabled(False)
        self.ContainerWebEngine.setGeometry(QtCore.QRect(-10, -10, 361, 471))
        self.ContainerWebEngine.setStyleSheet("background-color: rgb(255, 255, 127);\n"
"")
        self.ContainerWebEngine.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ContainerWebEngine.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ContainerWebEngine.setObjectName("ContainerWebEngine")
        self.label = QtWidgets.QLabel(self.ContainerWebEngine)
        self.label.setGeometry(QtCore.QRect(-260, -60, 651, 561))
        self.label.setMinimumSize(QtCore.QSize(651, 0))
        self.label.setObjectName("label")
        self.tabWidget.addTab(self.Navegador, "")
        self.Deploy = QtWidgets.QWidget()
        self.Deploy.setObjectName("Deploy")
        self.ContainerWebEngine_2 = QtWidgets.QFrame(self.Deploy)
        # self.ContainerWebEngine_2.setEnabled(False)
        self.ContainerWebEngine_2.setGeometry(QtCore.QRect(0, 0, 361, 471))
        self.ContainerWebEngine_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.ContainerWebEngine_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ContainerWebEngine_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ContainerWebEngine_2.setObjectName("ContainerWebEngine_2")
        self.label_9 = QtWidgets.QLabel(self.ContainerWebEngine_2)
        self.label_9.setGeometry(QtCore.QRect(10, 10, 81, 16))
        self.label_9.setObjectName("label_9")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.ContainerWebEngine_2)
        # self.scrollArea_2.setEnabled(False)
        self.scrollArea_2.setGeometry(QtCore.QRect(10, 40, 321, 261))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 319, 259))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.label_10 = QtWidgets.QLabel(self.ContainerWebEngine_2)
        self.label_10.setGeometry(QtCore.QRect(10, 390, 81, 16))
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        self.config_2 = QtWidgets.QPushButton(self.ContainerWebEngine_2)
        self.config_2.setGeometry(QtCore.QRect(10, 310, 131, 31))
        self.config_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.config_2.setStyleSheet("background-color: rgb(255, 99, 99);\n"
"border-radius:2px;\n"
"color: rgb(0, 0, 0);\n"
"QPushButton::hover {\n"
"    background-color: rgb(74, 101, 255);\n"
"}\n"
"")
        self.config_2.setObjectName("config_2")
        self.tabWidget.addTab(self.Deploy, "")
        self.Connection = QtWidgets.QWidget()
        self.Connection.setObjectName("Connection")
        self.ContainerWebEngine_3 = QtWidgets.QFrame(self.Connection)
        self.ContainerWebEngine_3.setGeometry(QtCore.QRect(0, 0, 361, 471))
        self.ContainerWebEngine_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.ContainerWebEngine_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ContainerWebEngine_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ContainerWebEngine_3.setObjectName("ContainerWebEngine_3")
        self.label_17 = QtWidgets.QLabel(self.ContainerWebEngine_3)
        self.label_17.setGeometry(QtCore.QRect(10, 10, 141, 16))
        self.label_17.setObjectName("label_17")
        self.scrollArea_5 = QtWidgets.QScrollArea(self.ContainerWebEngine_3)
        self.scrollArea_5.setGeometry(QtCore.QRect(10, 40, 321, 261))
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollArea_5.setObjectName("scrollArea_5")
        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(0, 0, 319, 259))
        self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")
        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_5)
        self.label_18 = QtWidgets.QLabel(self.ContainerWebEngine_3)
        self.label_18.setGeometry(QtCore.QRect(10, 390, 81, 16))
        self.label_18.setText("")
        self.label_18.setObjectName("label_18")
        self.config_4 = QtWidgets.QPushButton(self.ContainerWebEngine_3)
        self.config_4.setGeometry(QtCore.QRect(10, 310, 321, 31))
        self.config_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.config_4.setStyleSheet("background-color: rgb(85, 255, 127);\n"
"border-radius:2px;\n"
"color: rgb(0, 0, 0);\n"
"QPushButton::hover {\n"
"    background-color: rgb(74, 101, 255);\n"
"}\n"
"")
        self.config_4.setObjectName("config_4")
        self.tabWidget.addTab(self.Connection, "")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 460, 251, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(270, 460, 351, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(280, 10, 71, 16))
        self.label_12.setObjectName("label_12")
        self.scrollArea_3 = QtWidgets.QScrollArea(Dialog)
        self.scrollArea_3.setGeometry(QtCore.QRect(280, 30, 331, 41))
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 329, 39))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
        self.label_13 = QtWidgets.QLabel(Dialog)
        self.label_13.setGeometry(QtCore.QRect(350, 10, 121, 16))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(Dialog)
        self.label_14.setGeometry(QtCore.QRect(480, 10, 71, 16))
        self.label_14.setObjectName("label_14")

        self.retranslateUi(Dialog)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Logo.setText(_translate("Dialog", "<html><head/><body><p><img width=200 src='./App/Assets/Logo.png'/></p></body></html>"))
        self.lineEdit.setText(_translate("Dialog", "Usuário Ava ..."))
        self.label_3.setText(_translate("Dialog", "<html><head/><body><p><img src='./App/Assets/User.png'/></p></body></html>"))
        self.lineEdit_2.setText(_translate("Dialog", "Senha Ava ..."))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p><img src='./App/Assets/Pass.png'/></p></body></html>"))
        self.buscar_materia.setText(_translate("Dialog", "Buscar Materia"))
        
                
      
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
                                        self.lineEdit.setText(tupla[1])  # Set username
                                        self.lineEdit_2.setText(tupla[2])  # Set password
                                
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
        

        self.config.setText("configuração")
        self.iniciar.setText(_translate("Dialog", "Iniciar Transmissão"))
        self.label_7.setText(_translate("Dialog", "Escolher Materia"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p><img src=\":/Fundo/FundoPrototipo.png\"/></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Navegador), _translate("Dialog", "Downloads"))
        # Chamar setCurrentIndex com o índice da aba desejada (por exemplo, 1)
        self.tabWidget.setCurrentIndex(0)
        self.label_9.setText(_translate("Dialog", "Sockets Emitter"))
        self.config_2.setText(_translate("Dialog", "Limpar Logs"))
        
         #Evento para Limpar Logs
        self.config_2.clicked.connect(self.limpar_logs)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Deploy), _translate("Dialog", "Sockets"))
        
        #Evento para Atualizar o emitter Socket
        self.tabWidget.currentChanged.connect(self.on_tab_changed)
        
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Deploy), _translate("Dialog", "Sockets"))
        self.label_17.setText(_translate("Dialog", "Sockets Connections Events"))
        self.config_4.setText(_translate("Dialog", "Relate Erros"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Connection), _translate("Dialog", "Conexao"))
        self.pushButton.setText(_translate("Dialog", "Contribuir no Projeto"))
        self.pushButton_2.setText(_translate("Dialog", "Doe para o Criador"))
        self.label_12.setText(_translate("Dialog", "CRF GERADO"))
        self.label_13.setText(_translate("Dialog", "| AGENT AUTENTICADOR"))
        self.label_14.setText(_translate("Dialog", "| IP GERADO"))
        
        # Conectando o botão ao método on_click
        self.buscar_materia.clicked.connect(self.abrir_Janela_Busca)
        self.config.clicked.connect(self.abrir_Janela_config)     
        self.iniciar.clicked.connect(self.Buscar_Livros_Ava_Open)

    def abrir_Janela_Busca(self):
        # Esta função cria uma nova janela e mantém uma referência a ela
        self.janela_de_busca = Janela_Busca()
        self.janela_de_busca.show()

    def Buscar_Livros_Ava_Open(self):
        
        # print(self.lineEdit.text())
        # print(self.lineEdit_2.text())
        # QMessageBox.information(None, 'Sucesso', 'Busca Realizada Com Sucesso , Enviando Pacote <SKC4>')
        
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        materia  = self.selecionar_materia.currentText()

        if username == "Usuário Ava ..." or password == "Senha Ava ..." or  materia == "Escolha a Materia...":
                QMessageBox.critical(None, 'Campo Invalido', 'Erro Campos Vazios...')
        else:
                if username == "" or password == "" or  materia == "":
                        QMessageBox.critical(None, 'Campo Invalido', 'Erro Campos Vazios...')
                else:
                        Janela_livro = Janela_Busca_livro(Dialog,username,password,materia)
                        Janela_livro.exec_()
                        
        #Cria o QLabel para exibir a mensagem de logs limpos
        self.labelLogs = QtWidgets.QLabel(self.ContainerWebEngine_2)
        self.labelLogs.setGeometry(QtCore.QRect(180, 320, 200, 20))  # Defina a geometria adequada para o seu QLabel
        self.labelLogs.hide()  # Oculta o QLabel inicialmente
        
    def limpar_logs(self):
        # Implemente aqui a lógica para limpar os logs
        limpar_arquivo_log('./App/Logs/webdriver.log')
        # self.labelLogs.setText("Logs Limpos com Sucesso")
        # self.labelLogs.show()
        
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
                self.MonitorLogs = janelaMonitor(False,321, 331,1000)  # Passe True para habilitarLogs para atualizar o log a cada segundo
                        # print(MonitorLogs)
                self.scrollArea_2.setWidget(self.MonitorLogs)  


        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)  
    Dialog.show() 
    sys.exit(app.exec_())  
