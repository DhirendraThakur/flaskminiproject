
from flask import Flask, render_template, request, redirect, session, url_for
from sqlalchemy import create_engine, Column, Integer, String, DateTime

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key='secret_key'

class Todo(db.Model):
    __tablename__ = 'todo'
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    desc= db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
   ## data you want to see in table we use repr  
    def __repr__(self) -> str:
        return f"{self.sno} -  {self.title}"

class Register_user(db.Model):
    __tablename__ = 'Register_user'
    reg_no = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(100), nullable = False)
    address = db.Column(db.String(400), nullable = False)
    phone = db.Column(db.String(100), nullable = False)
    def __init__ (self, fullname, email, password, address, phone):
        self.fullname = fullname
        self.email= email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.address = address
        self.phone = phone
    # def __repr__(self) -> str:
    #     return f"{self.fullname} -  {self.email} -  {self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.getsalt()).decode('utf-8')} -  {self.address} -  {self.phone}"
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
        


with app.app_context():
    db.create_all()
    

@app.route('/', methods =['GET', 'POST'])
def main_page():
    if request.method =="POST":
        title =request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit() 
    alltodo = Todo.query.all()
    
    return render_template('index.html', alltodo=alltodo)
  
   
@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method =="POST":
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        phone=request.form['phone']
        register_user = Register_user(fullname=fullname, email=email, password=password, address = address, phone=phone)
        db.session.add(register_user)
        db.session.commit()
    allreg = Register_user.query.all()
    return render_template('register.html', allreg =allreg)

@app.route('/userdata', methods =['GET', 'POST'])
def user_data():
    allreg = Register_user.query.all()
    return render_template('userdata.html',allreg =allreg )



    
@app.route('/update/<int:sno>', methods =['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title =request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/updateuser/<int:reg_no>', methods =['GET', 'POST'])
def updateuser(reg_no):
    if request.method=='POST':
        fullname =request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        phone = request.form['phone']
        register_user = Register_user.query.filter_by(reg_no=reg_no).first()
        register_user.fullname = fullname
        register_user.email = email
        register_user.password = password
        register_user.address = address
        register_user.phone = phone
        
        db.session.add(register_user)
        db.session.commit()
        return redirect("/userdata")
    register_user = Register_user.query.filter_by(reg_no=reg_no).first()
    return render_template('updateuser.html', register_user=register_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        
        user = Register_user.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['fullname'] = user.fullname
            session['email'] = user.email
            session['password'] = user.password
            return redirect('/dashboard')
        else:
            return render_template('login.html', error ="Invalid User!")
        
    return render_template('login.html')
            
@app.route('/dashboard')
def dashboard():
    if session['fullname']:
        return render_template('dashboard.html')
    return redirect('/login.html')

    
@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    
    return redirect("/")

@app.route('/delete_userdata/<int:reg_no>')
def delete_userdata(reg_no):
    register_user = Register_user.query.filter_by(reg_no=reg_no).first()
    db.session.delete(register_user)
    db.session.commit()
    
    return redirect("/userdata")
    
if __name__ == "__main__":
    app.run(debug=True)