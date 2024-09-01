import sys
import time
import threading
import random
import psutil
from urllib.parse import urlparse, parse_qs
import socket
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QScrollArea, QLabel, QWidget, QFrame, QHBoxLayout
from PyQt5.QtGui import QFont, QColor, QPainter
from PyQt5.QtCore import Qt, QTimer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import pickle
from fake_useragent import UserAgent
from .DownloadLivro import DowloadBook

# Obtendo o nome da máquina
machine_name = socket.gethostname()

# Obtendo os endereços IP
ipv4_addresses = [addr.address for iface, addrs in psutil.net_if_addrs().items() for addr in addrs if addr.family == socket.AF_INET]
ipv6_addresses = [addr.address for iface, addrs in psutil.net_if_addrs().items() for addr in addrs if addr.family == socket.AF_INET6]

# Estilo "hacker"
class HackerStyle:
    # Estilo para o texto
    TEXT_STYLE = "color: lime; font-family: Courier New, monospace; font-size: 12pt;"

    # Estilo para o fundo
    BACKGROUND_STYLE = "background-color: black;"
    
    # Estilo para o frame
    FRAME_STYLE = "background-color: #333333; border: 2px solid lime; border-radius: 10px;"

# Widget para o gráfico bonito
class BeautifulGraph(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.graph_values = [50] * 100  # Lista para armazenar os valores do gráfico
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(1000)  # Atualizar o gráfico a cada segundo

    def update_graph(self):
        # Adicione um novo valor aleatório à lista
        new_value = random.randint(0, 100)
        self.graph_values.append(new_value)
        self.graph_values.pop(0)  # Remova o valor mais antigo

        # Atualize o widget
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0))  # Cor de fundo preta
        
        # Desenha o gráfico com base nos valores
        step_size = self.width() / len(self.graph_values)
        for i, value in enumerate(self.graph_values):
            x = i * step_size
            y = self.height() - value * self.height() / 100
            painter.setPen(QColor(0, 255, 0))  # Cor do gráfico
            painter.drawLine(x, self.height(), x, y)

def LogsApp():
    myLogs = ["01","02","02"]
    return myLogs

