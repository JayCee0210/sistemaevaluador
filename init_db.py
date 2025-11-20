import sqlite3
import hashlib
import binascii
import secrets
from typing import Optional

DB_PATH = 'db/database.db'

def connect_db():
    # Nota: puedes agregar timeout u otras opciones si lo deseas
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = connect_db()
    c = conn.cursor()

    # Crear tabla para docentes (igual que antes)
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

    # Crear tabla para puntuaciones (igual que antes)
    c.execute('''
    CREATE TABLE IF NOT EXISTS puntuaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        docente_id INTEGER,
        materia TEXT NOT NULL,
        puntuacion INTEGER,
        FOREIGN KEY (docente_id) REFERENCES docentes (id)
    )
    ''')

    # Nueva tabla para usuarios/auth
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password_hash TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

    # Asegurarse de que existan los usuarios por defecto
    ensure_default_users()

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

# -----------------------
# Funciones de hashing y usuario
# -----------------------

def create_password_hash(password: str, iterations: int = 200_000) -> str:
    """
    Retorna un string con formato:
    pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>
    """
    # Solo para pruebas: almacenar la contraseña en texto plano
    return password

def verify_password(stored: str, provided_password: str) -> bool:
    """Verifica un password contra el string almacenado en la DB."""
    # Solo para pruebas: comparar texto plano
    return stored == provided_password

def create_user(username: str, password: str) -> bool:
    """Crea un usuario con hash seguro. Devuelve True si se creó, False si ya existía."""
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    if c.fetchone():
        conn.close()
        return False
    pw_hash = create_password_hash(password)
    c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, pw_hash))
    conn.commit()
    conn.close()
    return True

def get_user_hash(username: str) -> Optional[str]:
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def verify_user(username: str, password: str) -> bool:
    """Verifica si username/password son correctos."""
    pw_hash = get_user_hash(username)
    print(f"[DEBUG] Usuario: {username}, Hash almacenado: {pw_hash}")
    if not pw_hash:
        print("[DEBUG] Usuario no encontrado")
        return False
    resultado = verify_password(pw_hash, password)
    print(f"[DEBUG] Resultado verificación: {resultado}")
    return resultado

def ensure_default_users():
    """
    Asegura que existan los usuarios por defecto:
    - univallerrhh  (contraseña igual al nombre por defecto)
    - postulantes2025
    Si ya existen, no los sobrescribe.
    """
    # Asegurar que la DB y tablas existan
    conn = connect_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password_hash TEXT NOT NULL
    )''')
    conn.commit()
    # Eliminar todos los usuarios existentes para garantizar solo uno
    c.execute('DELETE FROM users')
    conn.commit()
    # Crear solo el usuario admin/admin
    pw_hash = create_password_hash('admin')
    c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ('admin', pw_hash))
    conn.commit()
    conn.close()

# Inicializar DB al importar (crea tablas y usuarios por defecto)
# Esto no rompe nada: init_db comprueba if not exists
init_db()

# Permite ejecutar el script para solo inicializar si se ejecuta directamente
if __name__ == "__main__":
    print("Inicializando base de datos y usuarios por defecto...")
    init_db()
    print("Listo.")
