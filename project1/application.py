import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import requests


#print(res.json())

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
print(os.getenv("DATABASE_URL"))
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/signup", methods=['POST'])
def signup():
    if (request.method == "POST"):
            #get the username and password from the request
            username = request.form["username"]
            password = request.form["password"]

            #get the username/password data for soon to come logic
            people = db.execute("SELECT * FROM \"Accounts\";").fetchall()
            
            #We now see if we already have the user signed up
            for p in people:
                uTemp = p['username']
                pTemp = p['password']
                isloggedin = p['isloggedin']
                
                if(uTemp == username and pTemp == password):
                    #if they are signup already, we check if they are logged in already somewhere else
                    if isloggedin:
                        print("user already logged in")
                        return "user already logged in"
                    print("user logged in instead of a new account being made")

                    #if not, they can full continue to login
                    db.execute('UPDATE \"Accounts\" SET isloggedin = ' + '\'1\'' + 'WHERE username = \'' + username + '\'AND password = \'' + password + '\');')
                    db.commit()
                    return login()

            #If the user does not have an account created, we create one for them and sign them in
            insertCommand = 'INSERT INTO \"Accounts\" (username, password, isloggedin) VALUES (\'' + username + '\', \'' + password + '\', \'1\');'
            db.execute(insertCommand)
            db.commit()
            return book()

    return "not supported (please post)"

@app.route("/login")
def login():
    print("login")
    return book()


@app.route("/book", methods=['GET', 'POST'])
def book():
    if (request.method == "POST"):
        print("POST")
        user = request.form["username"]
        passw = request.form["password"]
        #print(render_template("book.html"))
        return render_template("book.html", username=user, password=passw)

    return render_template("book.html")
