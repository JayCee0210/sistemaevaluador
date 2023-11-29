import sqlite3

# Conectarse a la base de datos (se creará si no existe)
conn = sqlite3.connect('db/database.db')

# Crear un objeto cursor para ejecutar comandos SQL
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
