import os

def limpar_arquivo_log(caminho_arquivo):
    try:
        # Abre o arquivo no modo de escrita, o que automaticamente limpa o arquivo
        with open(caminho_arquivo, 'w'):
            print(f"Arquivo {caminho_arquivo} foi limpo com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao limpar o arquivo: {e}")

# Uso da função
# caminho_arquivo = './App/Logs/webdriver.log'
# limpar_arquivo_log(caminho_arquivo)
