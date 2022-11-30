from flask import Flask, render_template, request

FLASK_PORT = 3000
FLASK_HOST = "0.0.0.0"
DEBUG_STATUS = False

app = Flask(__name__)

#DEFAULT PAGE
@app.route("/")
def index():
    return render_template("login.html")

@app.route("/", methods=["POST"])
def login_info():
    if request.method == "POST":
        username = request.form.get("gebruikersnaam")
        password = request.form.get("wachtwoord")
        return f"Combination user  = {username}, {password}"

if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=DEBUG_STATUS)
