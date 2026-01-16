import sqlite3

conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Crear la tabla con los campos correctos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        nombre TEXT,
        apellido TEXT,
        password_hash TEXT
    )
''')

conn.commit()
conn.close()



from flask import Flask, request, render_template
import sqlite3
import hashlib
import os

app = Flask(__name__)
DATABASE = 'usuarios.db'

# Crear la base de datos si no existe
def init_db():
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            conn.execute('''
                CREATE TABLE usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    password_hash TEXT NOT NULL
                );
            ''')
            print("Base de datos creada.")

# Hash de contraseña
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Página principal
@app.route("/")
def home():
    return render_template("index.html")

# Registrar usuario
@app.route("/registrar", methods=["POST"])
def registrar():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    password = request.form['password']

    password_hashed = hash_password(password)

    with sqlite3.connect(DATABASE) as conn:
        conn.execute("INSERT INTO usuarios (nombre, apellido, password_hash) VALUES (?, ?, ?)",
                     (nombre, apellido, password_hashed))

    return "✅ Usuario registrado con éxito."

# Validar usuario
@app.route("/validar", methods=["POST"])
def validar():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    password = request.form['password']
    password_hashed = hash_password(password)

    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE nombre=? AND apellido=? AND password_hash=?",
                    (nombre, apellido, password_hashed))
        usuario = cur.fetchone()

    if usuario:
        return "✅ Usuario validado correctamente."
    else:
        return "❌ Usuario o contraseña incorrecta."

if __name__ == "__main__":
    init_db()
    app.run(port=5800, debug=True)
