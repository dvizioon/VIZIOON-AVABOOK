import sys
import time
import threading
import random
import psutil
from urllib.parse import urlparse, parse_qs
import socket
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QScrollArea, QLabel, QWidget, QFrame, QHBoxLayout
from PyQt5.QtGui import QFont, QColor, QPainter,QPen
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
# from .DownloadLivro import DowloadBook

# Obtendo o nome da máquina
machine_name = socket.gethostname()

# Obtendo os endereços IP
ipv4_addresses = [addr.address for iface, addrs in psutil.net_if_addrs().items() for addr in addrs if addr.family == socket.AF_INET]
ipv6_addresses = [addr.address for iface, addrs in psutil.net_if_addrs().items() for addr in addrs if addr.family == socket.AF_INET6]


# Função para gerar logs
logs = []

def log_event(message):
    """Função para registrar um log."""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    log_message = f"{timestamp}: {message}"
    logs.append(log_message)
    print(log_message)  # Também exibe no terminal
    # Aqui você pode salvar os logs em um arquivo se desejar
    with open("logs.txt", "a") as log_file:
        log_file.write(log_message + "\n")
      
def LogsApp():
    return logs 

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
        painter.setRenderHint(QPainter.Antialiasing)

        # Desenha o fundo branco
        painter.fillRect(self.rect(), QColor(255, 255, 255))

        # Desenha o gráfico com base nos valores
        pen = QPen(QColor(0, 0, 255), 2)  # Cor azul clássica
        painter.setPen(pen)

        step_size = self.width() / len(self.graph_values)
        for i in range(len(self.graph_values) - 1):
            x1 = int(i * step_size)
            y1 = int(self.height() - (self.graph_values[i] * self.height() / 100))
            x2 = int((i + 1) * step_size)
            y2 = int(self.height() - (self.graph_values[i + 1] * self.height() / 100))
            painter.drawLine(x1, y1, x2, y2)



