fask minimal app 
--- then enter you will find the routing or app.py page 1st code
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/main_page')
def main_page():
    return render_template('index.html')
   # return 'Hello, Dhiren welcome to your 1st flask project! Did you get new page'

if __name__ == "__main__":
    app.run(debug=True)



after that type:
it make the file to run
if __name__ == "__main__":
app.run(debug=true)

for bootstrap:
getbootstrap.com


---static file 
--> you can put/ insert file as it is and can be easily access
--> first of all donot add any file in static file, User/client can easly acess those file



## To activate the env
--> .\env\Scripts\activate.ps1


==================================================================
For database:
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
---> Here todo.db is name of the database that i am going to use
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


## create class (database_name means you can put any name you want)
class database_name(db.Model)
s_no = db.column(db.Integer, primary_key = True)
User_name = db.column(db.string, nullable= False)
User_desc = db.column(db.string, nullable = Flase)
date_created = db.column(db.DateTime, default = datetime.utcnow)