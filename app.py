from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_bcrypt import Bcrypt
import os
from vragenmodel import VragenModel
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity




app = Flask(__name__)
bcrypt = Bcrypt(app)
Flask.secret_key = "team_brainstorm"
app.config['SECRET_KEY'] = 'a3962e306c5e4fc68d6f7895ba26c6f2'
jwt = JWTManager(app)
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
    if "login" in session:
        return redirect(url_for("hello_world"))
    else:
        return render_template("login.html")

#login handeling
@app.route("/login", methods=["POST", "GET"])
def login_handle():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_password = vragen_model.get_userinfo(username)
        print(hashed_password[0][0])
        login_status = bcrypt.check_password_hash(hashed_password[0][0], password)
        if login_status == True:
            session['login'] = "logged_in"
            session.update({'username':username})
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token)
        else:
            return render_template("login.html", error="Voer een juiste combinatie in")

@app.route("/filtering/logout")
def logout():
    del session['login']
    del session['username']
    return redirect(url_for('login'))

#dashboardscherm
@app.route("/dashboard", methods=["GET", "POST"])
@jwt_required()
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
@jwt_required()
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
@jwt_required()
def hello_world():
    print(session)
    tables = vragen_model.get_tables()
    return render_template('Index.html', tablenames=tables)

#laat alle fouten zien
@app.route('/filtering/vragen', methods=["GET", "POST"])
@jwt_required()
def vragen():
    username = session['username']
    check = vragen_model.check_rights(username)
    check = str(check[0])
    posts = vragen_model.get_questions()
    return render_template("vragen.html", check=check, posts=posts)

@app.route('/filtering/vragen/filter', methods=["GET", "POST"])
@jwt_required()
def filteren():
    try:
        min_value = int(request.form.get("minimum"))
        print("Min is an int!")
    except:
        min_value = None

    try:
        max_value = int(request.form.get("maximum"))
        print("Max is an int!")
    except:
        max_value = None
    
    print(min_value, max_value)
    username = session['username']
    check = vragen_model.check_rights(username)
    check = str(check[0])

    #laat alle typfouten zien
    if request.form['action'] == 'Typ fouten':
        posts = vragen_model.get_typfout(min_value, max_value)
        return render_template("vragen.html", check=check, posts=posts)

    #laat alle niet bestaande auteurs zien
    elif request.form['action'] == 'Niet bestaande auteurs':
        posts = vragen_model.get_auteurfout(min_value, max_value)
        return render_template("vragen.html", check=check, posts=posts)

    #laat alle niet bestaande leerdoelen zien
    elif request.form['action'] == 'Niet bestaande leerdoelen':
        posts = vragen_model.get_leerdoelfout(min_value, max_value)
        return render_template("vragen.html", check=check, posts=posts)
    
    #laat alle vragen met lege vakken zien
    elif request.form['action'] == 'Lege vakjes':
        posts = vragen_model.get_null(min_value, max_value)
        return render_template("vragen.html", check=check, posts=posts)

#laat alle leerdoelen zien
@app.route('/filtering/leerdoelen')
@jwt_required()
def leerdoelen():
    username = session['username']
    check = vragen_model.check_rights(username)
    check = str(check[0])
    posts = vragen_model.get_leerdoelen()
    return render_template("leerdoelen.html",check=check, posts=posts)

#laat alle auteurs zien
@app.route('/filtering/auteurs', methods=["GET", "POST"])
@jwt_required()
def auteurs():
    username = session['username']
    check = vragen_model.check_rights(username)
    check = str(check[0])
    posts = vragen_model.get_auteurs()
    return render_template("auteurs.html",check=check, posts=posts)

#laat de details van de gekozen line zien
@app.route('/vraagdetail', methods=["GET", "POST"])
@jwt_required()
def vraagdetail():
    id = request.form['id']
    table = request.form['table']
    posts = vragen_model.get_details(id, table)
    return render_template("vraagdetail.html", posts=posts)

@app.route('/vraagdetail/aanpassen', methods=["GET", "POST"])
@jwt_required()
def vraag_aanpassen():
    if request.method == "POST":
        question_id = request.form.get("id")
        leerdoel = request.form.get("leerdoel")
        question = request.form.get("question")
        auteur = request.form.get("auteur")
        vragen_model.update_question(question_id, leerdoel, question, auteur)
    return redirect(url_for("vragen"))

@app.route('/auteurdetail', methods=["POST", "GET"])
@jwt_required()
def auteurdetail():
    id = request.form['id']
    table = request.form['table']
    posts = vragen_model.get_details(id, table)
    return render_template("auteurdetail.html", posts=posts)

@app.route('/auteurdetail/aanpassen', methods=["GET", "POST"])
@jwt_required()
def auteur_aanpassen():
    if request.method == "POST":
        auteur_id = request.form.get("id")
        voornaam = request.form.get("voornaam")
        achternaam = request.form.get("achternaam")
        geboortejaar = request.form.get("geboortejaar")
        medewerker = request.form.get("medewerker")
        pensioen = request.form.get("pensioen")
        vragen_model.update_auteur(auteur_id, voornaam, achternaam, geboortejaar, medewerker, pensioen)
    return redirect(url_for("auteurs"))

# SELECT id, KOLOMNAAM from TABELNAAM
# python filter op DATATYPE en stuur naar browser

if __name__ == '__main__':
    app.run(debug=True, port=8001)
