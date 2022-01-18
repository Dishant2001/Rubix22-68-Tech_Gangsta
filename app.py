from flask import Flask, request, render_template, session, url_for, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "abcd"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cashflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
APP_ROOT=os.path.dirname(os.path.abspath(__file__))

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(50))
    password = db.Column(db.String(20))
    income = db.Column(db.Integer)
    phoneNo = db.Column(db.String(15))

    def __init__(self, name, email, password, income, phoneNo):
        self.name=name
        self.email=email
        self.password=password
        self.income=income
        self.phoneNo=phoneNo
        

@app.route("/", methods = ["GET", "POST"])
def index():
    return render_template('index.html')


@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == 'POST':
        print("im in post")
        name = request.form['name']
        income = request.form['income']
        email = request.form['email']
        password = request.form['password']
        conpass = request.form['conpass']
        phoneNo = request.form['phoneNo']
        print(name, email, password, phoneNo, income)
        users = User.query.all()
        for user in users:
            try:
                if email == user.email:
                        return render_template('signup.html', password=0, email=1, user_exist=0)
                    
            except:
                return "There is an error"
        if conpass==password:
            new_entry=User(name=name, email=email, password=password, income=income, phoneNo=phoneNo)
            db.session.add(new_entry)
            db.session.commit()
            return render_template("login.html")
        else:
            return render_template("signup.html", password=1, email=0, user_exist=0)
    else:
        return render_template("signup.html", password=0, email=0, user_exist=0)


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == 'POST':
        print("im in post")
        email = request.form['email']
        password = request.form['password']
        print(email, password)
        users = User.query.all()
        for user in users:
            # print(user.email)
            if email == user.email: 
                if password == user.password:
                    session['name'] = user.name
                    return render_template("home.html",logged=1)
                
                else:
                    return render_template('login.html', credentials_incorrect=1)
            
        return render_template('signup.html', password=0, email=0, user_exist=1)
        
    else:
        return render_template("login.html", credentials_incorrect=0)


@app.route("/home", methods = ["GET", "POST"])
def home():
    if 'name' in session:
        return render_template("home.html", logged=0)
    else:
        return render_template("index.html")

if __name__ == '__main__':
    db.create_all()
    app.run()