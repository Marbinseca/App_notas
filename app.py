# Importar las bibliotecas necesarias
import gradio as gr
import pandas as pd
import numpy as np
import tempfile # Para crear archivos temporales
import os       # Para gestionar archivos
import plotly.express as px # Para generar gráficos interactivos con Plotly
import gradio.themes as themes # Para mejorar la estética de la interfaz

# Definir la función que leerá el archivo (CSV o Excel), calculará el promedio y mostrará los resultados
def process_academic_data(file):
    """
    Lee un archivo (CSV o Excel), asume que la primera columna es el nombre del alumno,
    calcula el promedio de las notas académicas (desde la segunda columna en adelante),
    determina el estado del curso (aprobó/no aprobó),
    y prepara el contenido para visualización, descarga y graficación con Plotly.
    """
    # Si no se ha subido ningún archivo, devolver un DataFrame vacío, None para el archivo de descarga y None para el gráfico
    if file is None:
        return pd.DataFrame(), None, None

    file_extension = os.path.splitext(file.name)[1].lower()
    df = pd.DataFrame() # Inicializar df

    try:
        if file_extension == '.csv':
            df = pd.read_csv(file.name)
        elif file_extension == '.xlsx':
            df = pd.read_excel(file.name)
        else:
            # Manejar tipos de archivo no soportados
            return pd.DataFrame({"Error": ["Formato de archivo no soportado. Por favor, sube un archivo CSV o XLSX."]}, ), None, None

        # --- Paso 1: Asegurar que la primera columna sea tratada como el nombre del alumno ---
        # Si el DataFrame no está vacío y tiene al menos una columna
        if not df.empty and len(df.columns) > 0:
            # Renombrar la primera columna a 'Nombre del Alumno' para estandarizarla
            original_first_col_name = df.columns[0]
            if original_first_col_name != 'Nombre del Alumno':
                df.rename(columns={original_first_col_name: 'Nombre del Alumno'}, inplace=True)
            # Asegurarse de que sea de tipo 'object' (string)
            df['Nombre del Alumno'] = df['Nombre del Alumno'].astype(str)
            student_name_column = 'Nombre del Alumno'
        else:
            student_name_column = None # No hay columna de nombre si el DF está vacío

        # --- Paso 2: Identificar las columnas de notas (desde la segunda columna en adelante) ---
        # Todas las columnas excepto la primera (que asumimos es el nombre)
        grade_columns = []
        if len(df.columns) > 1: # Asegurarse de que hay más de una columna
            for col_name in df.columns[1:]: # Iterar desde la segunda columna
                # Intentar convertir a numérico. Los valores no numéricos se convertirán a NaN.
                df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
                # Si la columna ahora es numérica (o lo era antes), la consideramos una columna de notas
                if df[col_name].dtype in ['int64', 'float64']:
                    grade_columns.append(col_name)

        if not grade_columns:
            # Si no se encuentran columnas numéricas para las notas, devolver el DataFrame original con un mensaje
            print("No se encontraron columnas de notas numéricas válidas (desde la segunda columna).")
            
            temp_file_path = None
            if not df.empty:
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".csv", encoding='utf-8') as tmp:
                    df.to_csv(tmp.name, index=False)
                    temp_file_path = tmp.name
            
            # Devolver el DataFrame, el archivo de descarga y None para el gráfico
            return pd.DataFrame({"Advertencia": ["No se encontraron columnas numéricas de notas. Asegúrate de que las notas estén desde la segunda columna en adelante y en formato numérico."]}).append(df, ignore_index=True), temp_file_path, None

        # --- Paso 3: Calcular el promedio de las notas ---
        # Calcular el promedio de las notas, ignorando los valores NaN (esto es robusto a celdas vacías o no numéricas)
        df['Promedio de Notas'] = df[grade_columns].apply(np.nanmean, axis=1)

        # Definir el umbral para el curso satisfactorio
        threshold = 3.0

        # --- Paso 4: Determinar si el alumno cursó satisfactoriamente el curso ---
        # Si el promedio es mayor o igual a 3, es "Aprobó", de lo contrario "No Aprobó"
        df['Estado de Aprobación'] = df['Promedio de Notas'].apply(
            lambda x: "Aprobó" if x >= threshold else "No Aprobó"
        )

        # Redondear el promedio para una mejor visualización
        df['Promedio de Notas'] = df['Promedio de Notas'].round(2)

        # --- Paso 5: Preparar el DataFrame para la descarga con las columnas especificadas ---
        # Las columnas para la descarga serán: Nombre del Alumno, Promedio de Notas, Estado de Aprobación
        download_cols = []
        if student_name_column and student_name_column in df.columns:
            download_cols.append(student_name_column)
        
        # Siempre incluir Promedio de Notas y Estado de Aprobación si existen
        if 'Promedio de Notas' in df.columns:
            download_cols.append('Promedio de Notas')
        if 'Estado de Aprobación' in df.columns:
            download_cols.append('Estado de Aprobación')

        # Asegurarse de que el DataFrame para descargar solo contenga las columnas deseadas y en el orden correcto
        df_to_download = df[download_cols]

        # Guardar el DataFrame a un archivo Excel temporal para la descarga
        temp_file_path = None
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".xlsx") as tmp: # Cambiado a .xlsx
            df_to_download.to_excel(tmp.name, index=False) # Cambiado a .to_excel
            temp_file_path = tmp.name

        # --- Paso 6: Generar el gráfico de barras para aprobados y no aprobados con Plotly ---
        plotly_fig = None
        if 'Estado de Aprobación' in df.columns:
            # Agrupar por 'Estado de Aprobación' y recolectar los nombres de los alumnos
            status_summary = df.groupby('Estado de Aprobación')['Nombre del Alumno'].apply(lambda x: '<br>'.join(x)).reset_index()
            status_summary.columns = ['Estado', 'Nombres de Alumnos']
            
            # Añadir el conteo de alumnos a este DataFrame
            status_counts = df['Estado de Aprobación'].value_counts().reset_index()
            status_counts.columns = ['Estado', 'Número de Alumnos']
            
            # Unir el conteo con los nombres de los alumnos
            plot_data = pd.merge(status_counts, status_summary, on='Estado', how='left')

            plotly_fig = px.bar(
                plot_data,
                x='Estado',
                y='Número de Alumnos',
                title='Conteo de Alumnos Aprobados y No Aprobados',
                color='Estado', # Diferenciar barras por color
                color_discrete_map={'Aprobó': 'lightgreen', 'No Aprobó': 'salmon'}, # Colores específicos
                text='Número de Alumnos', # Mostrar el valor encima de las barras
                hover_data={'Nombres de Alumnos': True, 'Número de Alumnos': False} # Mostrar los nombres en el hover
            )
            # Personalizar el layout para mejor visualización
            plotly_fig.update_layout(xaxis_title="Estado del Curso", yaxis_title="Número de Alumnos")
            plotly_fig.update_traces(
                texttemplate='%{text}',
                textposition='outside',
                # Personalizar hovertemplate para mostrar el conteo y la lista de nombres
                hovertemplate='<b>Estado</b>: %{x}<br><b>Número de Alumnos</b>: %{y}<br><b>Alumnos:</b><br>%{customdata[0]}<extra></extra>'
            )
            plotly_fig.update_yaxes(range=[0, plot_data['Número de Alumnos'].max() * 1.1]) # Ajustar rango del eje Y

        # Devolver el DataFrame completo para la visualización, la ruta del archivo temporal para la descarga y el objeto del gráfico Plotly
        return df, temp_file_path, plotly_fig
    
    except pd.errors.EmptyDataError:
        print("El archivo está vacío.")
        return pd.DataFrame({"Error": ["El archivo está vacío."]}, ), None, None
    except pd.errors.ParserError as pe:
        print(f"Error de análisis del archivo: {pe}")
        return pd.DataFrame({"Error": [f"Error al analizar el archivo. Asegúrate de que el formato sea correcto: {pe}"]}), None, None
    except Exception as e:
        # Manejar posibles errores generales durante la lectura o procesamiento del archivo
        print(f"Error general al procesar el archivo: {e}")
        return pd.DataFrame({"Error": [f"No se pudo procesar el archivo: {e}"]}), None, None

