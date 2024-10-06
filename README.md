# Flask User authentication

This is a simple Flask registration portal that demonstrates user authentication with registration and login functionality using MySQL as the database.

## Features

- User registration with email and username
- Secure password storage using bcrypt
- User login with session management
- Input validation for registration and login forms

## Technologies Used

- Flask
- Flask-MySQLdb
- Flask-Bcrypt
- MySQL
- HTML/CSS for front-end templates
- Regular expressions for input validation

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.x
- MySQL Server
- pip (Python package manager)

## Installation

1. **Clone the Repository**

2. **Create a virtual environment**
   git clone https://github.com/ranaNasmin/flask-user-authentication.git
   cd flask-user-authentication
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3.  **install dependencies**
   pip install Flask Flask-MySQLdb Flask-Bcrypt

4. **Set up the Database**
    Create a new database in MySQL (e.g., testdb).
    Create a table named xlogin with the following structure:

CREATE TABLE xlogin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
); 

5.**Update Database configuration**
Open the app.py file and update the MySQL connection settings:

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'testdb'

6. **Running the application**
To run the application, execute the following command:

python app.py
