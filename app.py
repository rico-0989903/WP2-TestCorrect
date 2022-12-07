from flask import Flask, render_template

from vragenmodel import VragenModel

app = Flask(__name__)

database_file = "databases/testcorrect_vragen.db"
vragen_model = VragenModel(database_file)

@app.route('/')

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

@app.route('/filtering/auteurs')
def auteurs():
    posts = vragen_model.get_auteurs()
    return render_template("auteurs.html", posts=posts)


# SELECT id, KOLOMNAAM from TABELNAAM
# python filter op DATATYPE en stuur naar browser

if __name__ == '__main__':
    app.run(debug=True, port=8001)