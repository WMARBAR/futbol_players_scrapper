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
   def ft_players_scrapping(self,link):
        # Iniciar el navegador
        driver = webdriver.Chrome()
        driver.get(link)

        # Esperar que cargue la página completamente
        time.sleep(5)

        # Obtener HTML de la página
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Extraer los equipos (h4 en lugar de div)
        participantes = []
        equipos_div = soup.find_all('h4')  # Buscamos los equipos en los encabezados <h4>

        # Guardamos los nombres de los equipos
        for equipo_div in equipos_div:
            equipo_nombre = equipo_div.text.strip()
            if equipo_nombre and "editar" not in equipo_nombre:  # Evitamos enlaces de edición
                participantes.append(equipo_nombre)

        # Diccionarios para almacenar jugadores, posiciones, edades, partidos jugados y clubes
        jugadores_por_equipo = {}
        posiciones_por_equipo = {}
        edades_por_equipo = {}
        partidos_por_equipo = {}
        clubes_por_equipo = {}

        # Buscar todas las tablas de jugadores
        tablas = soup.find_all('table', class_='wikitable')

        # Asegurar que haya la misma cantidad de equipos y tablas
        for i, tabla in enumerate(tablas):
            if i < len(participantes):  # Para evitar errores si hay más tablas que equipos
                equipo = participantes[i]  # Nombre del equipo
                jugadores = []
                posiciones = []
                edades = []
                partidos = []
                clubes = []

                # Buscar todas las filas de la tabla, omitiendo la primera (encabezados)
                filas = tabla.find_all('tr')[1:]

                for fila in filas:
                    columnas = fila.find_all('td')
                    

                    if len(columnas) >= 5:  # Evitar errores con filas incompletas
                        nombre_jugador = columnas[-4].text.strip()  # Nombre en la antepenúltima posición
                        posicion_jugador = columnas[-5].text.strip()  # Posición en la quinta posición desde el final
                        edad_jugador = columnas[-3].text.strip()  # Edad en la tercera posición desde el final
                        partidos_jugador = columnas[-2].text.strip()  # Partidos jugados en la penúltima posición
                        club_jugador = columnas[-1].text.strip()  # Club en la última columna

                        jugadores.append(nombre_jugador)
                        posiciones.append(posicion_jugador)
                        edades.append(edad_jugador)
                        partidos.append(partidos_jugador)
                        clubes.append(club_jugador)

                # Guardar en los diccionarios
                jugadores_por_equipo[equipo] = jugadores
                posiciones_por_equipo[equipo] = posiciones
                edades_por_equipo[equipo] = edades
                partidos_por_equipo[equipo] = partidos
                clubes_por_equipo[equipo] = clubes

        return jugadores_por_equipo,posiciones_por_equipo,edades_por_equipo,partidos_por_equipo,clubes_por_equipo
            
   def dict_converter(self,dict,col1,col2):
        # Crear lista de datos para el DataFrame
        data = []
        # Recorrer los equipos en el diccionario
        for pais, jugadores in dict.items():
            for jugador in jugadores:
                data.append([pais, jugador])  # Agregar país y nombre del jugador

        # Crear el DataFrame con las columnas correctas
        df = pd.DataFrame(data, columns=[col1, col2])
        return df

   def merge_multiple_dataframes(self,df_list):
        """
        Fusiona múltiples DataFrames con la misma columna inicial ('pais').

        Parámetros:
        - df_list: Lista de DataFrames con la primera columna en común.

        Retorna:
        - Un DataFrame fusionado con todas las columnas de los DataFrames de entrada.
        """
        # Copiar el primer DataFrame como base
        merged_df = df_list[0].copy()

        # Agregar cada DataFrame siguiente eliminando la columna duplicada 'pais'
        for df in df_list[1:]:
            merged_df = pd.concat([merged_df, df.iloc[:, 1:]], axis=1)

        return merged_df

   def merge_dataframes(self,df1, df2, key_df1, key_df2):
        """
        Une df1 con df2 utilizando key_df1 de df1 y key_df2 de df2.
        Retorna df1 con sus columnas originales más las columnas agregadas de df2.
        """
        # Realizar el merge conservando todas las filas de df1
        df_merged = df1.merge(df2, left_on=key_df1, right_on=key_df2, how='left')
        
        return df_merged

   def add_comparison_column(self,df1, nombrecol1, nombrecol2):
        """
        Agrega una nueva columna al DataFrame que indica si los valores en nombrecol1 y nombrecol2 son iguales (1) o diferentes (0).
        La nueva columna se nombra como 'nombrecol1_AND_nombrecol2'.
        """
        # Nombre de la nueva columna
        new_col_name = f"{nombrecol1}_AND_{nombrecol2}"
        
        # Crear la nueva columna con 1 si los valores son iguales y 0 si son diferentes
        df1[new_col_name] = (df1[nombrecol1] == df1[nombrecol2]).astype(int)
        
        return df1

   def guardar_excel(self,df, nombre_archivo):
        """
        Guarda un DataFrame en un archivo Excel con el nombre especificado.
        El archivo tendrá la extensión .xlsx.
        """
        # Asegurar que el nombre tenga la extensión .xlsx
        if not nombre_archivo.endswith('.xlsx'):
            nombre_archivo += '.xlsx'
        
        # Guardar el DataFrame en un archivo Excel
        df.to_excel(nombre_archivo, index=False)
        
        print(f"Archivo guardado como: {nombre_archivo}")