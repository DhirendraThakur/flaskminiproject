from flask import Flask, render_template
app = Flask(__name__)

@app.route('/main_page')
def main_page():
    return render_template('index.html')
   # return 'Hello, Dhiren welcome to your 1st flask project! Did you get new page'

if __name__ == "__main__":
    app.run(debug=True)