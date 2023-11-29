import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from PIL import Image
import pytesseract
import io  # Importar el módulo io


# Definiciones de tus variables y funciones

materias = [
    "Programación Web", "Animación Digital", "Fundamentos de Desarrollo de Software",
    "Procesamiento Digital de Imágenes", "Fundamentos de Ciencias de la Computación",
    "Redes y Comunicación de Datos", "Programación", "Data Warehousing",
    "Estadística Computacional", "Inglés Técnico", "Matemática Computacional",
    "Metodología de la Investigación", "Base de Datos", "Electrónica Digital Aplicada",
    "Realidad Virtual y Aumentada", "Software Quality Assurance", "Sistemas Operativos",
    "Tecnologías Emergentes", "Management Information Systems", "Auditoría y Seguridad Informática",
    "Software Project Management", "Robótica", "Sistemas Distribuidos", "Programación Móvil",
    "Taller de Sistemas", "Práctica Profesional", "Game Development", "Ingeniería de Software",
    "Proyecto de Sistemas", "Seminario de Modalidad de Titulación"
]

# Definición de palabras clave por materia
palabras_clave = {
    "Programación Web": ["html", "css", "javascript", "php", "frontend", "backend", "fullstack", "framework", "api"],
    "Animación Digital": ["animación", "3d", "render", "blender", "after effects", "motion graphics", "rigging"],
    "Fundamentos de Desarrollo de Software": ["algoritmo", "pseudocódigo", "UML", "patrones", "metodologías ágiles"],
    "Procesamiento Digital de Imágenes": ["filtrado", "segmentación", "histograma", "convolución", "transformación"],
    "Fundamentos de Ciencias de la Computación": ["algoritmo", "complejidad", "teoría", "autómata", "lógica"],
    "Redes y Comunicación de Datos": ["protocolo", "TCP/IP", "routing", "switching", "LAN", "WAN"],
    "Programación": ["lenguaje", "algoritmo", "estructura de datos", "funciones", "objetos", "compilador"],
    "Data Warehousing": ["data", "base de datos", "SQL", "almacenamiento", "consulta", "data mining"],
    "Estadística Computacional": ["variables", "probabilidad", "distribuciones", "hipótesis", "regresión"],
    "Inglés Técnico": ["inglés", "lectura", "escritura", "comprensión", "vocabulario técnico"],
    "Matemática Computacional": ["matrices", "vectores", "cálculo", "ecuaciones", "transformaciones"],
    "Metodología de la Investigación": ["investigación", "hipótesis", "variables", "método científico", "publicación"],
    "Base de Datos": ["SQL", "NoSQL", "relacional", "normalización", "consulta", "schema", "indexación"],
    "Electrónica Digital Aplicada": ["circuitos", "transistores", "microcontroladores", "FPGA", "señales"],
    "Realidad Virtual y Aumentada": ["VR", "AR", "headset", "simulación", "inmersión", "3D"],
    "Software Quality Assurance": ["QA", "testing", "pruebas", "bugs", "integración continua"],
    "Sistemas Operativos": ["kernel", "procesos", "hilos", "memoria", "Linux", "Windows", "UNIX"],
    "Tecnologías Emergentes": ["AI", "IoT", "blockchain", "cloud", "5G", "edge computing"],
    "Management Information Systems": ["gestión", "ERP", "CRM", "análisis de negocio", "BI"],
    "Auditoría y Seguridad Informática": ["criptografía", "firewall", "malware", "penetration testing", "ciberseguridad"],
    "Software Project Management": ["scrum", "kanban", "waterfall", "PMI", "stakeholder"],
    "Robótica": ["sensores", "actuadores", "robot", "autónomo", "ROS"],
    "Sistemas Distribuidos": ["microservicios", "API", "RPC", "escalabilidad", "concurrencia"],
    "Programación Móvil": ["iOS", "Android", "app", "mobile", "flutter", "react native"],
    "Taller de Sistemas": ["integración", "proyecto", "demostración", "desarrollo", "implementación"],
    "Práctica Profesional": ["empresa", "desarrollo real", "equipo", "entorno laboral", "feedback"],
    "Game Development": ["juego", "motor gráfico", "Unity", "Unreal", "gamificación", "3D"],
    "Ingeniería de Software": ["SDLC", "requisitos", "diseño", "implementación", "mantenimiento"],
    "Proyecto de Sistemas": ["desarrollo", "entrega", "iteración", "cliente", "solución"],


# Materias de Medicina
"Cirugía General": ["laparoscopia", "anestesia", "hemostasia", "bisturí", "sutura"],
"Cardiología": ["corazón", "arterias", "vejiga", "ECG", "cateterismo"],
"Pediatría": ["niño", "vacunación", "crecimiento", "desarrollo", "lactancia"],
"Neurología": ["cerebro", "neurona", "esclerosis", "convulsión", "migraña"],
"Oncología": ["cáncer", "quimioterapia", "radioterapia", "tumor", "biopsia"],

    # ... (y así sucesivamente para las demás materias de medicina)

# Materias de Derecho
"Derecho Penal": ["delito", "pena", "acusación", "defensa", "juicio"],
"Derecho Civil": ["contrato", "propiedad", "herencia", "divorcio", "adopción"],
"Derecho Laboral": ["empleador", "empleado", "contrato", "despido", "sindicato"],
"Derecho Ambiental": ["contaminación", "sostenibilidad", "recursos naturales", "legislación", "impacto ambiental"],
"Derecho Internacional": ["tratado", "soberanía", "organizaciones internacionales", "leyes extranjeras", "diplomacia"],

    # ... (y así sucesivamente para las demás materias de derecho)


    # Materias de Ingeniería Civil
"Estructuras": ["concreto", "acero", "mampostería", "carga", "resistencia"],
"Geotecnia": ["suelo", "cimentación", "permeabilidad", "compresibilidad", "ensayos"],
"Hidráulica": ["flujo", "caudal", "presión", "tubería", "bombas"],

# Materias de Comunicación
"Periodismo": ["noticias", "entrevista", "reportaje", "ética", "medios"],
"Relaciones Públicas": ["comunicación", "imagen", "marca", "evento", "prensa"],
"Producción Audiovisual": ["cámara", "edición", "guion", "sonido", "iluminación"],





}
pesos = {
    # ... Diccionario completo de tus pesos por materia ...
"Programación Web": {"Doctorado": 5, "Maestría": 4, "Licenciatura": 3, "Diplomado": 2, "Años de experiencia": 0.5},
    "Animación Digital": {"Doctorado": 4, "Maestría": 3, "Licenciatura": 3, "Diplomado": 2, "Años de experiencia": 0.6},
    "Fundamentos de Desarrollo de Software": {"Doctorado": 5, "Maestría": 4, "Licenciatura": 3, "Diplomado": 1, "Años de experiencia": 0.7},
    "Procesamiento Digital de Imágenes": {"Doctorado": 5, "Maestría": 3, "Licenciatura": 2, "Diplomado": 2, "Años de experiencia": 0.6},
    "Fundamentos de Ciencias de la Computación": {"Doctorado": 5, "Maestría": 4, "Licenciatura": 3, "Diplomado": 1, "Años de experiencia": 0.7},
    "Redes y Comunicación de Datos": {"Doctorado": 4, "Maestría": 4, "Licenciatura": 3, "Diplomado": 1, "Años de experiencia": 0.8},
    "Programación": {"Doctorado": 5, "Maestría": 4, "Licenciatura": 3, "Diplomado": 2, "Años de experiencia": 0.9},
    "Data Warehousing": {"Doctorado": 4, "Maestría": 3, "Licenciatura": 2, "Diplomado": 1, "Años de experiencia": 0.5},
    "Estadística Computacional": {"Doctorado": 4, "Maestría": 3, "Licenciatura": 3, "Diplomado": 2, "Años de experiencia": 0.6},
    "Inglés Técnico": {"Doctorado": 3, "Maestría": 3, "Licenciatura": 2, "Diplomado": 1, "Años de experiencia": 0.4},
    "Matemática Computacional": {"Doctorado": 5, "Maestría": 4, "Licenciatura": 3, "Diplomado": 1, "Años de experiencia": 0.6},
    "Metodología de la Investigación": {"Doctorado": 4, "Maestría": 3, "Licenciatura": 2, "Diplomado": 2, "Años de experiencia": 0.5},
    "Base de Datos": {"Doctorado": 5, "Maestría": 4, "Licenciatura": 3, "Diplomado": 2, "Años de experiencia": 0.8},
    "Electrónica Digital Aplicada": {"Doctorado": 4, "Maestría": 3, "Licenciatura": 2, "Diplomado": 2, "Años de experiencia": 0.7},



    
}