def BuscarLivroGrapichs(username,password,materia):
    
    """Função que realiza a busca e gera logs"""
    log_event(f"Iniciando busca para o usuário {username}")
    time.sleep(2)
    log_event(f"Usuário {username} buscando o livro da matéria {materia}")
    time.sleep(2)
    log_event("Busca de livro concluída.")
    
    def get_random_user_agent():
        ua = UserAgent()
        return ua.random
    
    random_user_agent = get_random_user_agent()
    log_event(f"User-Agent Aleatório:{random_user_agent}")

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.binary_location = "124.0.6367.91\chrome.exe"
    service = Service(options=chrome_options,executable_path='./chromedriver/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://www.colaboraread.com.br")
    # Define o tamanho da janela do navegador
    # driver.set_window_size(1920, 1080)
    # Configura o User-Agent nas opções do Chrome
    chrome_options.add_argument(f"user-agent={random_user_agent}")
    driver.maximize_window()

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
        log_event(f"Elemento Nome Encontrado => {nome}")
        log_event(f"Elemento Senha Encontrado => {senha}")
        log_event(f"Elemento Submit Encontrado => {submit}")
        # ==========================================#
        
        nome.send_keys(username)
        senha.send_keys(password)

        try:
            

            # Esperar até que o botão de aceitação de cookies apareça
            btnAcceptCookie = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "classBtnCookies"))  # Substitua pelo seletor correto
            )

            # Rolar até o elemento
            driver.execute_script("arguments[0].scrollIntoView(true);", btnAcceptCookie)

            # Esperar até que o botão esteja clicável
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "classBtnCookies")))

            # Clicar no botão
            btnAcceptCookie.click()

            time.sleep(2)  # Tempo de espera para garantir que a ação foi realizada

        except TimeoutException:
            log_event("O elemento não foi encontrado na página dentro do tempo limite.")
            submit.click()
        
        submit.click()
        
        time.sleep(3)
        

        buttonEntrarMaterias = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,"//*[@id='navbar-content-aluno-cursos']/div/div[1]/div/div[3]/form/div[2]/button")))
        buttonEntrarMaterias.click()
        time.sleep(2)
        
        log_event(f"MATERIA ESCOLHIDA  => {materia}")
                
        #Aqui ele Retorna a UL dentro de Cada ul > li > Table > tbody > tr > td
        MateriasBusca = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME,"list-line")))
        log_event(f"BUSCA MATERIAS ELEMENTO UL => {MateriasBusca}")
        #Aqui ele Retorna a Li dentro da UL
        MateriaBusca_li = WebDriverWait(MateriasBusca, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"atividadesCronograma")))
        log_event(f"BUSCA MATERIAS ELEMENTO LI => {MateriaBusca_li}")
        
        # aqui ele me Retorna todas as Class da LI com Cada elementos Respectivo
        for index,li in enumerate(MateriaBusca_li):
            try:
                log_event(f"{index}) ELEMENTOS LI INDEPENDENTS ENCONTRADOS => {li}")
                # aqui ele me Retorna todas as Class Table de Cada elementos Respectivo
                MateriaBusca_Table = WebDriverWait(li, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,".table > tbody > tr")))
                log_event(f"ELEMENTOS TABLE => DO IX:{index} > TBODY > TR ENCONTRADOS => {MateriaBusca_Table}")
                # aqui ele me Retorna todas as Class TR de Cada elementos Table Encontrado Respectivo
                MateriaBusca_Td = WebDriverWait(MateriaBusca_Table, 30).until(EC.presence_of_element_located((By.CLASS_NAME,"atividadesCronogramaTableNome")))
                log_event(f"ELEMENTOS TR => DO IX:{index} > ENCONTRADOS => {MateriaBusca_Td}")
                # aqui ele me Retorna todas aa Tags A de Cada elementos Tr Encontrado Respectivo
                MateriaBusca_a = WebDriverWait(MateriaBusca_Td, 30).until(EC.presence_of_element_located((By.TAG_NAME,"a")))
                log_event(f"ELEMENTOS A => DO IX:{index} > ENCONTRADOS => {MateriaBusca_a}")
                ################################# Atualizando os Atributios ====================================
                Title_Materia = MateriaBusca_a.get_attribute("title")
                Href_Materia  = MateriaBusca_a.get_attribute("href")
                log_event(f"ATRIBUTOS A => [{index}] TARGET:{Title_Materia} LINK:{Href_Materia}") 
                
                #Aqui Verica se a materia Escolhida pelo usuario Correponde com algun title
                
                # Convertendo ambas as strings para minúsculas e removendo espaços extras
                if materia.strip().lower() == Title_Materia.strip().lower():
                    log_event(f"MT1:{materia} => MT2:{Title_Materia} VERIFICADO... INICIANDO > TARGET:{Title_Materia} LINK:{Href_Materia}")
                    oferta_diciplina = Href_Materia.split("/aluno/timeline")[1]
                    url_momento_real = driver.current_url
                    # MateriaBusca_a.click()
                    # https://www.colaboraread.com.br/aluno/timeline/index/3673690202?ofertaDisciplinaId=2145455
                    log_event(f"CRACKEANDO URL :{Href_Materia}")
                    log_event(f"GERANDO DICIPLINA :{oferta_diciplina}")
                    log_event(f"INICIANDO PROTOCOLO DE CONTENÇÃO...")
                    MateriaBusca_a.click()
                    time.sleep(5)
                    log_event(f"OBTENDO NOVA URL: {url_momento_real}")
                    log_event(f"ENCUTANDO URL:  https://www.colaboraread.com.br/aluno/timeline{oferta_diciplina}")
                    
                    nova_url = f"https://www.colaboraread.com.br/aluno/timeline{oferta_diciplina}"
                    
                    if(nova_url == f"https://www.colaboraread.com.br/aluno/timeline{oferta_diciplina}"):
                        log_event("Entrando na Nova URL...")
                        
                        titulo_newPage = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/header/h2")))
                        log_event(f"ELEMENTO H2 ENCONTRADO => {titulo_newPage}")
                        log_event(f"ELEMENTO TEXTO H2 => {titulo_newPage.text}")
                        # Role para baixo até que as ULs sejam visíveis
                        driver.execute_script("window.scrollTo(0, 250);")
                                
                        #BUSCAR O FILTRO 
                        try:
                            filtro_checkbox = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "filters-marca-todos")))
                            if filtro_checkbox.is_selected():
                                log_event("O filtro está marcado.")
                                filtro_checkbox.click()
                                log_event("O filtro foi desmarcado.")
                                filtro_checkbox_all = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "checkbox")))
                                log_event(f"ELEMENTO CHECKBOXS ENCONTRADOS => {filtro_checkbox_all}")
                                
                                for ul in filtro_checkbox_all:
                                    # Encontre todas as LI dentro de cada UL
                                    Elementos_tools_label = WebDriverWait(ul, 30).until(EC.presence_of_element_located((By.TAG_NAME,"label")))
                                    log_event(f"ELEMENTO LABEL ENCONTRADO => {Elementos_tools_label}")
                                    log_event("ELEMENTO LABEL TEXT => {} ".format(Elementos_tools_label.text))
                                    Elementos_tools_input = WebDriverWait(Elementos_tools_label, 30).until(EC.presence_of_element_located((By.TAG_NAME,"input")))

                                    if Elementos_tools_label.text == "Leitura":
                                        log_event("ELEMENTO LABEL TEXT => [ by.Tag => {} == by.text.var => leitura]".format(Elementos_tools_label.text))
                                        log_event("Inciando PROTOCOLO DE DESLOCAMENTO PARA PDF")
                                        
                                        if Elementos_tools_input.is_selected():
                                            log_event("O filtro está marcado.")
                                        else:
                                            log_event("O filtro está desmarcado.")
                                            Elementos_tools_input.click()
                                        
                                        
                                        
                                Elementos_Box_Tools_ul = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "timeline")))
                                log_event(f"ELEMENTO CONTAINER TIMELINE ENCONTRADOS TODOS => {Elementos_Box_Tools_ul}") 

                                try:
                                    Elementos_Box_Tools_li = WebDriverWait(Elementos_Box_Tools_ul, 30).until(EC.presence_of_all_elements_located((By.TAG_NAME,"li")))
                                    for index, li in enumerate(Elementos_Box_Tools_li):
                                        log_event(f"================================= |LI=>[{index}]| =================================")
                                        log_event(f"-------------------------------- INFORMAÇÃOES GERAIS --------------------------")
                                        log_event(li.text)
                                        log_event(f"-------------------------------------------------------------------------------")
                                        # Obter todas as tags 'a' dentro da tag 'li'
                                        log_event(f"---------------------------------- LINKS ENCONTRADOS -------------------------------")
                                        links = li.find_elements(By.TAG_NAME, "a")
                                        for link in links:
                                            if link.text == "Livro Didático":
                                                log_event("ENTRANDO NA URL => INCIANDO SCKT PARA LPDF")
                                                log_event(f"Link: Nome : {link.text} Target : {link.get_attribute('href')}")
                                                link.click()
                                                # Salve os cookies em um arquivo
                                                with open('./App/Cookie/cookies.pkl', 'wb') as f:
                                                    pickle.dump(cookies, f)
                                                time.sleep(1)
                                                log_event("URL INICIADA EM {} ... FECHANDO ABA -1".format(link.text))
                                                # driver.close()
                                                time.sleep(2)
                                                
                                                parsed_link = urlparse(link.get_attribute('href'))
                                                query_params = parse_qs(parsed_link.query)
                                                url_origem = query_params.get('urlOrigem', [None])[0]
                                                # driver.get(url_origem)
                                                log_event(f"URL ORIGINAL {url_origem}")               
                                                janelas = driver.window_handles
                                                driver.switch_to.window(janelas[1])  
                                                driver.close()
                                                driver.switch_to.window(janelas[0]) 
                                                log_event("INICIANDO DowloadBook BOOK")
                                                DowloadBook(materia,link.get_attribute('href'),"",url_origem)
                                                time.sleep(3)
                                                driver.quit()
                                        log_event(f"-------------------------------------------------------------------------------------")
                                        log_event(f"==================================================================================")
                                        
                                        
                                except NoSuchElementException:
                                    log_event("TimeLine não foi Encontrada")
                                
                            else:
                                log_event("O filtro não está marcado.")
                                
                        except NoSuchElementException:
                            driver.execute_script("window.scrollBy(0, 500);")
                            log_event("Elemento do filtro checkbox não encontrado. A página foi rolada para baixo.")

                        
            except StaleElementReferenceException:
                log_event(f"Elemento estático foi referenciado. Alterando URL :)")
                # Refresh the elements before interacting with them again
                MateriaBusca_li = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "atividadesCronograma")))
                continue        
                
    except TimeoutException:
        log_event("O elemento não foi encontrado na página dentro do tempo limite.")
    
    driver.quit()




