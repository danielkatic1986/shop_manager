from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model za artikle
class Proizvod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(100), nullable=False)
    kategorija = db.Column(db.String(50), nullable=False)
    cijena = db.Column(db.Float, nullable=False)
    stanje = db.Column(db.Integer, nullable=False)

# Kreiranje baze podataka
with app.app_context():
    db.create_all()

# Rute
@app.route('/')
def index():
    proizvodi = Proizvod.query.all()
    return render_template('index.html', proizvodi=proizvodi)

@app.route('/dodaj', methods=['POST'])
def dodaj_proizvod():
    naziv = request.form['naziv']
    kategorija = request.form['kategorija']
    cijena = float(request.form['cijena'])
    stanje = int(request.form['stanje'])

    novi_proizvod = Proizvod(naziv=naziv, kategorija=kategorija, cijena=cijena, stanje=stanje)
    db.session.add(novi_proizvod)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/brisi/<int:id>')
def brisi_proizvod(id):
    proizvod = Proizvod.query.get(id)
    if proizvod:
        db.session.delete(proizvod)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
