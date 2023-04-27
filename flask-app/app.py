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

# user global variable
user = []
semester = []

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
        if conn.execute('SELECT * FROM Students WHERE Username = ? AND Password = ?;',
                        [username,password]).fetchone():
            student = conn.execute('SELECT Username FROM Students WHERE Username = ?;',
                                   [username]).fetchone()
            for i in student:
                user.append(i)
            conn.close()
            return redirect(url_for('home'))
        elif conn.execute('SELECT * FROM Faculty WHERE Username = ? AND Password = ?;',
                          [username,password]).fetchone():
            faculty = conn.execute('SELECT Username FROM Faculty WHERE Username = ?;',
                                   [username]).fetchone()
            for i in faculty:
                user.append(i)
            conn.close()
            return redirect(url_for('home'))
        elif conn.execute('SELECT * FROM Admins WHERE Username = ? AND Password = ?;',
                          [username,password]).fetchone():
            admin = conn.execute('SELECT Username FROM Admins WHERE Username = ?;',
                                 [username]).fetchone()
            for i in admin:
                user.append(i)
            conn.close()
            return redirect(url_for('home',admin=admin))
        else:
            flash("Invalid Credentials! Please Try Again!")
            return redirect(url_for('index'))
    else: #case should never happen as html form requires both these 
          #to be filled out before sending data here
        flash("Missing Credentials! Enter both username and password!")
        return redirect(url_for('index'))

#logout functionality - within the home page
@app.route('/logout')
def logout():
    print("Logging out " + user[0])
    user.remove(user[0])
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
        if conn.execute('SELECT * FROM Students WHERE Username = ? OR Password = ? OR Email = ?;',[username,password,email]).fetchall():
            flash("User with given credentials already exist! Please give different credentails!")
            return redirect(url_for('register'))
        elif conn.execute('SELECT * FROM Faculty WHERE Username = ? OR Password = ? OR Email = ?;',[username,password,email]).fetchall():
            flash("User with given credentials already exist! Please give different credentails!")
            return redirect(url_for('register'))
        else:
            cur = conn.cursor()
            cur.execute('INSERT INTO Students (Username,Password,Name,Address,Phone_Number,Email) VALUES (?,?,?,?,?,?);',[username,password,name,address,phone_number,email])
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
    if user:
        user_name = user[0]
        print("Logging in as " + user_name)
        if user_name:
            conn = get_db_connection()
            if conn.execute('SELECT * FROM Students WHERE Username = ?;',[user_name]).fetchone():
                user_info = conn.execute("SELECT * FROM Students WHERE Username = ?;",[user_name]).fetchone()
            elif conn.execute('SELECT * FROM Faculty WHERE Username = ?;',[user_name]).fetchone():
                user_info = conn.execute("SELECT * FROM Faculty WHERE Username = ?;",[user_name]).fetchone()
            elif conn.execute('SELECT * FROM Admins WHERE Username = ?;',[user_name]).fetchone():
                user_info = conn.execute("SELECT * FROM Admins WHERE Username = ?;",[user_name]).fetchone()
            else: #case should not happen as login is required for functionality to work, redirects to login page if user_name is not anywhere
                print("error on finding proper creds")
                return redirect(url_for('index'))
            conn.close()
            return render_template("home.html",user_info=user_info)
    else: #should never happen as the login is required to get this page to work, error will appear if not properly logged in
        return redirect(url_for('index'))

#class registration page route
@app.route("/class-registration", methods=['GET'])
def CR():
    semester_select = request.args.get('semester')
    return render_template("CR.html",semester=semester_select)

#submit semester functionality - within class registation page
@app.route("/submit-semester", methods=['POST'])
def submit_semester():
    semester_select = request.form.get('semester')
    flash("Selected " + semester_select + "!")
    if semester:
        semester.remove(semester[0])
        semester.append(semester_select)
    else:
        semester.append(semester_select)
    return redirect(url_for('CR',semester=semester_select))

#academic audit page route
@app.route("/academic-audit")
def AA():
    return render_template("AA.html")

#COR page route
@app.route("/course-override-request")
def COR():
    return render_template("COR.html")

#VAC page route
@app.route("/view-available-classes", methods=['GET'])
def VAC():
    semester_select = request.args.get('semester')
    if semester_select:
        conn = get_db_connection()
        courses = conn.execute('SELECT * FROM Courses WHERE Semester = ?;',[semester_select]).fetchall()
        conn.close()
    else:
        flash("No semester selected! Please choose a semester and submit!")
        return redirect(url_for('CR'))
    return render_template("VAC.html",courses=courses)

#VSSC page route (selects major here)
@app.route("/view-suggested-semester-classes")
def VSSC():
    semester_select = request.args.get('semester')
    if semester_select:
        pass
    else:
        flash("No semester selected! Please choose a semester and submit!")
        return redirect(url_for('CR'))
    return render_template("VSSC.html")

#Second VSSC page route (actual classes appear here)
@app.route("/VSSC_2",methods=['GET'])
def VSSC_2():
    semester_select = request.args.get('semester')
    major_select = request.args.get('major')
    if major_select:
        conn = get_db_connection()
        courses = conn.execute('SELECT * FROM Courses WHERE Semester = ? AND Major = ?;',
                               [semester_select,major_select]).fetchall()
        conn.close
        if not courses:
            flash("No current classes under these specifications at this time!")
    else:
        flash("Missing major! Please choose a major!")
        return redirect(url_for('VSSC'))
    return render_template("VSSC_2.html",courses=courses)

#submit major functionality - within VSSC page
@app.route("/submit-major", methods=['POST'])
def submit_major():
    semester_select = semester[0]
    print("With " + semester_select + "...")
    major_select = request.form.get('major')
    print("Selected " + major_select + "...")
    return redirect(url_for('VSSC_2',semester=semester_select,major=major_select))

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
    user_name = user[0]
    print("Accessing " + user_name + "'s Records")
    if user_name:
        conn = get_db_connection()
        if conn.execute('SELECT * FROM Students WHERE Username = ?;',[user_name]).fetchone():
            user_info = conn.execute("SELECT * FROM Students WHERE Username = ?;",[user_name]).fetchone()
        elif conn.execute('SELECT * FROM Faculty WHERE Username = ?;',[user_name]).fetchone():
            user_info = conn.execute("SELECT * FROM Faculty WHERE Username = ?;",[user_name]).fetchone()
        elif conn.execute('SELECT * FROM Admins WHERE Username = ?;',[user_name]).fetchone():
            user_info = conn.execute("SELECT * FROM Admins WHERE Username = ?;",[user_name]).fetchone()
        else: #case should not happen as login is required for functionality to work, redirects to login page if user_name is not anywhere
            print("error on finding proper creds")
            return redirect(url_for('index'))
        conn.close()
        return render_template("VSI.html",user_info=user_info)
    else: #should never happen as the login is required to get this page to work, error will appear if not properly logged in
        print("no user_name value")
        return redirect(url_for('index'))

#RFG page route
@app.route("/register-for-graduation")
def RFG():
    return render_template("RFG.html")