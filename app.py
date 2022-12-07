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
        username = request.form.get("gebruikersnaam")
        password = request.form.get("wachtwoord")
        login_status = db.login("inloggegevens", username, password)
        return login_status


if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=DEBUG_STATUS)
