import sqlite3


def connect_db():
    return sqlite3.connect('db/database.db')

def init_db():
    conn = connect_db()
    c = conn.cursor()

    # Crear tabla para docentes
    c.execute('''
    CREATE TABLE IF NOT EXISTS docentes (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        experiencia INTEGER,
        grado_academico TEXT,
        diplomados INTEGER,
        certificaciones INTEGER
    )
    ''')

    # Crear tabla para puntuaciones
    c.execute('''
    CREATE TABLE IF NOT EXISTS puntuaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        docente_id INTEGER,
        materia TEXT NOT NULL,
        puntuacion INTEGER,
        FOREIGN KEY (docente_id) REFERENCES docentes (id)
    )
    ''')

    # Guardar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

def insert_docente(nombre, experiencia, grado_academico, diplomados, certificaciones):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO docentes (nombre, experiencia, grado_academico, diplomados, certificaciones) VALUES (?, ?, ?, ?, ?)", 
              (nombre, experiencia, grado_academico, diplomados, certificaciones))
    conn.commit()
    docente_id = c.lastrowid
    conn.close()
    return docente_id

def insert_puntuacion(docente_id, materia, puntuacion):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO puntuaciones (docente_id, materia, puntuacion) VALUES (?, ?, ?)", 
              (docente_id, materia, puntuacion))
    conn.commit()
    conn.close()

# Llamar a init_db al ejecutar este script para asegurarse de que las tablas estén creadas
if __name__ == "__main__":
    init_db()