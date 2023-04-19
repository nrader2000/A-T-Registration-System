import sqlite3
from flask import Flask, render_template

# basic setup
app = Flask(__name__)
app.debug = True

# run the init_db.py script
with open("init_db.py") as f:
    exec(f.read())

# db setup
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# route and page function setup
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/class-registration")
def CR():
    return render_template("CR.html")

@app.route("/academic-audit")
def AA():
    return render_template("AA.html")

@app.route("/course-override-request")
def COR():
    return render_template("COR.html")

@app.route("/view-available-classes")
def VAC():
    return render_template("VAC.html")

@app.route("/view-suggested-semester-classes")
def VSSC():
    return render_template("VSSC.html")

@app.route("/view-grades")
def VG():
    return render_template("VG.html")

@app.route("/view-transcript-information")
def VTI():
    return render_template("VTI.html")

@app.route("/view-student-information")
def VSI():
    return render_template("VSI.html")

@app.route("/register-for-graduation")
def RFG():
    return render_template("RFG.html")

@app.route("/db-test")
def dbtest():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM Students').fetchall()
    conn.close()
    return render_template("db-test.html",students=students)