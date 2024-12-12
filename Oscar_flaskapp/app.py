from flask import Flask, send_from_directory, render_template, request, redirect, url_for, flash
from datetime import datetime
import random
import sqlite3

STATIC_FILES = "static"
DINAMIC_FILES = "templates"
app = Flask(__name__, static_folder="static")

# Se establece una clave secreta para los mensajes flash
app.secret_key = 'tu_clave_secreta'

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# @app.route("/nosotros")
# def sobre():
#     return send_from_directory(STATIC_FILES, "aboutus.html")

# @app.route("/contact")
# def contact():
#     return send_from_directory(STATIC_FILES, "contact.html")

# @app.route("/dynamic")
# def dinamica1():
#     apellido = "Alvarez"
#     fecha = datetime.now()
#     nombres = ["Oscar", "Jon", "Alex", "Ender"]
#     aleatorio = random.choice(nombres)
#     return render_template("dinamico1.html", nombre = aleatorio, apellido = apellido, fecha = fecha)

@app.route("/admin/usuarios")
def verUsuarios():
    conn = sqlite3.connect('flaskapp.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    usuarios = cursor.fetchall()

    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        phone = request.form["phone"]

        conn = sqlite3.connect('flaskapp.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ? AND phone = ?", (email, phone))
        user = cursor.fetchone()

        conn.close()

        if user:
            flash("Iniciaste sesión correctamente.", "success")
            return redirect(url_for('dashboard', user_id=user['id']))
        else:
            flash("Correo electrónico o teléfono incorrecto. Intenta de nuevo.", "error")

    return render_template('login.html')


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        phone = request.form["phone"]

        conn = sqlite3.connect('flaskapp.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)",
                       (first_name, last_name, email, phone))
        conn.commit()

        conn.close()

        flash("Usuario registrado exitosamente. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for('login'))

    return render_template('registro.html')

@app.route("/dashboard/<int:user_id>")
def dashboard(user_id):
    conn = sqlite3.connect('flaskapp.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    conn.close()

    return render_template('dashboard.html', user=user)

@app.route("/borrar/<int:user_id>")
def borrar_usuario(user_id):
    conn = sqlite3.connect('flaskapp.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()

    conn.close()

    return redirect(url_for('verUsuarios'))

if __name__ == "__main__":
    app.run()
