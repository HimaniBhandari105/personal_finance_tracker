from flask import Flask, render_template, request, redirect, url_for, flash
from db import get_db_connection
import hashlib

app = Flask(__name__)
app.secret_key="PFT_K_E_Y"

# Home / Welcome Page
@app.route("/")
def index():
    return render_template("index.html")

# Login Page
@app.route("/login")
def login():
    return render_template("login.html")

# Signup Page
@app.route("/signup")
def signup():
    return render_template("signup.html")

# ---------- STEP 2: SIGNUP LOGIC ----------
@app.route("/signup", methods=["POST"])
def signup_post():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    # Password hashing
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user:
        flash("Email already registered!")
        return redirect(url_for("signup"))

    # Insert user
    query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, email, hashed_password))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Account created successfully! Please login.")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)