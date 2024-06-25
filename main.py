import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from PIL import Image
import pytesseract
import io  # Importar el módulo io
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, NamedStyle
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
# Importar las funciones de init_db.py
from init_db import insert_docente, insert_puntuacion


# Crear una lista para almacenar los reportes de resultados anteriores
reportes_anteriores = []

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




# Función para generar el DataFrame formateado para el Excel
def create_formatted_dataframe(session_state):
    # Aquí debes calcular la puntuación total basada en tu lógica de aplicación
    # Esto es solo un ejemplo basado en las puntuaciones y los criterios que mencionaste
    total_score = sum([
        session_state.get('educacion_superior', 0),
        session_state.get('experiencia_profesional', 0),
        session_state.get('grado_academico', 0),
        session_state.get('investigaciones_publicaciones', 0),
        session_state.get('ejercicio_docencia', 0)
    ])

    # Crear el DataFrame con las secciones que has mencionado y las puntuaciones calculadas
    df_puntuaciones = pd.DataFrame({
        'Sección': [
            'Educación Superior', 'Experiencia Profesional', 'Grado Académico', 
            'Investigaciones y Publicaciones', 'Ejercicio de la Docencia', 'Total'
        ],
        'Puntuación': [
            session_state.get('educacion_superior', 0),
            session_state.get('experiencia_profesional', 0),
            session_state.get('grado_academico', 0),
            session_state.get('investigaciones_publicaciones', 0),
            session_state.get('ejercicio_docencia', 0),
            total_score  # Puntuación total
        ]
    })
    
    # Añadir las 3 materias principales al final del DataFrame si es necesario
    if 'top_materias' in session_state:
        for materia in session_state['top_materias']:
            df_puntuaciones = df_puntuaciones.append({'Sección': materia, 'Puntuación': session_state['top_materias'][materia]}, ignore_index=True)
    
    return df_puntuaciones

# Supongamos que esta es la información recopilada de la aplicación Streamlit
def create_detailed_dataframe():
    # Aquí puedes agregar toda la información que necesitas en tu reporte
    # Utiliza las variables globales o de sesión si es necesario para obtener los datos
    detailed_data = {
        'Nombre del Postulante': [st.session_state.get('nombre_postulante', '')],
        'Edad': [st.session_state.get('edad_postulante', '')],
        'Asignatura Aplicada': [st.session_state.get('asignatura_aplicada', '')],
        'Carrera Deseada': [st.session_state.get('carrera_deseada', '')],
        # ... Más datos según tu aplicación ...
    }
    return pd.DataFrame(detailed_data)

# Función modificada para generar el enlace de descarga de Excel
def get_table_download_link(df, postulant_name):
    """Genera un enlace de descarga para el DataFrame de pandas, formateado como el Excel deseado."""
    towrite = BytesIO()
    writer = pd.ExcelWriter(towrite, engine='openpyxl')
    df.to_excel(writer, index=False, header=True)  # Asegúrate de incluir el encabezado si es necesario
    
    # Aplicar estilos personalizados
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    header_font = Font(bold=True)
    header_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
    header_alignment = Alignment(horizontal='center')
    header_border = Border(bottom=Side(style='thin'))

    for cell in worksheet["1:1"]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = header_border

    # Formateo adicional, como ajuste de tamaños de columna
    column_widths = {'A': 25, 'B': 10, 'C': 20, 'D': 15}
    for column, width in column_widths.items():
        worksheet.column_dimensions[column].width = width

    # IMPORTANTE: Aquí usamos writer.close() en lugar de writer.save()
    writer.close()  # Cierra el writer y guarda el contenido en el buffer 'towrite'
    towrite.seek(0)  # Vuelve al principio del buffer para leer el contenido
    b64 = base64.b64encode(towrite.read()).decode()  # Codifica el contenido del buffer para la descarga
    
    # Nombre del archivo con el nombre del postulante
    file_name = f"Reporte_{postulant_name}.xlsx"

    return f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">Descargar archivo excel</a>'

    # Crear el DataFrame con la información recopilada
    df_puntuaciones = pd.DataFrame(data)

    # En tu aplicación de Streamlit, cuando esté listo para la descarga
    st.markdown(get_table_download_link(df_puntuaciones, st.session_state.get('nombre_postulante', '')), unsafe_allow_html=True)

