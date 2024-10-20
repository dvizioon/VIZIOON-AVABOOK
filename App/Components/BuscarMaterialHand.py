from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import sqlite3
import time
import logging
import os
from fake_useragent import UserAgent

from Modules.LimparLogs import limpar_arquivo_log

#limpar Logs Antes de Registrar os novos
limpar_arquivo_log('./App/Logs/webdriver.log')
#Verifica se a pasta 'Logs' existe no diretório 'App'

if not os.path.exists('./App/Logs'):
    # Cria a pasta 'Logs' se não existir
    os.makedirs('./App/Logs')

# Configuração do logging para redirecionar os logs para um arquivo
logging.basicConfig(filename='./App/Logs/webdriver.log', level=logging.DEBUG)

# Conecta ao banco de dados
conn = sqlite3.connect('./Database/avaBook.db')
c = conn.cursor()

# import requests

def BuscarLivroHand(usuario,senha):
    
    def get_random_user_agent():
        ua = UserAgent()
        return ua.random


    random_user_agent = get_random_user_agent()
    print("User-Agent Aleatório:", random_user_agent)

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # # Configura o User-Agent nas opções do Chrome

    chrome_options.add_argument(f"user-agent={random_user_agent}")
    chrome_options.binary_location = "124.0.6367.91\chrome.exe"
    service = Service(options=chrome_options,executable_path='./chromedriver/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(1920, 1080)
    # driver.maximize_window()


    # Navegação até a URL especificada
    driver.get("https://www.colaboraread.com.br")
    
    try:
        # Aguarda até que o elemento seja carregado na página
        
        username = usuario
        password = senha
        
        nome   = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        senha  = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
        submit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='loginForm']/button")))
        
        time.sleep(2)
        
        # ==========================================#
        print(f"Elemento Nome Encontrado => {nome}")
        print(f"Elemento Senha Encontrado => {senha}")
        print(f"Elemento Submit Encontrado => {submit}")
        # ==========================================#
        
        
        nome.send_keys(username)
        senha.send_keys(password)
        submit.click()
        
        time.sleep(3)
        
        buttonEntrarMaterias = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,"//*[@id='navbar-content-aluno-cursos']/div/div[1]/div/div[3]/form/div[2]/button")))
        buttonEntrarMaterias.click()
        
        # ==========================================#
        print(f"Elemento Butão Send Encontrado => {nome}")
        # ==========================================#
        
        time.sleep(2)
        
        # Aguarda até que o elemento ul seja carregado na página
        Materias = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#navbar-content-aluno-pda > ul")))

        # Encontra todas as li dentro do ul
        lis = Materias.find_elements(By.TAG_NAME, 'li')
        
        # ==========================================#
        print(f"Elemento Nome Encontrado => {nome}")
        print(f"Elemento Senha Encontrado => {senha}")
        print(f"Elemento Submit Encontrado => {submit}")
        # ==========================================#

        def recriar_tabela():
            # Executa a instrução SQL para excluir a tabela se ela existir
            c.execute("DROP TABLE IF EXISTS materias")
            
            # Executa a instrução SQL para criar a nova tabela
            c.execute("""
                CREATE TABLE materias (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL
                );
            """)
            # Salva as alterações
            conn.commit()

        recriar_tabela()

        # Lista para armazenar as matérias encontradas
        materias_encontradas = []
         
        # Para cada li, faz algo
        for li in lis:
            # Divide a string em duas partes: nome da matéria e data
            materia, _, _ = li.text.partition('\n')
            # Agora 'materia' contém apenas o nome da matéria
            # print(materia)
            
            # Adiciona a matéria à lista de matérias encontradas
            materias_encontradas.append(materia)
            
             # Executa a instrução SQL para limpar a tabela

            # Verifica se o nome já existe no banco de dados
            c.execute("SELECT * FROM materias WHERE nome = ?", (materia,))
            data = c.fetchone()

            # Se 'data' for None, o nome não existe no banco de dados e pode ser inserido
            if data is None:
                c.execute("INSERT INTO materias (nome) VALUES (?)", (materia,))
                # Salva as alterações
                conn.commit()
        
        loading = False
        # Retorna a lista de matérias encontradas
        driver.quit()
        return materias_encontradas , loading 

        
    except TimeoutException:
        print("O elemento não foi encontrado na página dentro do tempo limite.")
        
        loading = False
        materias_encontradas = False
        driver.quit()
        return materias_encontradas , loading 
    finally:
        # Fecha a conexão com o banco de dados
        conn.close()

# BuscarLivroHand("","")