import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrapear_poblacion():
    url = "https://www.worldometers.info/world-population/population-by-country/"


    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print("1. Conectando con Worldometer...")
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        # Buscamos la tabla. Si falla el ID, buscamos por clase
        tabla = soup.find('table', id='example2')
        if tabla is None:
            print("   (Tabla principal no encontrada por ID, buscando genérica...)")
            tabla = soup.find('table')  # Agarra la primera tabla que vea

        if tabla is None:
            print("ERROR: No se encontró ninguna tabla.")
            return pd.DataFrame()

        # Obtenemos filas
        cuerpo = tabla.find('tbody')
        if cuerpo:
            filas = cuerpo.find_all('tr')
        else:

            filas = tabla.find_all('tr')[1:]

        datos = []
        print(f"2. Procesando {len(filas)} países...")


        if len(filas) > 0:
            primera = filas[0].find_all('td')
            print(f"   [DEBUG] Primera fila tiene {len(primera)} columnas.")
            print(f"   [DEBUG] Col 1 (País): '{primera[1].text.strip()}'")
            print(f"   [DEBUG] Col 2 (Pob):  '{primera[2].text.strip()}'")


        for fila in filas:
            cols = fila.find_all('td')
            if len(cols) < 3: continue  # Saltar filas vacías

            # EXTRACCIÓN
            # 1. País
            nombre_pais = cols[1].text.strip()

            # 2. Población
            poblacion_txt = cols[2].text.replace(',', '').strip()
            try:
                poblacion = int(poblacion_txt)
            except:
                poblacion = 0


            migrantes = 0
            if len(cols) > 8:
                mig_txt = cols[8].text.replace(',', '').strip()
                if mig_txt and mig_txt != 'N.A.':
                    try:
                        migrantes = int(mig_txt)
                    except:
                        migrantes = 0

            # 4. Edad Promedio (Columna 9)
            edad = 0
            if len(cols) > 9:
                edad_txt = cols[9].text.strip()
                if edad_txt and edad_txt != 'N.A.':
                    try:
                        edad = int(edad_txt)
                    except:
                        edad = 0

            # Categoría para normalización
            if poblacion > 100000000:
                region = "Potencia Demográfica"
            elif poblacion > 50000000:
                region = "País Grande"
            elif poblacion > 10000000:
                region = "País Mediano"
            else:
                region = "País Pequeño"

            datos.append({
                'Pais': nombre_pais,
                'Poblacion': poblacion,
                'Migrantes': migrantes,
                'Edad': edad,
                'Categoria': region
            })

        return pd.DataFrame(datos)

    except Exception as e:
        print(f"Error grave: {e}")
        return pd.DataFrame()


if __name__ == "__main__":
    df = scrapear_poblacion()

    if not df.empty:
        # Imprimimos los primeros 5 países REALES 
        print("\n3. Muestra de datos obtenidos:")
        print(df.head())

        # Verificamos China o India 
        if df.iloc[0]['Poblacion'] > 0:
            df.to_csv("poblacion.csv", index=False)
            print("\n ¡ÉXITO! ")
        else:
            print("\n error")
    else:

        print("No se obtuvieron datos.")
