from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="portfolio_db"
    )

# INDEX PAGE
@app.route("/")
def index():
    return render_template("index.html")

# FORM PAGE
@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            "about": request.form["about"],
            "skills": request.form["skills"],
            "languages": request.form["languages"],
            "education": request.form["education"],
            "experience": request.form["experience"],
            "certifications": request.form["certifications"],
            "projects": request.form["projects"]
        }

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO portfolio 
                (name, email, phone, about, skills, languages, education, experience, certifications, projects)
                VALUES (%(name)s, %(email)s, %(phone)s, %(about)s, %(skills)s, %(languages)s, %(education)s, %(experience)s, %(certifications)s, %(projects)s)
            """, data)
            conn.commit()
            last_id = cursor.lastrowid
            cursor.close()
            conn.close()
            return redirect(url_for("portfolio", user_id=last_id))
        except mysql.connector.Error as err:
            return f"Database error: {err}", 500

    return render_template("form.html")

# VIEW PORTFOLIO
@app.route("/portfolio/<int:user_id>")
def portfolio(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM portfolio WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        return f"Database error: {err}", 500

    if not user:
        return "Portfolio not found", 404

    return render_template("portfolio.html", user=user)


# VIEW ALL USERS
@app.route("/users")
def users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM portfolio")
        all_users = cursor.fetchall()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        return f"Database error: {err}", 500

    return render_template("users.html", users=all_users)

if __name__ == '__main__':
    app.run(debug=True)
