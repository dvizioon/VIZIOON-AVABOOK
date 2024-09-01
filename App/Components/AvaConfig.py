import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame, QDialog, QCheckBox, QMessageBox
import os
from Components.AvaEditor import Janela_Codigo

janela = None
# Função para obter as tabelas do banco de dados
def obter_tabelas_do_banco():
    conn = sqlite3.connect('./Database/avaBook.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = [tupla[0] for tupla in c.fetchall()]
    conn.close()
    return tabelas

class DialogResetBanco(QDialog):
    def __init__(self, tabelas):
        super(DialogResetBanco, self).__init__()
        self.setWindowTitle("Resetar Banco")
        self.setFixedSize(300, 270)

        layout = QVBoxLayout()

        label_instrucao = QLabel("Selecione as tabelas para resetar do AvaBook:")
        layout.addWidget(label_instrucao)

        self.checkboxes = []

        for tabela in tabelas:
            checkbox = QCheckBox(tabela)
            layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        btn_confirmar = QPushButton("Confirmar")
        btn_confirmar.clicked.connect(self.confirmar_reset_banco)
        btn_confirmar.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Cor de fundo */
                color: white; /* Cor do texto */
                border: none; /* Sem borda */
                padding: 10px 20px; /* Preenchimento interno */
                font-size: 16px; /* Tamanho da fonte */
                border-radius: 5px; /* Borda arredondada */
            }
            QPushButton:hover {
                background-color: #45a049; /* Cor de fundo ao passar o mouse */
            }
        """)
        layout.addWidget(btn_confirmar)

        self.setLayout(layout)

    # Método para confirmar o reset do banco de dados
    # def confirmar_reset_banco(self):
    #     tabelas_selecionadas = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
    #     print("Tabelas selecionadas para resetar:", tabelas_selecionadas)
        
    #     # Conecta ao banco de dados
    #     conn = sqlite3.connect('./Database/avaBook.db')
    #     c = conn.cursor()
        
    #     # Executa o drop table para cada tabela selecionada
    #     for tabela in tabelas_selecionadas:
    #         c.execute(f"DROP TABLE IF EXISTS {tabela};")
        
    #     # Commit e fecha a conexão
    #     conn.commit()
    #     conn.close()
        
    #     # Exibir mensagem de confirmação
    #     QMessageBox.information(self, "Reset do Banco", "Tabelas resetadas pelo usuário.")
        
    #     # Atualizar a janela após o reset do banco
    #     atualizar_janela()
        
    #     self.accept()
    
    def confirmar_reset_banco(self):
        tabelas_selecionadas = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
        print("Tabelas selecionadas para resetar:", tabelas_selecionadas)
        
        # Conecta ao banco de dados
        conn = sqlite3.connect('./Database/avaBook.db')
        c = conn.cursor()
        
        # Executa DELETE FROM para cada tabela selecionada
        for tabela in tabelas_selecionadas:
            c.execute(f"DELETE FROM {tabela};")
        
        # Commit e fecha a conexão
        conn.commit()
        conn.close()
        
        # Exibir mensagem de confirmação
        QMessageBox.information(self, "Reset do Banco", "Valores das tabelas resetados pelo usuário.")
        
        # Atualizar a janela após o reset do banco
        self.accept()
        # atualizar_janela()
        self.close() 

def atualizar_janela():
    global janela  # Indicar que janela é global
    if janela is not None:
        janela.close()  # Fechar a janela existente
    janela = Janela_Config()  # Criar uma nova instância da janela
    janela.show()  # Exibir a janela

# Função para abrir o diálogo de reset do banco de dados
def open_dialog_reset_banco(tabelas):
    dialog_reset_banco = DialogResetBanco(tabelas)
    dialog_reset_banco.exec_()
    
    
# Função para criar o banco de dados e as tabelas
def criar_banco():
    # Verifica se a pasta 'Database' existe, se não, cria a pasta
    if not os.path.exists('Database'):
        os.makedirs('Database')

    # Conectando ao banco de dados na pasta 'Database'
    conn = sqlite3.connect(os.path.join('Database', 'avaBook.db'))
    print("Banco de dados 'avaBook' criado com sucesso na pasta 'Database'.")

    # Criando um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Criando a tabela 'usuario'
    cursor.execute("""
    CREATE TABLE usuario (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        senha TEXT NOT NULL
    );
    """)
    
    # Criando a tabela 'materias'
    cursor.execute("""
    CREATE TABLE materias (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    );
    """)
    
    cursor.execute("""
    CREATE TABLE agents (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        agente TEXT NOT NULL
    );
    """)
    
    cursor.execute("""
    CREATE TABLE livro (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        caminho_fragmentado TEXT NOT NULL,
        caminho_comprimido TEXT NOT NULL
    );
    """)
    
    print("Tabela 'usuario' criada com sucesso.")
    print("Tabela 'materias' criada com sucesso.")
    print("Tabela 'agents' criada com sucesso.")
    print("Tabela 'livros' criada com sucesso.")

    # Fechando a conexão com o banco de dados
    conn.close()

def apagar_tabelas():
    conn = sqlite3.connect('./Database/avaBook.db')
    c = conn.cursor()
    
    # Seleciona todas as tabelas do banco de dados, excluindo a tabela sqlite_sequence
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name!='sqlite_sequence';")
    tabelas = [tupla[0] for tupla in c.fetchall()]
    
    # Apaga cada tabela encontrada
    for tabela in tabelas:
        c.execute(f"DROP TABLE IF EXISTS {tabela};")
    
    conn.commit()
    conn.close()

    
# Classe para o diálogo de reset da aplicação
class DialogResetarApp(QDialog):
    def __init__(self):
        super(DialogResetarApp, self).__init__()
        self.setWindowTitle("Resetar Aplicação")
        self.setFixedSize(300, 270)

        layout = QVBoxLayout()

        label_instrucao = QLabel("Tem certeza que deseja resetar a aplicação AvaBook?")
        layout.addWidget(label_instrucao)

        btn_confirmar = QPushButton("Sim")
        btn_confirmar.clicked.connect(self.confirmar_reset_app)
        btn_confirmar.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Cor de fundo */
                color: white; /* Cor do texto */
                border: none; /* Sem borda */
                padding: 10px 20px; /* Preenchimento interno */
                font-size: 16px; /* Tamanho da fonte */
                border-radius: 5px; /* Borda arredondada */
            }
            QPushButton:hover {
                background-color: #45a049; /* Cor de fundo ao passar o mouse */
            }
        """)
        layout.addWidget(btn_confirmar)

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.close)
        btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #f44336; /* Cor de fundo */
                color: white; /* Cor do texto */
                border: none; /* Sem borda */
                padding: 10px 20px; /* Preenchimento interno */
                font-size: 16px; /* Tamanho da fonte */
                border-radius: 5px; /* Borda arredondada */
            }
            QPushButton:hover {
                background-color: #d32f2f; /* Cor de fundo ao passar o mouse */
            }
        """)
        layout.addWidget(btn_cancelar)

        self.setLayout(layout)

    # Método para confirmar o reset da aplicação
    def confirmar_reset_app(self):
        # Apaga todas as tabelas do banco de dados
        apagar_tabelas()
        
        # Cria novamente o banco de dados e tabelas
        criar_banco()
        
        # Exibe mensagem de confirmação
        QMessageBox.information(self, "Reset da Aplicação", "Aplicação resetada com sucesso.")
        
        # atualizar_janela()
        # Fecha o diálogo
        self.accept()
        self.close() 

def abriModoEditor():
    Janela = Janela_Codigo()
    Janela.show()
 
def open_dialog_reset_app():
    dialog_reset_app= DialogResetarApp()
    dialog_reset_app.exec_()
    
# Função para criar e exibir a janela principal
def Janela_Config():
    tabelas = obter_tabelas_do_banco()

    janela_principal = QWidget()
    janela_principal.setWindowTitle('Configuração')
    janela_principal.setFixedWidth(300)
    janela_principal.setFixedHeight(220)

    layout = QVBoxLayout()

    # Frame para os botões
    frame_botoes = QFrame()
    frame_botoes_layout = QVBoxLayout()
    
    label_info = QLabel("Painel de Configurações")
    label_info.setStyleSheet("""
        QLabel {
            color: #333;
            font-size: 18px; 
            font-weight: bold;
            padding-bottom: 5px;
            border-bottom: 2px solid #333; 
            text-align: center; /* Centraliza o texto */
        }
    """)


    # Botão para resetar o banco
    btn_reset_banco = QPushButton("Resetar Banco")
    btn_reset_banco.setObjectName("reset_banco")
    btn_reset_banco.setStyleSheet("""
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

    # Botão para resetar a aplicação
    btn_reset_aplicacao = QPushButton("Resetar Aplicação")
    btn_reset_aplicacao.setObjectName("reset_aplicacao")
    btn_reset_aplicacao.setStyleSheet("""
        QPushButton {
            width: 100px;
            background-color: #f44336;
            color: white;
            border: none;
            padding: 10px 0px;
            font-size: 16px;
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: #d32f2f;
        }
    """)
    
    btn_config_aplicacao = QPushButton("Configurar App")
    btn_config_aplicacao.setObjectName("config_app")
    btn_config_aplicacao.setStyleSheet("""
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
    
    btn_reset_banco.clicked.connect(lambda: open_dialog_reset_banco(tabelas))
    btn_reset_aplicacao.clicked.connect(lambda: open_dialog_reset_app())
    btn_config_aplicacao.clicked.connect(lambda:abriModoEditor())
    
    
    frame_botoes_layout.addWidget(label_info)
    frame_botoes_layout.addWidget(btn_reset_banco)
    frame_botoes_layout.addWidget(btn_reset_aplicacao)
    frame_botoes_layout.addWidget(btn_config_aplicacao)  # Adicionado por último

    frame_botoes.setLayout(frame_botoes_layout)


    # Frame para informações do desenvolvedor
    frame_info_dev = QFrame()
    # frame_info_dev_layout = QVBoxLayout()

    # # Campo de informações
    # label_info = QLabel("Contato do desenvolvedor: contact@example.com")
    # frame_info_dev_layout.addWidget(label_info)

    # frame_info_dev.setLayout(frame_info_dev_layout)

    layout.addWidget(frame_botoes)
    layout.addWidget(frame_info_dev)

    janela_principal.setLayout(layout)
    janela_principal.show()

    return janela_principal

# Inicialização da aplicação

# app = QApplication([])
# janela = Janela_Config()
# app.exec_()
