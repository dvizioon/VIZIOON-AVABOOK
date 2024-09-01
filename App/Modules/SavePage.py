from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QScrollArea, QLabel, QWidget, QFrame, QHBoxLayout
from PyQt5.QtGui import QFont, QColor, QPainter
from PyQt5.QtCore import Qt, QTimer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse, parse_qs
import re
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
import pyautogui

import time
import pickle
from datetime import datetime


# Configurações do Chrome
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": "C:/Users/Daniel/Downloads",  # Substitua pelo diretório onde você quer salvar a página
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Inicializa o driver
driver = webdriver.Chrome(options=chrome_options)


# Abre a página da web
driver.get("https://www.google.com")  # Substitua pela URL da página que você quer salvar

# Aguarda alguns segundos para dar tempo de abrir o navegador e a página da web
# Aguarda alguns segundos para dar tempo de abrir o navegador e a página da web
time.sleep(5)

# Simula as teclas CTRL + S para abrir a caixa de diálogo de salvar
pyautogui.hotkey('ctrl', 's')

# Aguarda um curto período de tempo para a caixa de diálogo de salvar ser exibida
time.sleep(2)

# Digita o nome do arquivo para salvar (opcional)
pyautogui.typewrite('nome_da_pagina.html')

# Pressiona a tecla Enter para confirmar o salvamento
pyautogui.press('enter')

# Aguarda um curto período de tempo para a página ser salva
time.sleep(2)

# Pressiona a tecla Shift quatro vezes
for _ in range(4):
    pyautogui.press('shift')

# Pressiona a tecla Enter para confirmar o salvamento
pyautogui.press('enter')

# Fecha o driver
driver.quit()
