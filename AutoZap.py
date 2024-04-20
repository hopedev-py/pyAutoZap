import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
from datetime import datetime, timedelta
import time
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Grupo e agenda de envio
grupo = " <ID_DO_GRUPO_AQUI_> "

# Inicializar o navegador
driver = webdriver.Chrome()  # Você precisa ter o ChromeDriver instalado e configurado

def get_versiculo_do_dia():
    try:
        url = "https://www.bibliaon.com/versiculo_do_dia"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        # Encontrar o elemento que contém o versículo do dia
        versiculo_element = soup.find("div", class_="v_dia").find("p")
        versiculo = versiculo_element.text.strip()
        return versiculo
    except Exception as e:
        print(f"Erro ao fazer scraping do versículo do dia: {e}")
        return None

def enviar_whatsapp_grupo(versiculo, root):
    global grupo, driver
    tempo_envio = 5 * 60  # 5 minutos em segundos (Tempo de reenvio)
    while True:
        try:
            versiculo_corrigido = unidecode(versiculo)
            # Abrir o WhatsApp Web
            driver.get("https://web.whatsapp.com/")
            # Esperar até que a página esteja completamente carregada
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
            # Encontrar o grupo pelo nome
            search_box = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')
            search_box.send_keys(grupo)
            search_box.send_keys(Keys.ENTER)
            # Esperar um pouco para o chat carregar
            time.sleep(2)
            # Enviar a mensagem
            input_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
            input_box.send_keys(versiculo_corrigido)
            input_box.send_keys(Keys.ENTER)
            print("Mensagem enviada com sucesso para o grupo!")
        except Exception as e:
            print(f"Erro ao enviar mensagem para o grupo: {e}")

        # Mostrar a janela com o timer regressivo
        countdown_label = tk.Label(root, font=('Helvetica', 48), text="00:00:00")
        countdown_label.pack()

        tempo_restante = tempo_envio
        while tempo_restante > 0:
            minutos, segundos = divmod(tempo_restante, 60)
            horas, minutos = divmod(minutos, 60)
            tempo_formatado = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
            countdown_label.config(text=tempo_formatado)
            root.update()
            time.sleep(1)
            tempo_restante -= 1

        countdown_label.pack_forget()  # Ocultar o timer após o término

        # Aguardar 10 segundos antes do próximo envio
        time.sleep(10)

# Iniciar o envio de mensagens agendadas
versiculo = get_versiculo_do_dia()
if versiculo:
    print("Versículo do Dia:")
    print(versiculo)
    root = tk.Tk()
    enviar_whatsapp_grupo(versiculo, root)
    root.mainloop()  # Manter a janela gráfica aberta
else:
    print("Não foi possível obter o versículo do dia.")