def BuscarLivroGrapichs(username,password,materia):
    
    def get_random_user_agent():
        ua = UserAgent()
        return ua.random
    
    random_user_agent = get_random_user_agent()
    print("User-Agent Aleatório:", random_user_agent)
    

    chrome_options = Options()
    chrome_options.binary_location = "124.0.6367.91\chrome.exe"
    service = Service(options=chrome_options,executable_path='./chromedriver/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://www.colaboraread.com.br")
     # Define o tamanho da janela do navegador
    # chrome_options.add_argument("--headless")
    driver.set_window_size(1920, 1080)
    # Configura o User-Agent nas opções do Chrome
    chrome_options.add_argument(f"user-agent={random_user_agent}")

    # Criação do driver do Chrome com as opções configuradas
    # driver = webdriver.Chrome(options=chrome_options)
    
    # Salve os cookies da sessão atual
    cookies = driver.get_cookies()
    
    try:
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
        time.sleep(2)
        
        print(f"MATERIA ESCOLHIDA  => {materia}")
                
        #Aqui ele Retorna a UL dentro de Cada ul > li > Table > tbody > tr > td
        MateriasBusca = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME,"list-line")))
        print(f"BUSCA MATERIAS ELEMENTO UL => {MateriasBusca}")
        #Aqui ele Retorna a Li dentro da UL
        MateriaBusca_li = WebDriverWait(MateriasBusca, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"atividadesCronograma")))
        print(f"BUSCA MATERIAS ELEMENTO LI => {MateriaBusca_li}")
        
        # aqui ele me Retorna todas as Class da LI com Cada elementos Respectivo
        for index,li in enumerate(MateriaBusca_li):
            try:
                print(f"{index}) ELEMENTOS LI INDEPENDENTS ENCONTRADOS => {li}")
                # aqui ele me Retorna todas as Class Table de Cada elementos Respectivo
                MateriaBusca_Table = WebDriverWait(li, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,".table > tbody > tr")))
                print(f"ELEMENTOS TABLE => DO IX:{index} > TBODY > TR ENCONTRADOS => {MateriaBusca_Table}")
                # aqui ele me Retorna todas as Class TR de Cada elementos Table Encontrado Respectivo
                MateriaBusca_Td = WebDriverWait(MateriaBusca_Table, 30).until(EC.presence_of_element_located((By.CLASS_NAME,"atividadesCronogramaTableNome")))
                print(f"ELEMENTOS TR => DO IX:{index} > ENCONTRADOS => {MateriaBusca_Td}")
                # aqui ele me Retorna todas aa Tags A de Cada elementos Tr Encontrado Respectivo
                MateriaBusca_a = WebDriverWait(MateriaBusca_Td, 30).until(EC.presence_of_element_located((By.TAG_NAME,"a")))
                print(f"ELEMENTOS A => DO IX:{index} > ENCONTRADOS => {MateriaBusca_a}")
                ################################# Atualizando os Atributios ====================================
                Title_Materia = MateriaBusca_a.get_attribute("title")
                Href_Materia  = MateriaBusca_a.get_attribute("href")
                print(f"ATRIBUTOS A => [{index}] TARGET:{Title_Materia} LINK:{Href_Materia}") 
                
                #Aqui Verica se a materia Escolhida pelo usuario Correponde com algun title
                
                # Convertendo ambas as strings para minúsculas e removendo espaços extras
                if materia.strip().lower() == Title_Materia.strip().lower():
                    print(f"MT1:{materia} => MT2:{Title_Materia} VERIFICADO... INICIANDO > TARGET:{Title_Materia} LINK:{Href_Materia}")
                    oferta_diciplina = Href_Materia.split("/aluno/timeline")[1]
                    url_momento_real = driver.current_url
                    # MateriaBusca_a.click()
                    # https://www.colaboraread.com.br/aluno/timeline/index/3673690202?ofertaDisciplinaId=2145455
                    print(f"CRACKEANDO URL :{Href_Materia}")
                    print(f"GERANDO DICIPLINA :{oferta_diciplina}")
                    print(f"INICIANDO PROTOCOLO DE CONTENÇÃO...")
                    MateriaBusca_a.click()
                    time.sleep(5)
                    print(f"OBTENDO NOVA URL: {url_momento_real}")
                    print(f"ENCUTANDO URL:  https://www.colaboraread.com.br/aluno/timeline{oferta_diciplina}")
                    
                    nova_url = f"https://www.colaboraread.com.br/aluno/timeline{oferta_diciplina}"
                    
                    if(nova_url == f"https://www.colaboraread.com.br/aluno/timeline{oferta_diciplina}"):
                        print("Entrando na Nova URL...")
                        
                        titulo_newPage = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/header/h2")))
                        print(f"ELEMENTO H2 ENCONTRADO => {titulo_newPage}")
                        print(f"ELEMENTO TEXTO H2 => {titulo_newPage.text}")
                        # Role para baixo até que as ULs sejam visíveis
                        driver.execute_script("window.scrollTo(0, 250);")
                                
                        #BUSCAR O FILTRO 
                        try:
                            filtro_checkbox = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "filters-marca-todos")))
                            if filtro_checkbox.is_selected():
                                print("O filtro está marcado.")
                                filtro_checkbox.click()
                                print("O filtro foi desmarcado.")
                                filtro_checkbox_all = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "checkbox")))
                                print(f"ELEMENTO CHECKBOXS ENCONTRADOS => {filtro_checkbox_all}")
                                
                                for ul in filtro_checkbox_all:
                                    # Encontre todas as LI dentro de cada UL
                                    Elementos_tools_label = WebDriverWait(ul, 30).until(EC.presence_of_element_located((By.TAG_NAME,"label")))
                                    print(f"ELEMENTO LABEL ENCONTRADO => {Elementos_tools_label}")
                                    print("ELEMENTO LABEL TEXT => {} ".format(Elementos_tools_label.text))
                                    Elementos_tools_input = WebDriverWait(Elementos_tools_label, 30).until(EC.presence_of_element_located((By.TAG_NAME,"input")))

                                    if Elementos_tools_label.text == "Leitura":
                                        print("ELEMENTO LABEL TEXT => [ by.Tag => {} == by.text.var => leitura]".format(Elementos_tools_label.text))
                                        print("Inciando PROTOCOLO DE DESLOCAMENTO PARA PDF")
                                        
                                        if Elementos_tools_input.is_selected():
                                            print("O filtro está marcado.")
                                        else:
                                            print("O filtro está desmarcado.")
                                            Elementos_tools_input.click()
                                        
                                        
                                        
                                Elementos_Box_Tools_ul = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "timeline")))
                                print(f"ELEMENTO CONTAINER TIMELINE ENCONTRADOS TODOS => {Elementos_Box_Tools_ul}") 

                                try:
                                    Elementos_Box_Tools_li = WebDriverWait(Elementos_Box_Tools_ul, 30).until(EC.presence_of_all_elements_located((By.TAG_NAME,"li")))
                                    for index, li in enumerate(Elementos_Box_Tools_li):
                                        print(f"================================= |LI=>[{index}]| =================================")
                                        print(f"-------------------------------- INFORMAÇÃOES GERAIS --------------------------")
                                        print(li.text)
                                        print(f"-------------------------------------------------------------------------------")
                                        # Obter todas as tags 'a' dentro da tag 'li'
                                        print(f"---------------------------------- LINKS ENCONTRADOS -------------------------------")
                                        links = li.find_elements(By.TAG_NAME, "a")
                                        for link in links:
                                            if link.text == "Livro Didático":
                                                print("ENTRANDO NA URL => INCIANDO SCKT PARA LPDF")
                                                print(f"Link: Nome : {link.text} Target : {link.get_attribute('href')}")
                                                link.click()
                                                # Salve os cookies em um arquivo
                                                with open('./App/Cookie/cookies.pkl', 'wb') as f:
                                                    pickle.dump(cookies, f)
                                                time.sleep(1)
                                                print("URL INICIADA EM {} ... FECHANDO ABA -1".format(link.text))
                                                # driver.close()
                                                time.sleep(2)
                                                
                                                parsed_link = urlparse(link.get_attribute('href'))
                                                query_params = parse_qs(parsed_link.query)
                                                url_origem = query_params.get('urlOrigem', [None])[0]
                                                # driver.get(url_origem)
                                                print(f"URL ORIGINAL {url_origem}")               
                                                janelas = driver.window_handles
                                                driver.switch_to.window(janelas[1])  
                                                driver.close()
                                                driver.switch_to.window(janelas[0]) 
                                                print("INICIANDO DowloadBook BOOK")
                                                DowloadBook(materia,link.get_attribute('href'),"",url_origem)
                                                time.sleep(3)
                                                driver.quit()
                                        print(f"-------------------------------------------------------------------------------------")
                                        print(f"==================================================================================")
                                        
                                        
                                except NoSuchElementException:
                                    print("TimeLine não foi Encontrada")
                                
                            else:
                                print("O filtro não está marcado.")
                                
                        except NoSuchElementException:
                            driver.execute_script("window.scrollBy(0, 500);")
                            print("Elemento do filtro checkbox não encontrado. A página foi rolada para baixo.")

                        
            except StaleElementReferenceException:
                print(f"Elemento estático foi referenciado. Alterando URL :)")
                # Refresh the elements before interacting with them again
                MateriaBusca_li = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "atividadesCronograma")))
                continue        
                
    except TimeoutException:
        print("O elemento não foi encontrado na página dentro do tempo limite.")
    
    driver.quit()


