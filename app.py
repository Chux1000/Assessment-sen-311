from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SmokeyJollof32755614c0d9d4947d59fa6909cfffac18c723154c17c7ed407c015e3c2cdf20'

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ugochukwu333999",
        database="tbl_user"
    )

@app.route("/getTable", methods=['GET'])
def get_table():
    try:
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        cursor.close()
        con.close()
        table_names = [table[0] for table in tables]
        return jsonify({"tables": table_names}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            error = "All fields are required."
        else:
            hashed = generate_password_hash(password)
            
            try:
                con = get_db_connection()
                cursor = con.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed))
                con.commit()
                cursor.close()
                con.close()
                
                print(f"New user signed up with username: {username}")
                flash(f'Account created successfully for {username}!', 'success')
                return redirect(url_for("home"))
                
            except mysql.connector.Error as err:
                if err.errno == 1062:
                    error = "Username already exists. Please choose another one."
                else:
                    error = f"Database error: {err}"

    return render_template("signup.html", error=error)

@app.route("/users", methods=["GET"])
def view_users():
    try:
        con = get_db_connection()
        cursor = con.cursor(dictionary=True) 
        cursor.execute("SELECT id, username FROM users;")
        users = cursor.fetchall()
        cursor.close()
        con.close()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)