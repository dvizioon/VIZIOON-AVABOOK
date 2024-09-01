from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QFrame, QScrollArea
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

def CriarWebEngine(url):
    # Criação da QFrame
    frame = QFrame()
    
    # Definição do layout QVBoxLayout para o QFrame
    layout = QVBoxLayout()
    frame.setLayout(layout)

    # Criação da QWebEngineView
    web_view = QWebEngineView()
    web_view.load(QUrl(url))

    # Adiciona a QWebEngineView ao layout
    layout.addWidget(web_view)

    # Criação da QScrollArea com tamanho fixo
    scroll_area = QScrollArea()
    scroll_area.setFixedSize(342, 500)
    scroll_area.setWidget(frame)
    scroll_area.setWidgetResizable(True)  # Para permitir o redimensionamento do conteúdo

    print("Web Engine Criada Com Sucesso")

    return scroll_area

# # Exemplo de uso:
# app = QApplication([])
# window = QWidget()
# window.setGeometry(100, 100, 250, 250)  # Definindo a geometria da janela principal
# layout = QVBoxLayout(window)
# web_engine_scroll_area = CriarWebEngine("https://www.google.com")
# layout.addWidget(web_engine_scroll_area)
# window.show()
# app.exec_()