class Janela_Busca_livro(QDialog):
    def __init__(self,Dialog, username, password, materia):
        super().__init__()
        self.setWindowTitle("Buscar Livro")
        self.setFixedSize(800, 600)
        self.setStyleSheet(HackerStyle.BACKGROUND_STYLE)
        
        terminal_BuscarLivroGrapichs= threading.Thread(target=BuscarLivroGrapichs, args=(username, password, materia))
        terminal_BuscarLivroGrapichs.daemon = True
        terminal_BuscarLivroGrapichs.start()

        layout = QVBoxLayout(self)

        # Adicionando o gráfico bonito
        graph_widget = BeautifulGraph()
        layout.addWidget(graph_widget)

        cards_layout = QHBoxLayout()

        frame_user_info = QFrame()
        frame_user_info.setStyleSheet(HackerStyle.FRAME_STYLE)
        frame_user_info_layout = QVBoxLayout(frame_user_info)
        
        label_info_user = QLabel("Informações Usuário")
        label_info_user.setStyleSheet(HackerStyle.TEXT_STYLE)
        frame_user_info_layout.addWidget(label_info_user)

    
        label_usuario = QLabel(f"Usuário:{username}")
        label_usuario.setStyleSheet(HackerStyle.TEXT_STYLE)
        label_usuario.setAlignment(Qt.AlignCenter)
        frame_user_info_layout.addWidget(label_usuario )

        # senha com asteriscos após os primeiros quatro caracteres
        password_masked = password[:4] + '*' * (len(password) - 4)

 
        label_password_value = QLabel("Senha:" + password_masked)
        label_password_value.setStyleSheet(HackerStyle.TEXT_STYLE)
        frame_user_info_layout.addWidget(label_password_value)

        cards_layout.addWidget(frame_user_info)


        frame_machine_info = QFrame()
        frame_machine_info.setStyleSheet(HackerStyle.FRAME_STYLE)
        frame_machine_info_layout = QVBoxLayout(frame_machine_info)


        label_machine_name = QLabel(f"MSCKT:{machine_name}")
        label_machine_name.setStyleSheet(HackerStyle.TEXT_STYLE)
        frame_machine_info_layout.addWidget(label_machine_name)

       # Senha com asteriscos após os primeiros quatro caracteres
        ipv4_masked = [addr[:8] + '-' * (len(addr) - 4) for addr in ipv4_addresses]

        label_ipv4 = QLabel(f"IPv4:{ipv4_masked[0]}")  
        label_ipv4.setStyleSheet(HackerStyle.TEXT_STYLE)
        frame_machine_info_layout.addWidget(label_ipv4)


        ipv6_masked = [addr[:8] + '-' * (len(addr) - 4) for addr in ipv6_addresses]

        label_ipv6 = QLabel(f"IPv6:{ipv6_masked[0]}")
        label_ipv6.setStyleSheet(HackerStyle.TEXT_STYLE)
        frame_machine_info_layout.addWidget(label_ipv6)

        cards_layout.addWidget(frame_machine_info)


        frame_subject = QFrame()
        frame_subject.setStyleSheet(HackerStyle.FRAME_STYLE)
        frame_subject_layout = QVBoxLayout(frame_subject)
        label_subject = QLabel("Matéria: " + materia)
        label_subject.setStyleSheet(HackerStyle.TEXT_STYLE)
        frame_subject_layout.addWidget(label_subject)
        cards_layout.addWidget(frame_subject)

        layout.addLayout(cards_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        logs_widget = QWidget()  
        logs_layout = QVBoxLayout(logs_widget)
        Logs = LogsApp()  # Supondo que LogsApp é uma classe que contém uma lista de logs
        for log in Logs:  
            log_label = QLabel(f"Log {log}")
            log_label.setStyleSheet(HackerStyle.TEXT_STYLE)
            logs_layout.addWidget(log_label)
      
        scroll_area.setWidget(logs_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = Janela_Busca_livro("","61439646376", "Tccc123456sed654", "Análise Orientada a Objetos")
    janela.show()
    sys.exit(app.exec_())
