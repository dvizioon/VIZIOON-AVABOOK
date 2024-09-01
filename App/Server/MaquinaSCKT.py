from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
import threading
import time
import sqlite3
import re
import os

app = Flask(__name__)
socketio = SocketIO(app)

def extrair_valores_conf(nome_arquivo):
    with open(nome_arquivo, 'r') as file:
        linhas = file.readlines()  # Lê todas as linhas do arquivo
        for linha in linhas:
            if linha.startswith('host_servidor'):
                host_servidor = linha.split('=')[1].strip()  # Extrai o valor após o '='
            elif linha.startswith('porta_servidor'):
                porta_servidor = int(linha.split('=')[1].strip())  # Extrai o valor após o '=' e converte para inteiro
            elif linha.startswith('time_emisao_pacotes'):
                time_emisao_pacotes = int(linha.split('=')[1].strip()) 
            elif linha.startswith('rota_oringi'):
                valor_path = linha.split('=')[1].strip()  # Extrai o valor após o '='
                rota_oringi = re.sub(r'["\[\]]', '', valor_path)
            elif linha.startswith('rota_user'):
                valor_path = linha.split('=')[1].strip()  # Extrai o valor após o '='
                rota_user = re.sub(r'["\[\]]', '', valor_path)
    return host_servidor, porta_servidor,rota_oringi,time_emisao_pacotes,rota_user

# Caminho para o arquivo .Conf
caminho_arquivo = './App/Config/.Conf'

# Extraindo o host e a porta do servidor
host_servidor, porta_servidor , rota_oringi, time_emisao_pacotes,rota_user = extrair_valores_conf(caminho_arquivo)

# Exibindo o host e a porta do servidor
# print("Host do servidor:", host_servidor)
# print("Porta do servidor:", porta_servidor)


# Função para obter os dados da tabela 'materias' do banco de dados SQLite
def obter_dados_materia():
    conn = sqlite3.connect('./Database/avaBook.db')
    c = conn.cursor()
    c.execute("SELECT * FROM materias")
    dados = c.fetchall()
    conn.close()
    return dados

def obter_dados_user():
    conn = sqlite3.connect('./Database/avaBook.db')
    c = conn.cursor()
    c.execute("SELECT * FROM usuario")
    dados = c.fetchall()
    conn.close()
    return dados

# Rota para retornar os dados da tabela 'materias'
@app.route(f'{rota_oringi}')
def dados_materia():
    dados = obter_dados_materia()
    return jsonify(dados)

# Rota para retornar os dados da tabela 'usuarios'
@app.route(f'{rota_user}')
def dados_user():
    dados = obter_dados_user()
    return jsonify(dados)


# Função para emitir os dados atualizados para os clientes conectados via SocketIO
def emitir_dados_atualizados():
    while True:
        # Obter os dados mais recentes da tabela 'materias'
        dados_materia = obter_dados_materia()
        dados_usuario = obter_dados_user()
        # Emitir os dados atualizados para os clientes conectados via SocketIO
        socketio.emit('dados_atualizados', dados_materia)
        socketio.emit('dados_atualizados', dados_user)
        # Esperar um intervalo de tempo antes de atualizar novamente
        time.sleep(time_emisao_pacotes)  # 5 segundos

def iniciarServidorFlask():
    from waitress import serve
    serve(app, host=host_servidor, port=porta_servidor)
    
def iniciarMaquina(service):
    if service == "Start":
        # Iniciar a thread para emitir os dados atualizados
        terminal_0 = threading.Thread(target=emitir_dados_atualizados)
        terminal_0.daemon = True
        terminal_0.start()
        # Iniciar o servidor Flask em uma thread separada
        servidor_thread = threading.Thread(target=iniciarServidorFlask)
        servidor_thread.daemon = True
        servidor_thread.start()
    elif service == "Stop":
        pass


    
