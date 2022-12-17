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
        login_status = vragen_model.login("inlog", username, password)
        if login_status == True:
            session['login'] = "logged_in"
            session.update({'username':username})
            return redirect(url_for("hello_world"))
        else:
            return render_template("login_failed.html")

@app.route("/filtering/logout")
def logout():
    del session['login']
    del session['username']
    print(session)
    return redirect(url_for('login'))

#dashboardscherm
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    username = session['username']
    check = vragen_model.check_rights(username)
    check = str(check[0])
    posts = vragen_model.get_username()
    if check == "('True',)":
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
    print(session)
    tables = vragen_model.get_tables()
    return render_template('Index.html', tablenames=tables)

#laat alle fouten zien
@app.route('/filtering/vragen')
def vragen():
    username = session['username']
    check = vragen_model.check_rights(username)
    check = str(check[0])
    posts = vragen_model.get_questions()
    return render_template("vragen.html", check=check, posts=posts)

#laat alle typfouten zien
@app.route('/filtering/vragen/typfout')
def typfout():
    username = session['username']
    check = vragen_model.check_rights(username)
    check = str(check[0])
    posts = vragen_model.get_typfout()
    return render_template("vragen.html", check=check, posts=posts)

#laat alle niet bestaande auteurs zien
@app.route('/filtering/vragen/auteurfout')
def auteurfout():
    username = session['username']
    check = vragen_model.check_rights(username)
    check = str(check[0])
    posts = vragen_model.get_auteurfout()
    return render_template("vragen.html", check=check, posts=posts)

#laat alle niet bestaande leerdoelen zien
@app.route('/filtering/vragen/leerdoelfout')
def leerdoelfout():
    username = session['username']
    check = vragen_model.check_rights(username)
    check = str(check[0])
    posts = vragen_model.get_leerdoelfout()
    return render_template("vragen.html", check=check, posts=posts)

#laat alle leerdoelen zien
@app.route('/filtering/leerdoelen')
def leerdoelen():
    username = session['username']
    check = vragen_model.check_rights(username)
    check = str(check[0])
    posts = vragen_model.get_leerdoelen()
    return render_template("leerdoelen.html",check=check, posts=posts)

#laat alle auteurs zien
@app.route('/filtering/auteurs', methods=["GET", "POST"])
def auteurs():
    username = session['username']
    check = vragen_model.check_rights(username)
    check = str(check[0])
    posts = vragen_model.get_auteurs()
    return render_template("auteurs.html",check=check, posts=posts)

#laat de details van de gekozen line zien
@app.route('/vraagdetail', methods=["GET", "POST"])
def vraagdetail():
    id = request.form['id']
    table = request.form['table']
    posts = vragen_model.get_details(id, table)
    return render_template("vraagdetail.html", posts=posts)

@app.route('/vraagdetail/aanpassen', methods=["GET", "POST"])
def vraag_aanpassen():
    if request.method == "POST":
        question_id = request.form.get("id")
        leerdoel = request.form.get("leerdoel")
        question = request.form.get("question")
        auteur = request.form.get("auteur")
        vragen_model.update_question(question_id, leerdoel, question, auteur)
    return redirect(url_for("vragen"))



# SELECT id, KOLOMNAAM from TABELNAAM
# python filter op DATATYPE en stuur naar browser

if __name__ == '__main__':
    app.run(debug=True, port=8001)
