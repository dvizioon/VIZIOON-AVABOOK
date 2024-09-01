import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer
import time
# Função para criar e exibir a janela principal
def Janela_Codigo():
    # Função para salvar o texto em um arquivo
    def salvar_texto():
        texto = texto_editado.toPlainText()
        with open('./App/Config/.Conf', 'w') as arquivo:
            arquivo.write(texto)
            QMessageBox.information(janela_principal, 'Edição', 'Sucesso...')

    # Função para carregar o texto de um arquivo de configuração
    def carregar_texto():
        try:
            with open('./App/Config/.Conf', 'r') as arquivo:
                texto = arquivo.read()
                texto_editado.setPlainText(texto)
        except FileNotFoundError:
            QMessageBox.warning(janela_principal, 'Aviso', 'Nenhum texto salvo encontrado.')
            
    def restauraConfig():
        try:
            with open('./App/Config/.Conf', 'w') as arquivo:
                texto = """#=========== Configuracão Servidor =============#
host_servidor = localhost
porta_servidor = 5000
rota_oringi = ["/dadosMateria"]
time_emisao_pacotes = 5
time_requisao_pacotes = 7
                """
                arquivo.write(texto)
                QMessageBox.warning(janela_principal, 'Aviso', 'Sucesso Conf.dll Restaurado...')
                janela_principal.close()
        except FileNotFoundError:
            QMessageBox.warning(janela_principal, 'Aviso', 'Nenhum texto salvo encontrado.')
            

    janela_principal = QWidget()
    janela_principal.setWindowTitle('Configuração')
    janela_principal.setFixedWidth(400)
    janela_principal.setFixedHeight(300)

    layout_principal = QVBoxLayout()

    texto_editado = QTextEdit()
    layout_principal.addWidget(texto_editado)

    layout_botoes = QVBoxLayout()
    btn_salvar = QPushButton('Salvar')
    btn_salvar.setStyleSheet("""
        QPushButton {
            width: 100px;
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 0px;
            font-size: 16px;
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
    """)
    btn_salvar.clicked.connect(salvar_texto)
    layout_botoes.addWidget(btn_salvar)

    btn_carregar = QPushButton('Restaurar Configurações')
    btn_carregar.setStyleSheet("""
        QPushButton {
            width: 100px;
            background-color: rgb(74, 101, 255);
            color: white;
            border: none;
            padding: 10px 0px;
            font-size: 16px;
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: rgb(74, 90, 255);
        }
    """)
    
    btn_carregar.clicked.connect(restauraConfig)
    layout_botoes.addWidget(btn_carregar)

    layout_principal.addLayout(layout_botoes)

    janela_principal.setLayout(layout_principal)
    
    # Carregar o texto do arquivo .conf quando a janela é exibida
    carregar_texto()
    
    janela_principal.show()

    return janela_principal

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     Janela_Codigo()
#     sys.exit(app.exec_())
