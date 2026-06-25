from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)
DATABASE = 'journal.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par leur nom
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    # On récupère tous les articles du plus récent au plus ancien
    cursor.execute('SELECT * FROM articles ORDER BY id DESC')
    articles = cursor.fetchall()
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True, port=5000)