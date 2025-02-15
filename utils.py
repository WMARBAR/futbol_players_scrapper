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


   def ft_players_scrappingII(self,link):
        """
        Extrae información sobre los jugadores de cada equipo desde una página de Wikipedia del Mundial.
        Devuelve diccionarios organizados por equipo con datos de jugadores, posiciones, edades, partidos jugados y clubes.
        """

        # Iniciar el navegador
        driver = webdriver.Chrome()
        driver.get(link)

        # Esperar que cargue la página completamente
        time.sleep(5)

        # Obtener HTML de la página
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # 1️⃣ EXTRAER LOS EQUIPOS PARTICIPANTES
        equipos = []
        divs = soup.find_all('div', class_='mw-heading mw-heading4')
        for div in divs:
            h4 = div.find('h4')  # Buscar el h4 dentro del div
            if h4:
                pais = h4.text.strip()
                if pais and "editar" not in pais:  # Evitar texto irrelevante
                    equipos.append(pais)

        # 2️⃣ CREAR DICCIONARIOS PARA ALMACENAR DATOS DE JUGADORES
        jugadores_por_equipo = {}
        posiciones_por_equipo = {}
        edades_por_equipo = {}
        partidos_por_equipo = {}
        clubes_por_equipo = {}

        # 3️⃣ BUSCAR TODAS LAS TABLAS DE JUGADORES
        tablas = soup.find_all('table', class_='sortable')

        # 4️⃣ RECORRER CADA TABLA Y ASIGNAR A CADA EQUIPO
        for i, tabla in enumerate(tablas):
            if i < len(equipos):  # Para evitar errores si hay más tablas que equipos
                equipo = equipos[i]  # Nombre del equipo
                jugadores = []
                posiciones = []
                edades = []
                partidos = []
                clubes = []

                # Buscar todas las filas de la tabla, omitiendo la primera (encabezados)
                filas = tabla.find_all('tr')[1:]

                for fila in filas:
                    columnas = fila.find_all('td')

                    if len(columnas) >= 6:  # Evitar errores con filas incompletas
                        nombre_jugador = columnas[1].text.strip()  # Nombre (2da columna)
                        posicion_jugador = columnas[2].text.strip()  # Posición (3ra columna)
                        edad_jugador = columnas[3].text.strip()  # Edad (4ta columna)
                        partidos_jugador = columnas[4].text.strip()  # Partidos (5ta columna)
                        club_jugador = columnas[6].text.strip()  # Club (7ma columna)

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

        driver.quit()  # Cerrar el navegador

        return jugadores_por_equipo, posiciones_por_equipo, edades_por_equipo, partidos_por_equipo, clubes_por_equipo

   def paises_continente(self):
       # Lista de países
        paises = [
            'Inglaterra', 'Francia', 'México', 'Uruguay', 'Argentina',
            'España', 'Suiza', 'Alemania Occidental', 'Brasil', 'Bulgaria',
            'Hungría', 'Portugal', 'Chile', 'Italia', 'Corea del Norte',
            'Unión Soviética', 'Bélgica', 'El Salvador', 'Suecia', 'Israel',
            'Checoslovaquia', 'Rumanía', 'Perú', 'Marruecos',
            'Alemania Oriental', 'Australia', 'Escocia', 'Yugoslavia', 'Zaire',
            'Países Bajos', 'Polonia', 'Haití', 'Corea del Sur', 'Irak',
            'Paraguay', 'Canadá', 'Argelia', 'Irlanda del Norte', 'Dinamarca',
            'Alemania Federal', 'Austria', 'Estados Unidos', 'Camerún',
            'Rumania', 'Costa Rica', 'Colombia', 'Emiratos Árabes Unidos',
            'Egipto', 'Irlanda', 'Rusia', 'Bolivia', 'Alemania', 'Grecia',
            'Nigeria', 'Noruega', 'Arabia Saudita', 'Sudáfrica', 'Irán',
            'RF de Yugoslavia', 'Túnez', 'Croacia', 'Jamaica', 'Japón',
            'Senegal', 'Eslovenia', 'China', 'Turquía', 'Ecuador',
            'Trinidad y Tobago', 'Costa de Marfil', 'Serbia y Montenegro',
            'Angola', 'República Checa', 'Ghana', 'Togo', 'Ucrania',
            'Honduras', 'Bosnia Herzegovina', 'Islandia', 'Serbia', 'Panamá'
        ]

        # Diccionario de países con continentes
        continentes = {
            'Europa': ['Inglaterra', 'Francia', 'España', 'Suiza', 'Alemania Occidental', 'Bulgaria', 'Hungría', 'Portugal', 'Italia', 'Unión Soviética', 'Bélgica', 'Suecia', 'Checoslovaquia', 'Rumanía', 'Alemania Oriental', 'Escocia', 'Yugoslavia', 'Países Bajos', 'Polonia', 'Irlanda del Norte', 'Dinamarca', 'Alemania Federal', 'Austria', 'Irlanda', 'Rusia', 'Grecia', 'RF de Yugoslavia', 'Croacia', 'Eslovenia', 'República Checa', 'Ucrania', 'Bosnia Herzegovina', 'Islandia', 'Serbia'],
            'América': ['México', 'Uruguay', 'Argentina', 'Brasil', 'Chile', 'El Salvador', 'Perú', 'Paraguay', 'Canadá', 'Costa Rica', 'Colombia', 'Bolivia', 'Estados Unidos', 'Haití', 'Ecuador', 'Trinidad y Tobago', 'Honduras', 'Jamaica', 'Panamá'],
            'Asia': ['Corea del Norte', 'Corea del Sur', 'Irak', 'Emiratos Árabes Unidos', 'Arabia Saudita', 'Irán', 'Japón', 'China', 'Turquía'],
            'África': ['Marruecos', 'Zaire', 'Argelia', 'Camerún', 'Egipto', 'Nigeria', 'Sudáfrica', 'Túnez', 'Senegal', 'Costa de Marfil', 'Angola', 'Ghana', 'Togo'],
            'Oceanía': ['Australia']
        }
    # Crear el DataFrame
        paises_continentes = []
        for pais in paises:
            for continente, lista_paises in continentes.items():
                if pais in lista_paises:
                    paises_continentes.append({'pais': pais, 'Continente': continente})

        # Convertir a DataFrame
        df = pd.DataFrame(paises_continentes)
        return df



   def campeones_data(self):
       # Datos de los campeones del Mundial desde 1966
            mundial_campeones = {
                1966: "Inglaterra",
                1970: "Brasil",
                1974: "Alemania Occidental",
                1978: "Argentina",
                1982: "Italia",
                1986: "Argentina",
                1990: "Alemania Occidental",
                1994: "Brasil",
                1998: "Francia",
                2002: "Brasil",
                2006: "Italia",
                2010: "España",
                2014: "Alemania",
                2018: "Francia",
                2022: "Argentina"
            }

            # Crear el DataFrame
            df_mundial = pd.DataFrame(list(mundial_campeones.items()), columns=["Año", "Campeón"])
            return df_mundial

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

   def unir_dataframes(self, df1, df2):
        """
        Une dos DataFrames colocando df2 debajo de df1.
        
        Args:
            df1 (pd.DataFrame): Primer DataFrame.
            df2 (pd.DataFrame): Segundo DataFrame.
        
        Returns:
            pd.DataFrame: DataFrame combinado.
        """
        df_combinado = pd.concat([df1, df2], ignore_index=True)
        return df_combinado

