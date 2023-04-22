import sqlite3
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_login import login_user, LoginManager, login_required, logout_user

# run the init_db.py script
with open("init_db.py") as f:
    exec(f.read())

# basic setup
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'

# db setup
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#login setup
login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return

# route and page function setup
@app.route("/")
def index():
    return render_template('index.html')

#login functionality - within the index page
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    print(username)
    password = request.form.get('password')
    print(password)
    if username and password:
        conn = get_db_connection()
        if conn.execute('SELECT * FROM Students WHERE Username = ? AND Password = ?',(username,password)).fetchone():
            student = conn.execute('SELECT * FROM Students WHERE Username = ? AND Password = ?',(username,password)).fetchone()
            conn.close()
            return redirect(url_for('home',student=student))
        elif conn.execute('SELECT * FROM Faculty WHERE Username = ? AND Password = ?',(username,password)).fetchone():
            faculty = conn.execute('SELECT * FROM Faculty WHERE Username = ? AND Password = ?',(username,password)).fetchone()
            conn.close()
            return redirect(url_for('home',faculty=faculty))
        elif conn.execute('SELECT * FROM Admins WHERE Username = ? AND Password = ?',(username,password)).fetchone():
            admin = conn.execute('SELECT * FROM Admins WHERE Username = ? AND Password = ?',(username,password)).fetchone()
            conn.close()
            return redirect(url_for('home',admin=admin))
        else:
            flash("Invalid Credentials! Please Try Again!")
            return redirect(url_for('index'))

#logout functionality - within the home page
@app.route('/logout')
def logout():
    return redirect(url_for('index'))

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
    courses = conn.execute('SELECT * FROM Courses').fetchall()
    conn.close()
    return render_template("db-test.html",courses=courses)