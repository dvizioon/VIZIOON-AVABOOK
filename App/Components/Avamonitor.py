from PyQt5 import QtWidgets, QtCore
import os

class LogMonitorWindow(QtWidgets.QWidget):
    def __init__(self, habilitar_logs, update_interval):
        super().__init__()

        # Layout onde os logs serão adicionados
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.layout)

        # Verifica se logs estão habilitados
        if habilitar_logs:
            # Configura o QTimer para atualizar os logs periodicamente
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.update_log)
            self.timer.start(update_interval)
        else:
            self.limpar_logs()  # Limpa os logs quando desabilitado
            self.mostrar_mensagem_desabilitado()  # Mostra a mensagem que logs estão desativados

    def update_log(self):
        caminho_arquivo = './App/Logs/webdriver.log'
        try:
            with open(caminho_arquivo, 'r') as f:
                linhas = f.readlines()

            # Limpa o layout atual antes de adicionar novas linhas
            for i in reversed(range(self.layout.count())):
                widget = self.layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()

            # Se o arquivo estiver vazio, exibe uma mensagem de "Nenhum log disponível"
            if not linhas:
                label = QtWidgets.QLabel("Nenhum log disponível")
                label.setAlignment(QtCore.Qt.AlignCenter)  # Centraliza o texto
                self.layout.addWidget(label)
            else:
                # Adiciona cada linha do log como um QLabel no layout
                for linha in linhas:
                    label = QtWidgets.QLabel(linha.strip())
                    self.layout.addWidget(label)
                    
        except FileNotFoundError:
            print("Arquivo de log não encontrado")
            # Limpa o layout se o arquivo não for encontrado
            for i in reversed(range(self.layout.count())):
                widget = self.layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()

            # Exibe uma mensagem de erro
            label = QtWidgets.QLabel("Arquivo de log não encontrado")
            label.setAlignment(QtCore.Qt.AlignCenter)  # Centraliza o texto
            self.layout.addWidget(label)

    def limpar_logs(self):
        """Função que limpa o conteúdo do arquivo de log."""
        caminho_arquivo = './App/Logs/webdriver.log'
        try:
            with open(caminho_arquivo, 'w') as f:
                f.write('')  # Escreve um arquivo vazio para limpar os logs
        except FileNotFoundError:
            print("Arquivo de log não encontrado para limpar")

    def mostrar_mensagem_desabilitado(self):
        """Exibe uma mensagem informando que os logs estão desabilitados."""
        # Limpa o layout atual
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Adiciona uma QLabel com a mensagem e centraliza o texto
        label = QtWidgets.QLabel("Habilite os logs para visualizar.")
        label.setAlignment(QtCore.Qt.AlignCenter)  # Centraliza o texto
        self.layout.addWidget(label)

def janela_monitor(habilitar_logs, update_interval):
    return LogMonitorWindow(habilitar_logs, update_interval)

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     janela = janela_monitor(False, 1000)  # Passe True para habilitar_logs para atualizar o log a cada segundo
#     janela.show()
#     sys.exit(app.exec_())
