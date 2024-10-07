from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors, re , os
from flask_bcrypt import Bcrypt
from flask_wtf import CSRFProtect

app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'sqluser'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'testdb'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

bcrypt=Bcrypt(app)
mysql = MySQL(app)
csrf = CSRFProtect(app)


@app.route('/')
def home():
    return render_template('home.html')


#login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and "password" in request.form:
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM xlogin WHERE email = %s", (email,))
        account = cursor.fetchone()

        if account and bcrypt.check_password_hash(account['password'], password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            msg = "You have successfully logged in"

        else:
            msg = "Invalid email or password"
        
    return render_template('login.html', msg = msg)




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
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            
            #Account doesn't exist and the form data is valid , so insert a new entry into the database.
            cursor.execute("INSERT INTO xlogin VALUE(NULL, %s,%s,%s)", (username,hashed_password,email))
            mysql.connection.commit()
            msg = "You have registered successfully"

    elif request.method == 'POST':
        msg = "Please fill the form"

    return render_template('register.html', msg=msg)




if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