# Función para extracción de texto (ajusta según tu implementación de OCR)
def extract_text_from_image(image_data):
    return pytesseract.image_to_string(Image.open(image_data))


# Suponiendo que esta es la lógica de tu función de cálculo de puntuación
def calcular_puntuacion_materia(texto_cv, años_exp, grado, diplomados, certificaciones, materia, 
                                educacion_superior, experiencia_profesional, grado_academico,
                                investigaciones_publicaciones, ejercicio_docencia, 
                                info_adicional_puntos):
    puntuacion = 0
    texto_cv_min = texto_cv.lower()

    # Puntuación basada en palabras clave
    for palabra in palabras_clave.get(materia, []):
        puntuacion += texto_cv_min.count(palabra.lower())

    # Puntuación basada en grado académico, años de experiencia, diplomados y certificaciones
    grado_puntos = pesos[materia].get(grado, 0) if materia in pesos else 0
    años_exp_puntos = años_exp * pesos[materia].get("Años de experiencia", 0.5) if materia in pesos else 0
    diplomados_puntos = diplomados * 0.5
    certificaciones_puntos = certificaciones * 0.5

    # Sumar puntos de los campos adicionales
    puntuacion += educacion_superior + experiencia_profesional + grado_academico
    puntuacion += investigaciones_publicaciones + ejercicio_docencia

    # Sumar puntos de la información adicional del candidato
    puntuacion += info_adicional_puntos

    # Sumar todos los puntos
    puntuacion += grado_puntos + años_exp_puntos + diplomados_puntos + certificaciones_puntos

    return puntuacion




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
        

        # Recolección y almacenamien        st.session_state['nombre_postulante'] = st.text_input("Nombre y Apellidos del Postulante", key='nombre_postulante')
        st.text_input("Nombre y Apellidos del Postulante", key='nombre_postulante')
        st.number_input("Edad", min_value=18, max_value=100, step=1, key='edad_postulante')
        st.text_input("Asignatura", key='asignatura_aplicada')
        st.text_input("Carrera", key='carrera_deseada')
        st.session_state['años_de_experiencia'] = st.number_input('Años de Experiencia', min_value=0)
        st.session_state['grado_académico'] = st.selectbox('Grado Académico', ['Doctorado', 'Maestría', 'Licenciatura', 'Diplomado', 'Ninguno'])
        st.session_state['diplomados'] = st.number_input('Número de Diplomados', min_value=0)
        st.session_state['certificaciones'] = st.number_input('Número de Certificaciones', min_value=0)
        
        # Sección de Evaluación del Candidato
        st.subheader("Evaluación del Candidato")
        educacion_superior = st.slider("Educación Superior (0-12 puntos)", 0, 12, 0)
        experiencia_profesional = st.slider("Experiencia Profesional y Docencia (0-12 puntos)", 0, 12, 0)
        grado_academico = st.slider("Grado Académico Alcanzado (0-24 puntos)", 0, 24, 0)
        investigaciones_publicaciones = st.slider("Investigaciones y Publicaciones (0-15 puntos)", 0, 15, 0)
        ejercicio_docencia = st.slider("Ejercicio de la Docencia (0-9 puntos)", 0, 9, 0)




    if st.button('Confirmar Información'):
        # Aquí guardas los datos en la base de datos y asignas el docente_id
        docente_id = insert_docente(st.session_state.get('nombre_postulante', ''), 
                                    st.session_state.get('experiencia_profesional', 0), 
                                    st.session_state.get('grado_academico', ''),
                                    st.session_state.get('diplomados', 0),
                                    st.session_state.get('certificaciones', 0))
        st.session_state['docente_id'] = docente_id
        st.success("Información del docente guardada correctamente.")
    
     #Sección de Evaluación de Personalidad
        # Categorías de personalidad y estilo de enseñanza
