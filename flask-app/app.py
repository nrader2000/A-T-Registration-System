#base imports
import sqlite3
from flask import Flask, render_template, redirect, request, url_for, flash, Response

# basic setup
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'

# db setup
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# user variable
user_name = ''

#--------route and page function setup---------
#index page/login page route
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
            student = conn.execute('SELECT Username FROM Students WHERE Username = ?;',[username]).fetchone()
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
    else: #case should never happen as html form requires both these to be filled out before sending data here
        flash("Missing Credentials! Enter both username and password!")
        return redirect(url_for('index'))

#logout functionality - within the home page
@app.route('/logout')
def logout():
    return redirect(url_for('index'))

#register page route
@app.route("/register")
def register():
    return render_template('register.html')

#register new user functionality - within the register page
@app.route("/register-new-user", methods=['POST'])
def register_new_user():
    username = request.form.get('username')
    print(username)
    password = request.form.get('password')
    print(password)
    name = request.form.get('name')
    print(name)
    address = request.form.get('address')
    print(address)
    email = request.form.get('email')
    print(email)
    phone_number = request.form.get('phone')
    print(phone_number)
    if username and password and name and address and email and phone_number:
        conn = get_db_connection()
        if conn.execute('SELECT * FROM Students WHERE Username = ? OR Password = ? OR Email = ?;',(username,password,email)).fetchall():
            flash("User with given credentials already exist! Please give different credentails!")
            return redirect(url_for('register'))
        elif conn.execute('SELECT * FROM Faculty WHERE Username = ? OR Password = ? OR Email = ?;',(username,password,email)).fetchall():
            flash("User with given credentials already exist! Please give different credentails!")
            return redirect(url_for('register'))
        else:
            cur = conn.cursor()
            cur.execute('INSERT INTO Students (Username,Password,Name,Address,Phone_Number,Email) VALUES (?,?,?,?,?,?);',(username,password,name,address,phone_number,email))
            conn.commit()
            print("Successfully addded " + username + "!")
            conn.close()
            return redirect(url_for('index'))
    else: #case should never happen as html form requires both these to be filled out before sending data here
        flash("Missing Credentials! Please enter all required credentials!")
        return redirect(url_for('register'))
        
#homepage route
@app.route("/home", methods=['GET'])
def home():
    return render_template("home.html")

#class registration page route
@app.route("/class-registration")
def CR():
    return render_template("CR.html")

#academic audit page route
@app.route("/academic-audit")
def AA():
    return render_template("AA.html")

#COR page route
@app.route("/course-override-request")
def COR():
    return render_template("COR.html")

#VAC page route
@app.route("/view-available-classes")
def VAC():
    return render_template("VAC.html")

#VSSC page route
@app.route("/view-suggested-semester-classes")
def VSSC():
    return render_template("VSSC.html")

#grades page route
@app.route("/view-grades")
def VG():
    return render_template("VG.html")

#transcript page route
@app.route("/view-transcript-information")
def VTI():
    return render_template("VTI.html")

#student info page route
@app.route("/view-student-information")
def VSI():
    return render_template("VSI.html")

#RFG page route
@app.route("/register-for-graduation")
def RFG():
    return render_template("RFG.html")

@app.route("/db-test")
def dbtest():
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM Courses').fetchall()
    conn.close()
    return render_template("db-test.html",courses=courses)