# Crear la interfaz de Gradio usando Blocks para un layout personalizado
# Se ha aplicado un tema 'Soft' para un aspecto más elegante y moderno.
with gr.Blocks(title="Análisis de Notas de Alumnos", theme=themes.Soft()) as demo:
    gr.Markdown("""
    # Análisis de Notas de Alumnos
    Sube un archivo CSV o EXCEL donde la primera columna sean los nombres de los alumnos y las siguientes sean sus notas.
    La aplicación calculará el promedio y determinará si aprobaron o no (>= 3), y mostrará un gráfico de resumen.
    """)

    with gr.Row():
        with gr.Column(scale=1): # Columna izquierda para el input y la tabla
            file_input = gr.File(label="Sube tu archivo CSV o XLSX aquí", file_types=[".csv", ".xlsx"])
            data_output = gr.DataFrame(label="Contenido del archivo con Análisis Completo", interactive=True) # interactive=True para permitir ordenar y filtrar
        
        with gr.Column(scale=2): # Columna derecha para el gráfico y la descarga
            plot_output = gr.Plot(label="Gráfico de Alumnos Aprobados vs. No Aprobados")
            download_file_output = gr.File(label="Descargar Resultados del Análisis (Excel)", file_count="single", interactive=False) # Actualizado el label

    # Conectar los componentes de entrada y salida a la función de procesamiento
    file_input.change(
        fn=process_academic_data,
        inputs=file_input,
        outputs=[data_output, download_file_output, plot_output]
    )

# Iniciar la aplicación Gradio
if __name__ == "__main__":
    demo.launch()