categorias = {
    "Empatía": [
        "Capacidad para entender emociones ajenas", 
        "Responder adecuadamente a las necesidades emocionales de los estudiantes",
        "Mantener una actitud comprensiva ante los problemas de los estudiantes",
        "Reconocer y apoyar la diversidad emocional y cultural en el aula",
        "Desarrollar relaciones de confianza con los estudiantes"
    ],
    "Paciencia": [
        "Manejar con calma las interrupciones en clase",
        "Mantener la serenidad con estudiantes desafiantes",
        "Dar tiempo a los estudiantes para entender nuevos conceptos",
        "Permanecer paciente durante procesos de aprendizaje lentos",
        "Gestionar las expectativas propias y de los estudiantes de manera realista"
    ],
    "Comunicación": [
        "Explicar conceptos complejos de manera clara",
        "Fomentar la participación activa en clase",
        "Comunicarse eficazmente con padres y colegas",
        "Utilizar diversos medios y tecnologías para mejorar la comunicación",
        "Escuchar activamente y dar feedback constructivo"
    ],
    "Liderazgo": [
        "Motivar a los estudiantes hacia objetivos comunes",
        "Gestionar el aula de manera efectiva",
        "Tomar iniciativas para proyectos y actividades",
        "Fomentar un ambiente de respeto mutuo y colaboración",
        "Ser un modelo a seguir en cuanto a ética y valores"
    ],
    "Creatividad": [
        "Incorporar métodos innovadores en la enseñanza",
        "Resolver problemas de manera creativa",
        "Adaptarse a diferentes estilos de aprendizaje",
        "Desarrollar y utilizar recursos creativos para el aprendizaje",
        "Fomentar la creatividad y el pensamiento crítico en los estudiantes"
    ],
    "Adaptabilidad": [
        "Ajustarse a cambios y desafíos inesperados en el aula",
        "Manejar situaciones estresantes con flexibilidad",
        "Adaptar las estrategias de enseñanza a las necesidades cambiantes de los estudiantes",
        "Ser receptivo a nuevas ideas y enfoques pedagógicos",
        "Mantener una actitud positiva frente a la incertidumbre y el cambio"
    ],
    "Organización": [
        "Planificar y organizar el contenido del curso de manera eficiente",
        "Gestionar el tiempo de clase de forma efectiva",
        "Mantener registros y documentación ordenados y actualizados",
        "Establecer y seguir rutinas que faciliten el aprendizaje",
        "Priorizar tareas y responsabilidades para maximizar el rendimiento"
    ]
}

# Generar preguntas
for categoria, preguntas in categorias.items():
    st.markdown(f"#### {categoria}")
    for pregunta in preguntas:
        st.slider(pregunta, 1, 5, 3)

# Botón para enviar las respuestas
if st.button('Evaluar Personalidad y Estilo de Enseñanza'):
    # Aquí puedes procesar y almacenar las respuestas
    st.success("Evaluación de personalidad completada.")
        

st.title("Evaluación de Competencias Docentes")

resultados = {}
for categoria, preguntas in categorias.items():
    st.subheader(categoria)
    puntaje_total = 0
    for pregunta in preguntas:
        puntaje = st.slider(pregunta, 1, 5, key=pregunta)
        puntaje_total += puntaje
    promedio = puntaje_total / len(preguntas)
    resultados[categoria] = promedio
if st.button('Evaluar'):
    for categoria, promedio in resultados.items():
        st.write(f"Categoría: {categoria}, Puntuación Promedio: {promedio:.2f}")

        # Interpretación y recomendaciones
        if promedio >= 4:
            st.markdown(f"**Excelente en {categoria}**: Tus respuestas indican que posees habilidades excepcionales en esta área. Continúa fortaleciendo y compartiendo estas habilidades con otros.")
        elif 2.5 <= promedio < 4:
            st.markdown(f"**Competente en {categoria}**: Muestras habilidades adecuadas en esta área, pero hay espacio para mejorar. Considera explorar nuevas estrategias y técnicas para fortalecer esta competencia.")
        else:
            st.markdown(f"**Desarrollo necesario en {categoria}**: Parece que esta es un área en la que podrías mejorar. Busca oportunidades de desarrollo profesional y recursos que te ayuden a crecer en esta área.")

# Nota: Este es un esquema simplificado. Puedes personalizar las respuestas y recomendaciones según las necesidades específicas del contexto educativo.



