from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import MySQLdb.cursors, re , os
from flask_bcrypt import Bcrypt


app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'sqluser'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'testdb'

bcrypt=Bcrypt(app)
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')


#login route
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST' and 'email' in request.form and "password" in request.form:
        email = request.form['email']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
        # hash = hashlib.sha1(hash.encode())
        # password = hash.hexdigest()

    # check if the username and email exist or not
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM xlogin WHERE email = %s AND password = %s", (email, hashed_password))
        account = cursor.fetchone()        

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            return " You have successfully logged in"

        else: 
            return "invalid email or password"
        
    return render_template('login.html')




@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        #check if the user exist in the db
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM xlogin WHERE username = %s AND email = %s", (username, email))
        account = cursor.fetchone()

        if account:
            msg = "Account already exists"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = "Invalid email address"
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = "Username must contain characters and numbers"
        elif not username or not password or not email:
            msg = "Please fill out the form completely"
        else:
            # hash the password
            hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
            # Account doesn't exist and the form data is valid , so insert a new entry into the database.
            cursor.execute("INSERT INTO xlogin VALUE(NULL, %s,%s,%s)", (username,hashed_password,email))
            mysql.connection.commit()
            msg = "You have registered successfully"

    elif request.method == 'POST':
        msg = "Please fill the form"

    return render_template('register.html', msg=msg)




if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


