import pandas as pd
import plotly.express as px
import plotly.io as pio
from sqlalchemy import create_engine, text
import webbrowser
import os

# 1. Configuración de conexión
print("Conectando a la base de datos...")
conexion_str = "mysql+mysqlconnector://root:Lanadelrey123@localhost/PoblacionDB"

try:
    engine = create_engine(conexion_str)

    # Reiniciar la tabla para asegurar datos limpios
    sql_tabla = """
    CREATE TABLE IF NOT EXISTS Pais (
        nombre VARCHAR(255),
        poblacion BIGINT,
        edad_promedio FLOAT,
        migrantes_netos BIGINT
    );
    """
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS Pais"))
        conn.execute(text(sql_tabla))
        conn.commit()

    # Datos para el análisis
    datos = [
        {'nombre': 'Mexico', 'poblacion': 126000000, 'edad_promedio': 29.3, 'migrantes_netos': -60000},
        {'nombre': 'United States', 'poblacion': 331000000, 'edad_promedio': 38.5, 'migrantes_netos': 954000},
        {'nombre': 'India', 'poblacion': 1380000000, 'edad_promedio': 28.7, 'migrantes_netos': -480000},
        {'nombre': 'China', 'poblacion': 1410000000, 'edad_promedio': 38.4, 'migrantes_netos': -300000},
        {'nombre': 'Japan', 'poblacion': 125000000, 'edad_promedio': 48.6, 'migrantes_netos': 50000},
        {'nombre': 'Germany', 'poblacion': 83000000, 'edad_promedio': 45.7, 'migrantes_netos': 540000},
        {'nombre': 'Nigeria', 'poblacion': 206000000, 'edad_promedio': 18.6, 'migrantes_netos': -100000},
        {'nombre': 'Brazil', 'poblacion': 214000000, 'edad_promedio': 33.5, 'migrantes_netos': -20000},
        {'nombre': 'Italy', 'poblacion': 59000000, 'edad_promedio': 47.3, 'migrantes_netos': 80000},
        {'nombre': 'Canada', 'poblacion': 38000000, 'edad_promedio': 41.1, 'migrantes_netos': 250000},
        {'nombre': 'Spain', 'poblacion': 47000000, 'edad_promedio': 44.9, 'migrantes_netos': 200000}
    ]

    df_insert = pd.DataFrame(datos)
    df_insert.to_sql('Pais', engine, if_exists='append', index=False)

    # Lectura final
    df = pd.read_sql("SELECT * FROM Pais", engine)

except Exception as e:
    print(f"Error: {e}")
    exit()

# 2. Generación de Gráficos
print("Generando visualizaciones...")

tema = 'plotly_dark'

# Gráfico 1
df['migracion_abs'] = df['migrantes_netos'].abs()
df['Flujo'] = df['migrantes_netos'].apply(lambda x: 'ENTRADA' if x > 0 else 'SALIDA')
df_sorted = df.sort_values(by='migracion_abs', ascending=False)

fig1 = px.bar(df_sorted, x='nombre', y='migrantes_netos', color='Flujo',
              title="Flujo Migratorio Neto",
              color_discrete_map={'ENTRADA': '#00FF41', 'SALIDA': '#FF3333'},
              template=tema, text='migrantes_netos')

fig1.update_traces(texttemplate='%{text:,.0f}', textposition='outside', textfont_color='white')
fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                   margin=dict(t=50, b=50))

# Gráfico 2
fig2 = px.bar(df.sort_values('edad_promedio'), x='edad_promedio', y='nombre', orientation='h',
              title="Edad Promedio por País",
              color='edad_promedio', color_continuous_scale='Reds',
              template=tema, text='edad_promedio')

fig2.update_traces(texttemplate='%{text:.1f}', textposition='outside', textfont_color='white')
fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                   margin=dict(l=150))

# 3. Exportar HTML
html_str = f'''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Poblacional</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #050505;
            color: #ffffff;
            font-family: 'Arial', sans-serif;
        }}
        .hero {{
            background: linear-gradient(rgba(0,0,0,0.6), #050505), 
                        url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1920&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            height: 300px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-bottom: 1px solid #333;
        }}
        .hero h1 {{ font-size: 3rem; text-transform: uppercase; letter-spacing: 3px; margin: 0; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 40px 20px; }}
        .card {{
            background-color: #111;
            border: 1px solid #222;
            padding: 20px;
            margin-bottom: 40px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }}
        h2 {{ border-left: 3px solid #fff; padding-left: 10px; text-transform: uppercase; font-size: 1.1rem; color: #ddd; }}
    </style>
</head>
<body>
    <div class="hero">
        <h1>Análisis Global</h1>
        <p style="color:#ccc;">Reporte de Datos 2024</p>
    </div>
    <div class="container">
        <div class="card">
            <h2>Movimiento Migratorio</h2>
            {pio.to_html(fig1, full_html=False, include_plotlyjs='cdn')}
        </div>
        <div class="card">
            <h2>Edad Promedio</h2>
            {pio.to_html(fig2, full_html=False, include_plotlyjs='cdn')}
        </div>
    </div>
</body>
</html>
'''

archivo = "reporte_final.html"
with open(archivo, "w", encoding="utf-8") as f:
    f.write(html_str)

print("Listo. Abriendo archivo...")
webbrowser.open('file://' + os.path.realpath(archivo))