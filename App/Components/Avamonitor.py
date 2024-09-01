from PyQt5 import QtWidgets, QtCore

def janelaMonitor(habilitarLogs,width,height,Time):
    class MinhaJanela(QtWidgets.QMainWindow):
        def __init__(self):
            super().__init__()

            self.setWindowTitle("Visualizador de Log")  # Define o título da janela
                
            # Definindo a largura e a altura da janela
            self.setFixedWidth(width)  # Substitua 800 pela largura desejada
            self.setFixedHeight(height)  # Substitua 600 pela altura desejada

            # Cria um QScrollArea e configurações
            self.scroll_area = QtWidgets.QScrollArea(self)
            self.scroll_area.setGeometry(0, 0, width, height)  # Tamanho da área de rolagem
            self.scroll_area.setWidgetResizable(True)  # Permite redimensionamento do widget dentro da área de rolagem

            # Oculta as barras de rolagem vertical e horizontal
            self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

            # Cria um QWidget para adicionar ao QScrollArea
            self.scroll_area_widget = QtWidgets.QWidget()
            self.scroll_area.setWidget(self.scroll_area_widget)

            # Define um layout para o QWidget dentro do QScrollArea
            self.scroll_area_layout = QtWidgets.QVBoxLayout(self.scroll_area_widget)

            # Cria um QTimer para atualizar o log a cada segundo se habilitarLogs for True
            if habilitarLogs:
                self.timer = QtCore.QTimer(self)
                self.timer.timeout.connect(self.monitorar_log)
                self.timer.start(Time)  # Atualiza a cada segundo
            else:
                self.monitorar_log()

        def monitorar_log(self):
            caminho_arquivo = './App/Logs/webdriver.log'
            try:
                with open(caminho_arquivo, 'r') as f:
                    linhas = f.readlines()

                for linha in linhas:
                    label = QtWidgets.QLabel(linha.strip(), self.scroll_area_widget)  # Cria o QLabel diretamente no widget
                    self.scroll_area_layout.addWidget(label)  # Adiciona o QLabel ao layout do widget
            except FileNotFoundError:
                print("Arquivo de log não encontrado")

    return MinhaJanela()

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     janela = janelaMonitor(False,300, 200,1000)  # Passe True para habilitarLogs para atualizar o log a cada segundo
#     janela.show()
#     sys.exit(app.exec_())
