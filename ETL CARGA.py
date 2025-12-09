import mysql.connector
import pandas as pd


DB_CONFIG = {
    'host': "localhost",
    'user': "root",
    'password': "Lanadelrey123",
    'database': "PoblacionDB",
    'auth_plugin': 'mysql_native_password'
}


def obtener_id_region(cursor, nombre_region):
    cursor.execute("SELECT id_region FROM Region WHERE nombre_region = %s", (nombre_region,))
    res = cursor.fetchone()
    if res:
        return res[0]
    else:
        cursor.execute("INSERT INTO Region (nombre_region) VALUES (%s)", (nombre_region,))
        return cursor.lastrowid


def cargar_datos():
    try:

        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Leemos el CSV
        try:
            df = pd.read_csv("poblacion.csv")
        except FileNotFoundError:
            print("ERROR: No se encontró el archivo 'poblacion.csv'")
            return

        print(f"Cargando {len(df)} países a la Base de Datos...")

        for i, fila in df.iterrows():
            id_reg = obtener_id_region(cursor, fila['Categoria'])

            sql = """INSERT INTO Pais (nombre, poblacion, edad_promedio, migrantes_netos, id_region) 
                     VALUES (%s, %s, %s, %s, %s)"""

            cursor.execute(sql, (fila['Pais'], fila['Poblacion'], fila['Edad'], fila['Migrantes'], id_reg))

        conn.commit()
        print("¡Base de datos con éxito!")
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error de MySQL: {err}")

    except Exception as e:
        print(f"Otro error: {e}")


if __name__ == "__main__":
    cargar_datos()