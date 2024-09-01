from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QScrollArea, QLabel, QWidget, QFrame, QHBoxLayout,QMessageBox
from PyQt5.QtGui import QFont, QColor, QPainter
from PyQt5.QtCore import Qt, QTimer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse, parse_qs
import re
from bs4 import BeautifulSoup
import requests
import random
from selenium.webdriver.common.action_chains import ActionChains
import uuid
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
import pickle
from datetime import datetime

app = QApplication([])

def DowloadBook(nome_materia,url,Dialog,url_origin):
    chrome_options = Options()

    chrome_options.binary_location = "./124.0.6367.91/chrome.exe"
    service = Service(options=chrome_options,executable_path='./chromedriver/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(1920, 1080)

    driver.get(url_origin)
    
    try: 
        if(url):
            # https://www.colaboraread.com.br/integracaoAlgetec/index?usuarioEmail=danielestevao232004%40gmail.com&usuarioNome=DANIEL+ESTEVAO+MARTINS+MENDES&disciplinaDescricao=ANÁLISE+ORIENTADA+A+OBJETOS&atividadeId=3925709&atividadeDescricao=Leitura1+-+ANÁLISE+ORIENTADA+A+OBJETOS&ofertaDisciplinaId=2145454&codigoMaterial=0&fornecedor=2&urlOrigem=https%3A%2F%2Fcm-kls-content.s3.amazonaws.com%2F202002%2FINTERATIVAS_2_0%2FANALISE_ORIENTADA_A_OBJETOS%2FLIVRO_DIGITAL%2Findex.html&isAluno=true
            """
                Extrair Valores da URL
            """
            # Faz o parse da URL
            parsed_url = urlparse(url)

            # Extrai os parâmetros da query
            query_params = parse_qs(parsed_url.query)
            
            # Obtém a data e hora atuais
            data_hora_atual = datetime.now()
            # Formata a data e hora como string
            data_hora_formatada = data_hora_atual.strftime("%d_%m_%Y-%H-%M-%S")
            
            data_criacao = data_hora_formatada
            email = query_params.get('usuarioEmail', [''])[0]
            username =  query_params.get('usuarioNome', [''])[0]
            materia = nome_materia
            atividade_id = query_params.get('atividadeId', [''])[0]
            
            #======================= DEBUG ======================#"
            print("Data e hora atual:", data_criacao)
            print("Email:", email)
            print("Nome de usuário:", username)
            print("Nome da Materia:", materia)
            print("ID da atividade:", atividade_id)
            #====================================================#"
            
            """
                Criar uma Pasta Com o Nome da Materia
            """
            
            def criar_pasta_e_arquivo_materia(nome_materia, diretorio_base):
                
                def gerar_codigo_unico():
                        # Gerar um número aleatório entre 100000 e 999999
                        numero_aleatorio = random.randint(100000, 999999)
                        # Gerar um UUID único
                        id_unico = uuid.uuid4()
                        # Concatenar o número aleatório e o UUID para criar o código único
                        codigo_unico = f"{numero_aleatorio}_{id_unico}"
                        return codigo_unico

                    # Exemplo de uso:
                codigo = gerar_codigo_unico()
                print(f"UUID: {codigo}")
                
                # Substitua espaços por underscores e converta para minúsculas
                nome_materia = f"Nome_{nome_materia.replace(' ', '_').lower()} Data_{data_criacao}"
                
                # Caminho completo da nova pasta
                caminho_pasta = os.path.join(diretorio_base, nome_materia)

                # Verifica se a pasta já existe, caso não, cria a pasta
                if not os.path.exists(caminho_pasta):
                    os.makedirs(caminho_pasta)
                    print(f"Pasta '{nome_materia}' criada com sucesso em '{diretorio_base}'.")
                       # Configuração do Selenium
                    chrome_options = Options()
                    chrome_options.add_experimental_option("prefs", {
                        "download.default_directory": f"{diretorio_base}",  # Altere para o caminho desejado
                        "download.prompt_for_download": False,
                        "download.directory_upgrade": True,
                        "safebrowsing.enabled": True
                    })
                    
                    time.sleep(2)
                    # Envia o comando "Ctrl + S" para a página da web
                    cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL

                    ActionChains(driver)\
                        .key_down(cmd_ctrl)\
                        .send_keys("s")\
                        .key_up(cmd_ctrl)\
                        .perform()
                        
                    time.sleep(10)
                else:
                    print(f"A pasta '{nome_materia}' já existe em '{diretorio_base}'.")
                    pass
                    
                # Caminho completo do arquivo a ser criado
                caminho_arquivo = os.path.join(caminho_pasta, f"usuario_{email}.txt")
                
                caminho_comprimido = "./App/Downloads/Comprimidos"
                caminho_fragmentado = "./App/Downloads/Fragmentados"

                # Cria o arquivo de texto
                with open(caminho_arquivo, "w") as arquivo:
                    arquivo.write("Data e hora atual: " + data_criacao + "\n")
                    arquivo.write("Email: " + email + "\n")
                    arquivo.write("Nome de usuário: " + username + "\n")
                    arquivo.write("Nome da Matéria: " + nome_materia + "\n")
                    arquivo.write("ID da atividade: " + atividade_id + "\n")
                    arquivo.write("Local_Comprimido: " + caminho_comprimido + "\n")
                    arquivo.write("Local_Fragmentado: " + caminho_fragmentado + "\n")
                    arquivo.write("UUID: " + codigo)


                print(f"Arquivo 'Usuario_{email}.txt' criado em '{caminho_pasta}'.")
                #valores para usar no Processo de Automação
                return nome_materia,caminho_fragmentado , caminho_comprimido , codigo
            # Exemplo de uso da função
            nome_materia = "ANÁLISE ORIENTADA A OBJETOS"
            diretorio_base = "./App/Downloads/Web"
            
            '''
                Variaveis com os Valores para Apontamento
            '''
            nome_da_materia_salva,caminho_fragmentado_salvo,caminho_comprimido_salvo,codigo_uuid = criar_pasta_e_arquivo_materia(materia, diretorio_base)

            if nome_da_materia_salva == "" and caminho_fragmentado_salvo == "" and caminho_comprimido_salvo == "":
                print("Erro campos Vazios Detectados...")
                # MsgErro = QMessageBox.critical(None,"Erro","Campos Vazios")
                # MsgErro.addButton(QMessageBox.Ok)
                # MsgErro.exec_()
            else:
                
                try:
                    
                    # Crie uma instância de ActionChains
                    actions = ActionChains(driver)
                    
                    js = """
                        localStorage.setItem('DivMenu', JSON.stringify({"style":"width:200px;"}));
                        let valor = JSON.parse(localStorage.getItem('DivMenu'));
                        let elemento = document.getElementsByClassName('main-leftsidebar-div')[0];
                        elemento.setAttribute('style', valor.style);
                    """
                    driver.execute_script(js)
                    
                    abri_div_menu_lateral_esquerda = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME,"main-leftsidebar-div")))
                    #======================= DEBUG ======================#"
                    print(f"DIV MENU ENCONTRADA INICIADO O PROCESSO DE ABERTURA =>{abri_div_menu_lateral_esquerda}")
                    # Execute o JavaScript para adicionar o estilo ao elemento
                    driver.execute_script("arguments[0].setAttribute('style', 'width:200px;');", abri_div_menu_lateral_esquerda)
                    print(f"ADICIONANDO PROPIEDADES [200!OK] =>True")
                    print(f"ADICIONANDO PROPIEDADES [STYLE/200px]")
                    #====================================================#"
                    
                    print("...")
                    
                    #Começando o Processo 
                    print("INCIANDO EXTRAÇÂO... =>[200!OK]")

                    menu_lateral_esquerdo_div = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME,"leftsidebarmenu")))
                    #======================= DEBUG ======================#"
                    print(f"DEBUG ELEMENTO SIDEBAR ENCONTRADO =>{menu_lateral_esquerdo_div}")
                    #====================================================#"
                    menu_lateral_esquerdo_ul = WebDriverWait(menu_lateral_esquerdo_div, 20).until(EC.presence_of_element_located((By.XPATH,"//*[@id='header-black']/div[3]/div/div/ul")))
                    #======================= DEBUG ======================#"
                    print(f"DEBUG ELEMENTO UL DO SIDEBAR ENCONTRADO =>{menu_lateral_esquerdo_ul}")
                    #====================================================#"

                    # Encontre todas as <li> dentro do <ul>
                    menu_lateral_esquerdo_li = WebDriverWait(menu_lateral_esquerdo_ul, 20).until(EC.presence_of_all_elements_located((By.XPATH,".//li[not(ancestor::li)]")))
                    for i,li_sub_menu in enumerate(menu_lateral_esquerdo_li):
                        
                        print(f"::LI > [{i+1}]->Parents ")
                        #======================= DEBUG ======================#"
                        print(f"#======================= [LI] ======================#")
                        print(f"DEBUG ELEMENTO LI DENTRO DO UL ENCONTRADO =>{li_sub_menu} TABINEX => {li_sub_menu.get_attribute('tabindex')}")
                        print(f"#=============================================================#")
                        #====================================================#"
                        Arquivo_fragamentado_unidade = f"Unidade_{i+1} {nome_da_materia_salva} ID_{codigo_uuid} UUID_{atividade_id}"
                        caminho_pasta = os.path.join(caminho_fragmentado_salvo, Arquivo_fragamentado_unidade)
                        if not os.path.exists(caminho_pasta):
                            os.makedirs(caminho_pasta) #Salvando Unidada Fragementada
                            print(f"Pasta '{Arquivo_fragamentado_unidade}' criada com sucesso em '{caminho_pasta}'.")
                            time.sleep(2)
                            # li_sub_menu.click()
                            actions.move_to_element(li_sub_menu).perform()
                            menu_lateral_esquerdo_sub_menu_a = WebDriverWait(li_sub_menu, 20).until(EC.presence_of_element_located((By.CLASS_NAME,"nav-link")))
                            print(f"#======================= [LI] ======================#")
                            print(f"DEBUG ELEMENTO A DENTRO DO LI DO SUB MENU ENCONTRADO =>{menu_lateral_esquerdo_sub_menu_a} TEXTO => {menu_lateral_esquerdo_sub_menu_a.text} TARGET => {menu_lateral_esquerdo_sub_menu_a.get_attribute('href')}")
                            print(f"#=============================================================#")
                            
                            menu_lateral_esquerdo_sub_menu_div = WebDriverWait(li_sub_menu,20).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"sidebar-second-menu-div")))
                            print(f"#======================= [UL] ======================#")
                            print(f"DEBUG ELEMENTO UL DENTRO DA LI QUANTIDADES => {i+1} DEPOIS DO A TOTAL[{len(menu_lateral_esquerdo_sub_menu_div)}] =>{menu_lateral_esquerdo_sub_menu_div}")
                            print(f"#=============================================================#")
                            
                            
                            escolher_div_extrair_ul = menu_lateral_esquerdo_sub_menu_div[1]
                            print(f"#======================= [DIV] ======================#")
                            print(f"DEBUG ELEMENTO DIV ENCONTADO DENTRO DA UL > {escolher_div_extrair_ul}")
                            print(f"#=============================================================#")
                            
                            # actions.move_to_element(escolher_div_extrair_ul).perform()
                            
                            # Encontre apenas as <ul> que são filhas diretas da <div>
                            div_menu_esquerda_sub_menu_second_ul_in_div = WebDriverWait(escolher_div_extrair_ul, 20).until(EC.presence_of_element_located((By.CLASS_NAME,"sidebar-second-menu")))
                            print(f"#======================= [SUBMENU ENCONTRADO UL] ======================#")
                            print(f"DEBUG ELEMENTO UL ENCONTRADO DENTRO DA DIV PROCURANDO LIS...> {div_menu_esquerda_sub_menu_second_ul_in_div}")
                            print(f"#=============================================================#")
                            
                            div_menu_esquerda_sub_menu_second_Li_ul_in_div = WebDriverWait(div_menu_esquerda_sub_menu_second_ul_in_div, 20).until(EC.presence_of_all_elements_located((By.XPATH,"./li")))
                            print(f"#======================= [SUBMENU ENCONTRADO LI ENCONTRADAS DENTRO DA UL] ======================#")
                            print(f"DEBUG ELEMENTO LI ENCONTRADO DENTRO DA UL PROCURANDO DIV...> {div_menu_esquerda_sub_menu_second_Li_ul_in_div}")
                            print(f"#=============================================================#")
                            
                            # aqui vamos Olhar dentro de Cada list não ordenado para Extrair os Valores da LIS
                            
                            for i,li_in_ul_in_div in enumerate(div_menu_esquerda_sub_menu_second_Li_ul_in_div ):
                                
                                actions.move_to_element(li_in_ul_in_div).perform()
                                
                                """
                                    Salvar as Seções dentro das Unidades
                
                                """
                                a_in_li_in_ul = WebDriverWait(li_in_ul_in_div, 20).until(EC.presence_of_element_located((By.TAG_NAME,"a")))
                                
                                #Criando Pasta dentro da UNIDADE
                                
                                nome_secao_unidade = a_in_li_in_ul.text
                                novo_caminho_unidade_secao = f"{caminho_fragmentado_salvo}/{Arquivo_fragamentado_unidade}"
                                caminho_pasta_sesao = os.path.join(novo_caminho_unidade_secao, nome_secao_unidade)

                                if not os.path.exists(caminho_pasta_sesao):
                                    os.makedirs(caminho_pasta_sesao) #Salvando Unidade Seção
                                    print(f"Pasta '{nome_secao_unidade}' criada com sucesso em '{novo_caminho_unidade_secao}'.")
                                    time.sleep(2)
                                
                                    print(f"#======================= [UL SEÇÃO ENCONTRADA LIS...] ======================#")
                                    print(f"DEBUG ELEMENTO A ENCONTRADO DENTRO DA LI PROCURANDO NA UL...> {a_in_li_in_ul.text} TARGET =>{a_in_li_in_ul.get_attribute('href')}")
                                    print(f"DEBUG ELEMENTO LI ENCONTRADO DENTRO DA UL PROCURANDO NA DIV...> {li_in_ul_in_div}")
                                    print(f"#=============================================================#")

                                    
                                    sidebar_third_menu = WebDriverWait(li_in_ul_in_div, 20).until(EC.presence_of_element_located((By.XPATH,"./div/ul")))
                                    
                                    print(f"#======================= [ULTIMOS UL COM OS LINKS ENCONTRADOS] ======================#")
                                    print(f"UL QUE CONTEM TODOS OS LINKS PARA MONTAGEM ENCONTRADOS...> {sidebar_third_menu}")
                                    print(f"#=============================================================#")

                                    sidebar_third_menu_a = WebDriverWait(sidebar_third_menu, 20).until(EC.presence_of_all_elements_located((By.XPATH,"./li/a")))

                                   # Iterar sobre os elementos do menu de terceiro nível
                                    # for index_a_sidebaser_third, sidebar_third_a in enumerate(sidebar_third_menu_a):
                                    #     print(f"DENTRO DO THIRD MENU FORAM ENCONTRADOS ... => {index_a_sidebaser_third} A")
                                    #     actions.move_to_element(sidebar_third_a).perform()
                                    #     print(f"TARGET => {sidebar_third_a.get_attribute('href')} A => {sidebar_third_a.text}")
                                        
                                    #     # Formatar o caminho para o arquivo HTML
                                    #     a_linkCracker = os.path.join(caminho_pasta_sesao.strip(), f"a_{index_a_sidebaser_third}.html")
                                        
                                    #     # URL do link obtido pelo atributo href
                                    #     url_link_cracker = sidebar_third_a.get_attribute('href')

                                    #     # Fazer uma requisição GET para obter o conteúdo da URL
                                    #     response_link = requests.get(url_link_cracker)

                                    #     # Verificar se a requisição foi bem-sucedida
                                    #     if response_link.status_code == 200:
                                    #         # Conteúdo da resposta (HTML, JSON, etc.)
                                    #         html_content = response_link.content.decode('utf-8')  # Decodificar como UTF-8
                                            
                                    #         # Parse do HTML usando BeautifulSoup
                                    #         soup = BeautifulSoup(html_content, 'html.parser')
                                            
                                    #         # Remover todas as ocorrências das tags <header>
                                    #         for header in soup.find_all('header'):
                                    #             header.decompose()
                                            
                                    #         # Salvar apenas as tags <section> com conteúdo
                                    #         sections_with_content = soup.find_all('section')
                                            
                                    #         # Escrever o conteúdo filtrado no arquivo HTML
                                    #         with open(a_linkCracker, 'w', encoding='utf-8') as arquivo:
                                    #             arquivo.write(str(sections_with_content))
                                            
                                    #         print(f"Arquivo HTML criado em: {a_linkCracker}")
                                    #     else:
                                    #         print(f"A requisição falhou com o status {response_link.status_code}.")

                                    # Iterar sobre os elementos do menu de terceiro nível
                                    for index_a_sidebaser_third, sidebar_third_a in enumerate(sidebar_third_menu_a):
                                        print(f"DENTRO DO THIRD MENU FORAM ENCONTRADOS ... => {index_a_sidebaser_third} A")
                                        actions.move_to_element(sidebar_third_a).perform()
                                        print(f"TARGET => {sidebar_third_a.get_attribute('href')} A => {sidebar_third_a.text}")
                                        
                                        # Formatar o caminho para o arquivo HTML
                                        a_linkCracker = os.path.join(caminho_pasta_sesao.strip(), f"a_{index_a_sidebaser_third}.html")
                                        
                                        # URL do link obtido pelo atributo href
                                        url_link_cracker = sidebar_third_a.get_attribute('href')

                                        # Fazer uma requisição GET para obter o conteúdo da URL
                                        response_link = requests.get(url_link_cracker)

                                        # Verificar se a requisição foi bem-sucedida
                                        if response_link.status_code == 200:
                                            # Conteúdo da resposta (HTML, JSON, etc.)
                                            html_content = response_link.content.decode('utf-8')  # Decodificar como UTF-8
                                            
                                            # Parse do HTML usando BeautifulSoup
                                            soup = BeautifulSoup(html_content, 'html.parser')
                                            
                                            # Remover todas as ocorrências das tags <header> e <footer>
                                            for tag in soup.find_all(['header', 'footer']):
                                                tag.decompose()
                                            
                                            # Escrever o conteúdo filtrado no arquivo HTML
                                            with open(a_linkCracker, 'w', encoding='utf-8') as arquivo:
                                                arquivo.write(str(soup))
                                            
                                            print(f"Arquivo HTML criado em: {a_linkCracker}")
                                        else:
                                            print(f"A requisição falhou com o status {response_link.status_code}.")
                                else:
                                    print("ARQUIVO JÁ EXISTE...") 
                            
                        else:
                            print(f"A pasta '{Arquivo_fragamentado_unidade}' já existe em '{caminho_pasta}'.")
                            pass
                            
                    
                except NoSuchElementException as e:
                    print (f"Não foi possível Encontrar o ELEMENTO {e}")

    except TimeoutException as e :
        print (f"Não foi possível Encontrar o ELEMENTO no Tempo Determinado... {e}")
    
    
# DowloadBook("Análise Orientada a Objetos","http://localhost/AVAPDF/index.html?usuarioEmail=danielestevao232004%40gmail.com&usuarioNome=DANIEL+ESTEVAO+MARTINS+MENDES&disciplinaDescricao=ANÁLISE+ORIENTADA+A+OBJETOS&atividadeId=3925709&atividadeDescricao=Leitura1+-+ANÁLISE+ORIENTADA+A+OBJETOS&ofertaDisciplinaId=2145454&codigoMaterial=0&fornecedor=2&urlOrigem=https%3A%2F%2Fcm-kls-content.s3.amazonaws.com%2F202002%2FINTERATIVAS_2_0%2FANALISE_ORIENTADA_A_OBJETOS%2FLIVRO_DIGITAL%2Findex.html&isAluno=true","Janela_principal","https://cm-kls-content.s3.amazonaws.com/202002/INTERATIVAS_2_0/ANALISE_ORIENTADA_A_OBJETOS/LIVRO_DIGITAL/index.html")