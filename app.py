from flask import Flask, render_template, request, redirect, url_for
import os
from vragenmodel import VragenModel


app = Flask(__name__)

database_file = "databases/testcorrect_vragen.db"
vragen_model = VragenModel(database_file)

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
        login_status = vragen_model.login("inloggegevens", username, password)
        if login_status == True:
            return redirect(url_for("hello_world"))
        else:
            return render_template("login_failed.html")


@app.route('/filtering/')
def hello_world():
    tables = vragen_model.get_tables()
    return render_template('Index.html', tablenames=tables)

@app.route('/filtering/vragen')
def vragen():
    posts = vragen_model.get_questions()
    return render_template("vragen.html", posts=posts)

@app.route('/filtering/vragen/typfout')
def typfout():
    posts = vragen_model.get_typfout()
    return render_template("vragen.html", posts=posts)

@app.route('/filtering/vragen/auteurfout')
def auteurfout():
    posts = vragen_model.get_auteurfout()
    return render_template("vragen.html", posts=posts)

@app.route('/filtering/vragen/leerdoelfout')
def leerdoelfout():
    posts = vragen_model.get_leerdoelfout()
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
