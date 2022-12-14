from flask import Flask, render_template, request, redirect, url_for, session
import os
from vragenmodel import VragenModel


app = Flask(__name__)
Flask.secret_key = "team_brainstorm"


database_file = "databases/testcorrect_vragen.db"
vragen_model = VragenModel(database_file)

@app.before_request
def check_login():
    if "login" not in session and request.endpoint not in ["login", "static", "login_handle"]:
        return redirect(url_for("login"))

#homepage
@app.route("/")
def index():        
    if "login" in session:
        return redirect(url_for("hello_world"))
    else:
        return redirect(url_for("login"))

#login pagina
@app.route("/login")
def login():
    return render_template("login.html")

#login handeling
@app.route("/login", methods=["POST", "GET"])
def login_handle():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        login_status = vragen_model.login("inloggegevens", username, password)
        if login_status == True:
            session['login'] = "logged_in"
            return redirect(url_for("hello_world"))
        else:
            return render_template("login_failed.html")

#keuzescherm
@app.route('/filtering/')
def hello_world():
    tables = vragen_model.get_tables()
    return render_template('Index.html', tablenames=tables)

#laat alle fouten zien
@app.route('/filtering/vragen')
def vragen():
    posts = vragen_model.get_questions()
    return render_template("vragen.html", posts=posts)

#laat alle typfouten zien
@app.route('/filtering/vragen/typfout')
def typfout():
    posts = vragen_model.get_typfout()
    return render_template("vragen.html", posts=posts)

#laat alle niet bestaande auteurs zien
@app.route('/filtering/vragen/auteurfout')
def auteurfout():
    posts = vragen_model.get_auteurfout()
    return render_template("vragen.html", posts=posts)

#laat alle niet bestaande leerdoelen zien
@app.route('/filtering/vragen/leerdoelfout')
def leerdoelfout():
    posts = vragen_model.get_leerdoelfout()
    return render_template("vragen.html", posts=posts)

#laat alle leerdoelen zien
@app.route('/filtering/leerdoelen')
def leerdoelen():
    posts = vragen_model.get_leerdoelen()
    return render_template("leerdoelen.html", posts=posts)

#laat alle auteurs zien
@app.route('/filtering/auteurs', methods=["GET", "POST"])
def auteurs():
    posts = vragen_model.get_auteurs()
    return render_template("auteurs.html", posts=posts)

#laat de details van de gekozen line zien
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