# Función auxiliar para descargar un archivo
def get_table_download_link(df):
    """Genera un enlace de descarga para el DataFrame de pandas"""
    towrite = BytesIO()
    df.to_excel(towrite, index=False, header=True)  # Se escribe en un BytesIO buffer
    towrite.seek(0)  # Se va al inicio del buffer
    b64 = base64.b64encode(towrite.read()).decode()  # Codificación en base64
    return f'<a href="data:application/octet-stream;base64,{b64}" download="puntuaciones.xlsx">Descargar archivo excel</a>'

# Función para extracción de texto (ajusta según tu implementación de OCR)
def extract_text_from_image(image_data):
    try:
        # Reinicia el puntero del buffer
        image_data.seek(0)

        # Abre la imagen con Pillow
        image = Image.open(image_data)

        # Convierte la imagen a texto usando pytesseract
        text = pytesseract.image_to_string(image)

        return text
    except IOError as e:
        # En caso de error, imprime un mensaje descriptivo
        st.error(f"Error al procesar la imagen: {e}")
        return ""




# Suponiendo que esta es la lógica de tu función de cálculo de puntuación
def calcular_puntuacion_materia(texto_cv, años_exp, grado, diplomados, certificaciones, materia):
    puntuacion = 0
    # Aquí iría la lógica de cálculo de tu puntuación...
    return puntuacion