class Janela_Busca_livro(QDialog):
    def __init__(self, Dialog, username, password, materia):
        super().__init__()
        self.setWindowTitle("Buscar Livro")
        self.setFixedSize(800, 600)
        
        # Iniciar a busca em uma thread separada para não bloquear a interface
        self.thread_busca = threading.Thread(target=BuscarLivroGrapichs, args=(username, password, materia))
        self.thread_busca.daemon = True
        self.thread_busca.start()

        layout = QVBoxLayout(self)

        # Adicionando o gráfico bonito (simulado aqui)
        graph_widget = BeautifulGraph()
        layout.addWidget(graph_widget)

        cards_layout = QHBoxLayout()

        frame_user_info = QFrame()
        frame_user_info_layout = QVBoxLayout(frame_user_info)
        
        label_info_user = QLabel("Informações Usuário")
        frame_user_info_layout.addWidget(label_info_user)

        label_usuario = QLabel(f"Usuário:{username}")
        label_usuario.setAlignment(Qt.AlignCenter)
        frame_user_info_layout.addWidget(label_usuario)

        password_masked = password[:4] + '*' * (len(password) - 4)
        label_password_value = QLabel("Senha:" + password_masked)
        frame_user_info_layout.addWidget(label_password_value)

        cards_layout.addWidget(frame_user_info)

        frame_machine_info = QFrame()
        frame_machine_info_layout = QVBoxLayout(frame_machine_info)

        label_machine_name = QLabel(f"MSCKT: Máquina Simulada")
        frame_machine_info_layout.addWidget(label_machine_name)

        ipv4_masked = ipv4_addresses
        label_ipv4 = QLabel(f"IPv4: {ipv4_masked}")
        frame_machine_info_layout.addWidget(label_ipv4)

        ipv6_masked = ipv6_addresses 
        label_ipv6 = QLabel(f"IPv6: {ipv6_masked}")
        frame_machine_info_layout.addWidget(label_ipv6)

        cards_layout.addWidget(frame_machine_info)

        frame_subject = QFrame()
        frame_subject_layout = QVBoxLayout(frame_subject)
        materiaMask = materia[:20] + '*' * (len(materia) - 20)
        label_subject = QLabel("Matéria: " + materiaMask)
        frame_subject_layout.addWidget(label_subject)
        cards_layout.addWidget(frame_subject)

        layout.addLayout(cards_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        self.logs_widget = QWidget()  
        self.logs_layout = QVBoxLayout(self.logs_widget)

        scroll_area.setWidget(self.logs_widget)

        # Timer para atualizar os logs dinamicamente
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_logs)
        self.timer.start(1000)

    def update_logs(self):
        """Função para atualizar os logs dinamicamente na interface"""
        logs_list = LogsApp()
        # Limpar logs anteriores
        for i in range(self.logs_layout.count()):
            self.logs_layout.itemAt(i).widget().deleteLater()

        # Adicionar novos logs
        for log in logs_list:
            log_label = QLabel(f"Log: {log}")
            self.logs_layout.addWidget(log_label)

        self.logs_widget.setLayout(self.logs_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = Janela_Busca_livro("","61439646376", "Anhanguera@2024", "Linguagem Orientada a Objetos")
    janela.show()
    sys.exit(app.exec_())
