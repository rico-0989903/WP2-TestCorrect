from flask import Flask, render_template, request, redirect, url_for
import os

from lib.databasemodel import DatabaseModel


FLASK_PORT = 3000
FLASK_HOST = "0.0.0.0"
DEBUG_STATUS = True

app = Flask(__name__)

DATABASE_FILE = os.path.join(app.root_path, 'databases', 'testcorrect_vragen.db')
db = DatabaseModel(DATABASE_FILE)


#DEFAULT PAGE
@app.route("/")
def index():
    return render_template("homepage.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_info():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        login_status = db.login("inloggegevens", username, password)
        if login_status == True:
            return f"Login succesfull! Welcome {username}!"
        else:
            return render_template("login_failed.html")


#MAIN ROMAN
from vragenmodel import VragenModel


database_file = "databases/testcorrect_vragen.db"
vragen_model = VragenModel(database_file)


@app.route('/filtering/')
def hello_world():
    tables = vragen_model.get_tables()
    return render_template('Index.html', tablenames=tables)

@app.route('/filtering/vragen')
def vragen():
    posts = vragen_model.get_questions()
    return render_template("vragen.html", posts=posts)

@app.route('/filtering/leerdoelen')
def leerdoelen():
    posts = vragen_model.get_leerdoelen()
    return render_template("leerdoelen.html", posts=posts)

@app.route('/filtering/auteurs', methods=["GET", "POST"])
def auteurs():
    posts = vragen_model.get_auteurs()
    return render_template("auteurs.html", posts=posts)

@app.route('/vraagdetail', methods=["GET", "POST"])
def vraagdetail():
    id = request.form['id']
    table = request.form['table']
    posts = vragen_model.get_details(id, table)
    return render_template("vraagdetail.html", posts=posts)



# SELECT id, KOLOMNAAM from TABELNAAM
# python filter op DATATYPE en stuur naar browser

if __name__ == '__main__':
    app.run(debug=True, port=8001)
