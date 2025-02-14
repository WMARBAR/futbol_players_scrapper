from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from bs4 import BeautifulSoup
import pandas as pd
import re

class Utils:
   def yt_scraper(self,link):
        driver = webdriver.Chrome()
        url = f'{link}'
        driver.get(url)
        # Espera a que la página cargue completamente
        time.sleep(5)  # Puedes ajustar el tiempo de espera según sea necesario

        # Desplazarse hacia abajo en la página
        scroll_pause_time = 2  # Tiempo de pausa para cargar el contenido
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        print("Desplazando...") 
        while True:
            # Desplazarse hasta el final de la página
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

            # Esperar a que se cargue el nuevo contenido
            time.sleep(scroll_pause_time)

            # Calcular la nueva altura de la página y comparar con la altura anterior
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
        print("Desplazamiento listo...")
        print("Scrapeando...")
        html = driver.page_source
        # Analizar el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        print("Scrapeado ok...")
        comment_threads = driver.find_elements(By.XPATH, '//ytd-comment-thread-renderer')
        print("Listado de comentarios ok...")
        print("Scraping principal ejecutando...")

        # Listas para almacenar nombres de autores, comentarios y likes
        authors = []
        comments = []
        likes = []


        for thread in comment_threads:
            # XPATH para el nombre del autor
            nick_element = thread.find_element(By.XPATH, './/h3/a/span')
            # XPATH para el texto del comentario
            comment_element = thread.find_element(By.XPATH, './/ytd-expander/div/yt-attributed-string/span')
            # XPATH para la cantidad de likes
            like_element = thread.find_element(By.XPATH, './/span[@id="vote-count-middle"]')

            # Extraer texto del nombre del autor, comentario y cantidad de likes
            author_name = nick_element.text.strip()
            comment_text = comment_element.text.strip()
            like_count = like_element.text.strip()
            

            # Guardar en las listas
            authors.append(author_name)
            comments.append(comment_text)
            likes.append(like_count)

        # Imprimir resultados para verificar
        print("Scraping principal finalizado ok...")
        print("Scraping secundario ejecutando...")
 
        titulos = driver.find_elements(By.XPATH, '//*[@id="title"]/h1/yt-formatted-string')
        titulo_video = titulos[0].text if titulos else "Titulo no encontrado"

        youtubers = driver.find_elements(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[1]/ytd-video-owner-renderer/div[1]/ytd-channel-name/div/div/yt-formatted-string/a')
        yt_name = youtubers[0].text if youtubers else "Youtuber no encontrado"
        print("Scraping secundario finalizado ok...")
        # Crear DataFrame
        df = pd.DataFrame({
            'nick': authors,
            'coment': comments,
            'likes': likes,
        })
        df['Video_name']=titulo_video
        df['ytbr_name']=yt_name
            # Crear la columna 'llave'
        df['llave'] = df['nick'] + df['Video_name'] + df['ytbr_name']

        print("Youtube Coments Database: CREATED...")
        return df
            

       