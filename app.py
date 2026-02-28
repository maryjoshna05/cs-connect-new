from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "csconnectsecret"

DATABASE = "csconnect.db"

# ----------------------------
# CREATE DATABASE TABLE
# ----------------------------
def init_db():
    conn = sqlite3.connect("csconnect.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            user_id TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# ----------------------------
# WEBSITE ROUTES (YOUR PAGES)
# ----------------------------

@app.route('/')
def home():
    return render_template('indexn.html')

@app.route('/faculty')
def faculty():
    return render_template('faculty/faculty.html')

@app.route('/about-cse')
def about_cse():
    return render_template('about/about-cse.html')

@app.route('/about-aisat')
def about_aisat():
    return render_template('about/about-aisat.html')

@app.route('/academics')
def academics():
    return render_template('academics/academics.html')

@app.route('/library')
def library():
    return render_template('library/library.html')

# ----------------------------
# REGISTER
# ----------------------------
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        user_id = request.form["user_id"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO users (name, email, user_id, password)
                VALUES (?, ?, ?, ?)
            """, (name, email, user_id, password))

            conn.commit()
            flash("Account Created Successfully!", "success")

        except sqlite3.IntegrityError:
            flash("Email or User ID already exists!", "danger")

        finally:
            conn.close()

        return redirect(url_for("login"))   # 🔥 moved outside try

    return render_template("register.html")
# ----------------------------
# LOGIN
# ----------------------------
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and user[4] == password:
            session["user_id"] = user[0]
            session["name"] = user[1]

            flash("Login successful!", "success")
            return redirect(url_for("home"))

        else:
            flash("Invalid email or password!", "danger")

    return render_template("login.html")
# ----------------------------
# LOGOUT
# ----------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("login"))

# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    init_db()   
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)