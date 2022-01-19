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

class Budget(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    food = db.Column(db.Integer)
    rent = db.Column(db.Integer)
    life = db.Column(db.Integer)
    others = db.Column(db.Integer)
    

    def __init__(self, email, food, rent, life, others):
        self.email=email
        self.food=food
        self.rent=rent
        self.life=life
        self.others=others
        

@app.route("/", methods = ["GET", "POST"])
def index():
    return render_template('index.html')


@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == 'POST':
        print("im in post")
        name = request.form.get('name')
        income = request.form.get('income')
        email = request.form.get('email')
        password = request.form.get('password')
        conpass = request.form.get('conpass')
        phoneNo = request.form.get('phoneNo')
        print(name, email, password, phoneNo, income)
        users = User.query.all()
        for user in users:
            try:
                if email == user.email:
                        return render_template('signup.html', password=0, email=1, user_exist=0)
                    
            except:
                return "There is an error"
        
        new_entry=User(name=name, email=email, password=password, income=income, phoneNo=phoneNo)
        db.session.add(new_entry)
        db.session.commit()
        return render_template("login.html")
        
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
                    session['email'] = user.email
                    session['income'] = user.income
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

@app.route("/budget", methods = ["GET", "POST"])
def budget():
    if 'name' in session:
        if request.method == 'POST':
            email=session['email']
            food=request.form['food']
            rent=request.form['rent']
            life=request.form['life']
            others=request.form['others']
            # print(email, food, rent, life, others)
            exist_data = Budget.query.filter_by(email=email).first()
            exist_data.food=food
            exist_data.rent=rent
            exist_data.life=life
            exist_data.others=others
            db.session.commit()
            data = Budget.query.filter_by(email=email).first()
            return render_template("budget.html", income=session['income'], data=data)
        else:
            data = Budget.query.filter_by(email=session['email']).first()
            return render_template("budget.html", income=session['income'], data=data)
    else:
        return render_template("index.html")

if __name__ == '__main__':
    db.create_all()
    app.run()