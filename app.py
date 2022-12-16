from flask import Flask, render_template, request, redirect, url_for
import os
from vragenmodel import VragenModel


app = Flask(__name__)

database_file = "databases/testcorrect_vragen.db"
vragen_model = VragenModel(database_file)

#homepage
@app.route("/")
def index():
    return render_template("homepage.html")

#login pagina
@app.route("/login")
def login():
    return render_template("login.html")

#login handeling
@app.route("/login", methods=["POST"])
def login_info():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        login_status = vragen_model.login("inlog", username, password)
        if login_status == True:
            return redirect(url_for("hello_world"))
        else:
            return render_template("login_failed.html")

#dashboardscherm
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    posts = vragen_model.get_username()
    for post in posts:
        if post[2] == "True":
            return render_template("dashboard.html", posts=posts)
        else:
            return render_template("norights.html", posts=posts)

@app.route("/check", methods=["GET", "POST"])
def check():
    username = request.form.get("username")
    admin = request.form.get("admin")
    if admin == "Ontneem rechten":
        admin = "False"
    elif admin == "Geef rechten":
        admin = "True"
    
    vragen_model.set_admin(username, admin)
    return redirect(url_for('dashboard')) 

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
