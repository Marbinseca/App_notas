# Análisis de Notas de Alumnos

## Descripción

Esta es una aplicación interactiva construida con [Gradio](https://www.gradio.app/) que permite a los usuarios analizar datos académicos de manera sencilla. La aplicación está diseñada para procesar archivos CSV o Excel que contengan nombres de alumnos y sus respectivas notas. Calcula automáticamente el promedio de las notas, determina el estado de aprobación (basado en un umbral configurable de 3.0), y presenta los resultados en una tabla interactiva y un gráfico de barras dinámico.

## Características

- **Soporte Multi-formato:** Acepta archivos de entrada en formato CSV y XLSX.
- **Cálculo de Promedios:** Calcula el promedio de las notas académicas de cada alumno.
- **Determinación de Estado:** Clasifica a los alumnos como "Aprobó" o "No Aprobó" basándose en un umbral de promedio (actualmente >= 3.0).
- **Visualización Interactiva:** Muestra los datos procesados en una tabla interactiva dentro de la interfaz de Gradio.
- **Gráficos Dinámicos:** Genera un gráfico de barras interactivo (utilizando Plotly) que visualiza el conteo de alumnos aprobados versus no aprobados, con detalles al pasar el ratón.
- **Descarga de Resultados:** Permite descargar los resultados del análisis (Nombre del Alumno, Promedio de Notas, Estado de Aprobación) en un archivo Excel.

## Cómo Usar

1.  **Preparar el Archivo de Datos:** Asegúrate de que tu archivo CSV o XLSX tenga la siguiente estructura:

    - La **primera columna** debe contener los nombres de los alumnos.
    - Las **columnas siguientes** deben contener las notas numéricas de los alumnos.
    - Ejemplo de `notas.csv`:
      ```csv
      Nombre,Nota1,Nota2,Nota3
      Juan,4.5,3.8,4.0
      Maria,2.1,2.5,1.9
      Pedro,3.0,3.2,2.8
      Ana,4.8,4.9,5.0
      ```

2.  **Ejecutar la Aplicación:**

    ```bash
    python app.py
    ```

    Esto iniciará la interfaz de Gradio en tu navegador web (generalmente en `http://127.0.0.1:7860`).

3.  **Subir el Archivo:** En la interfaz de Gradio, haz clic en el botón "Sube tu archivo CSV o XLSX aquí" y selecciona tu archivo de datos.

4.  **Ver Resultados:** Una vez subido el archivo, la tabla "Contenido del archivo con Análisis Completo" se actualizará con los datos procesados, incluyendo el promedio y el estado de aprobación. El gráfico "Gráfico de Alumnos Aprobados vs. No Aprobados" también se generará automáticamente.

5.  **Descargar Resultados:** Haz clic en el enlace "Descargar Resultados del Análisis (Excel)" para obtener un archivo Excel con los nombres de los alumnos, sus promedios y su estado de aprobación.

## Requisitos

Para ejecutar esta aplicación, necesitarás tener Python instalado, junto con las siguientes bibliotecas:

- `gradio`
- `pandas`
- `numpy`
- `plotly`

## Instalación

1.  **Clonar el Repositorio (si aplica):**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```
2.  **Instalar Dependencias:**
    ```bash
    pip install gradio pandas numpy plotly
    ```

## Tecnologías Utilizadas

- **Python**
- **Gradio:** Para la creación de la interfaz de usuario web.
- **Pandas:** Para la manipulación y análisis de datos.
- **NumPy:** Para operaciones numéricas eficientes.
- **Plotly Express:** Para la generación de gráficos interactivos.


---

¡Espero que esta herramienta te sea útil para el análisis de notas!