# Función para extracción de texto (ajusta según tu implementación de OCR)
def extract_text_from_image(image_data):
    return pytesseract.image_to_string(Image.open(image_data))

# Función auxiliar para descargar un archivo
def get_table_download_link(df):
    """Genera un enlace de descarga para el DataFrame de pandas"""
    towrite = BytesIO()
    df.to_excel(towrite, index=False, header=True)  # Se escribe en un BytesIO buffer
    towrite.seek(0)  # Se va al inicio del buffer
    b64 = base64.b64encode(towrite.read()).decode()  # Codificación en base64
    return f'<a href="data:application/octet-stream;base64,{b64}" download="puntuaciones.xlsx">Descargar archivo excel</a>'

# Inicialización de la sesión para almacenar el texto extraído y las puntuaciones
if 'extracted_text' not in st.session_state:
    st.session_state['extracted_text'] = ""
if 'puntuaciones' not in st.session_state:
    st.session_state['puntuaciones'] = {}

# Aplicación Streamlit
st.title('Evaluador de Competencias Docentes')

# Opción para cambiar entre vistas
opcion = st.sidebar.radio("¿Qué deseas hacer?", ('Cargar Documento', 'Ver Resultados'), key='opcion_vista')

if opcion == 'Cargar Documento':
    # Lógica para la vista de carga de documentos
    uploaded_file = st.file_uploader("Carga tu CV o documento aquí", type=["jpg", "jpeg", "png", "pdf", "txt"])
    if uploaded_file is not None:
        image_stream = io.BytesIO(uploaded_file.read())
        extracted_text = extract_text_from_image(image_stream)
        st.session_state['extracted_text'] = extracted_text
        st.write("Texto Extraído:")
        st.text_area("Texto", extracted_text, height=150)
elif opcion == 'Ver Resultados':
    if st.session_state['extracted_text']:
        extracted_text = st.session_state['extracted_text']
        # Entradas para los datos adicionales
        años_de_experiencia = st.number_input('Años de Experiencia', min_value=0)
        grado_académico = st.selectbox('Grado Académico', ['Doctorado', 'Maestría', 'Licenciatura', 'Diplomado', 'Ninguno'])
        diplomados = st.number_input('Número de Diplomados', min_value=0)
        certificaciones = st.number_input('Número de Certificaciones', min_value=0)

        if st.button('Evaluar Competencias'):
            # Cálculo de puntuaciones y almacenamiento en el estado de la sesión
            puntuaciones = {
                materia: calcular_puntuacion_materia(
                    extracted_text,
                    años_de_experiencia,
                    grado_académico,
                    diplomados,
                    certificaciones,
                    materia
                )
                for materia in materias
            }
            st.session_state['puntuaciones'] = puntuaciones

            # Crear DataFrame con puntuaciones para visualización y descarga
            df_puntuaciones = pd.DataFrame(list(puntuaciones.items()), columns=['Materia', 'Puntuación'])
            st.write(df_puntuaciones)

            # Mostrar las puntuaciones en una tabla y en un gráfico de barras
            st.bar_chart(df_puntuaciones.set_index('Materia'))

            # Permitir al usuario descargar las puntuaciones como archivo Excel
            st.markdown(get_table_download_link(df_puntuaciones), unsafe_allow_html=True)

            # Mostrar las 3 materias principales
            top_materias = df_puntuaciones.nlargest(3, 'Puntuación')
            st.write("Las top 3 materias para las cuales el docente sería más apto son:")
            st.table(top_materias)

            # Proporcionar retroalimentación basada en las puntuaciones
            for index, row in top_materias.iterrows():
                st.write(f"Para la materia {row['Materia']}, la puntuación obtenida es {row['Puntuación']}.")
            

            # Definición del umbral de aceptación (puedes cambiar el valor según tus necesidades)
            umbral_de_aceptación = 5  # por ejemplo, esto podría ser el puntaje mínimo aceptable
                        
            # Suponiendo que 'top_materias' es un DataFrame de pandas y estás verificando el valor máximo en la columna 'Puntuación'
            if top_materias['Puntuación'].max() < umbral_de_aceptación:
                # Lógica para manejar situaciones donde la puntuación máxima es menor que el umbral de aceptación
                st.write("El docente no cumple con el umbral de aceptación para ninguna materia.")
            else:
                # Lógica para manejar situaciones donde la puntuación máxima es igual o mayor que el umbral de aceptación
                st.write("El docente cumple con el umbral de aceptación para las siguientes materias:")
                # Aquí podrías mostrar las materias que cumplen con el umbral, etc.