elif opcion == 'Ver Resultados':
    if 'docente_id' in st.session_state:

        # Incluir aquí la evaluación de competencias docentes
        st.subheader("Evaluación de Competencias Docentes")

        # Ejemplo de cómo podrían presentarse las preguntas de evaluación
        evaluacion_competencias = {categoria: st.slider(categoria, 0, 5, 0) for categoria in categorias}
        st.session_state['evaluacion_competencias'] = evaluacion_competencias

        if st.button('Evaluar Competencias'):
            # Calcula puntos adicionales basados en la información del candidato
            info_adicional_puntos = (st.session_state.get('educacion_superior', 0) +
                                     st.session_state.get('experiencia_profesional', 0) +
                                     st.session_state.get('grado_academico', 0) +
                                     st.session_state.get('investigaciones_publicaciones', 0) +
                                     st.session_state.get('ejercicio_docencia', 0))

            # Cálculo de puntuaciones utilizando las variables
            puntuaciones = {
                materia: calcular_puntuacion_materia(
                    st.session_state['extracted_text'],
                    st.session_state.get('años_de_experiencia', 0),
                    st.session_state.get('grado_académico', 'Ninguno'),
                    st.session_state.get('diplomados', 0),
                    st.session_state.get('certificaciones', 0),
                    materia,
                    st.session_state.get('educacion_superior', 0),
                    st.session_state.get('experiencia_profesional', 0),
                    st.session_state.get('grado_academico', 0),
                    st.session_state.get('investigaciones_publicaciones', 0),
                    st.session_state.get('ejercicio_docencia', 0),
                    info_adicional_puntos
                )
                for materia in materias
            }
            st.session_state['puntuaciones'] = puntuaciones
            st.success("Competencias evaluadas y guardadas en la base de datos.")

            # Crear el DataFrame con puntuaciones para visualización y descarga
            df_puntuaciones = pd.DataFrame(list(puntuaciones.items()), columns=['Materia', 'Puntuación'])
            st.write(df_puntuaciones)

            # Generar el gráfico de barras para las puntuaciones
            fig, ax = plt.subplots()
            ax.barh(df_puntuaciones['Materia'], df_puntuaciones['Puntuación'])
            plt.xlabel('Puntuación')
            plt.ylabel('Materia')
            plt.title('Puntuación por Materia')
            st.pyplot(fig)

             # Crear un DataFrame con la información relevante para el reporte
            df_reporte = pd.DataFrame({
             'Nombre del Postulante': [st.session_state.get('nombre_postulante', '')],
             'Edad': [st.session_state.get('edad_postulante', '')],
             'Asignatura Aplicada': [st.session_state.get('asignatura_aplicada', '')],
             'Carrera Deseada': [st.session_state.get('carrera_deseada', '')]
            })

            # Generar el enlace de descarga para el DataFrame df_puntuaciones
            st.markdown(get_table_download_link(df_puntuaciones), unsafe_allow_html=True)

            # Añadir las puntuaciones al DataFrame del reporte
            df_reporte = pd.concat([df_reporte, df_puntuaciones], axis=1)

            # Añadir el reporte a la lista de reportes anteriores
            reportes_anteriores.append(df_reporte)


            # Mostrar las 3 materias principales
            top_materias = df_puntuaciones.nlargest(3, 'Puntuación')
            st.write("Las top 3 materias para las cuales el docente sería más apto son:")
            st.table(top_materias)

            # Proporcionar retroalimentación basada en las puntuaciones
            for index, row in top_materias.iterrows():
                st.write(f"Para la materia {row['Materia']}, la puntuación obtenida es {row['Puntuación']}.")

            # Definición del umbral de aceptación
            umbral_de_aceptacion = 3  # por ejemplo, esto podría ser el puntaje mínimo aceptable

            materias_aceptadas = df_puntuaciones[df_puntuaciones['Puntuación'] >= umbral_de_aceptacion]
            if not materias_aceptadas.empty:
                st.write("El docente cumple con el umbral de aceptación para las siguientes materias:")
                st.table(materias_aceptadas)
            else:
                st.write("El docente no cumple con el umbral de aceptación para ninguna materia.")

