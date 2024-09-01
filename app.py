from flask import Flask, render_template
from sqlalchemy import create_engine, Column, Integer, String, DateTime

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todo'
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    desc= db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
   ## data you want to see in table we use repr  
    def __repr__(self) -> str:
        return f"{self.sno} -  {self.title}"

with app.app_context():
    db.create_all()

@app.route('/main_page')
def main_page():
    todo = Todo(title ="First todo", desc = "Make an investment in crypto")
    db.session.add(todo)
    db.session.commit() 
    alltodo = Todo.query.all()
    
    return render_template('index.html', alltodo=alltodo)
   # return 'Hello, Dhiren welcome to your 1st flask project! Did you get new page'


@app.route('/show')
def product():
    alltodo = Todo.query.all()
    print(alltodo)
if __name__ == "__main__":
    app.run(debug=True)