from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Model za artikle
class Proizvod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(100), nullable=False)
    kategorija = db.Column(db.String(50), nullable=False)
    opis = db.Column(db.String(200), nullable=False)
    cijena = db.Column(db.Float, nullable=False)
    stanje = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200), nullable=True) #putanja do slike

# Kreiranje baze podataka
with app.app_context():
    db.create_all()

# Rute
@app.route('/')
def index():
    proizvodi = Proizvod.query.all()
    if not proizvodi:
        return redirect(url_for('forma_dodaj_proizvod'))
    return render_template('index.html', proizvodi=proizvodi)

@app.route('/forma_dodaj_proizvod')
def forma_dodaj_proizvod():
    return render_template('dodaj-proizvod.html')

@app.route('/dodaj', methods=['POST'])
def dodaj_proizvod():
    naziv = request.form['naziv']
    kategorija = request.form['kategorija']
    opis = request.form.get('opis')  # ako želiš spremiti i opis
    cijena = float(request.form['cijena'])
    stanje = int(request.form['stanje'])
    
    # Obrada slike
    slika = request.files.get('slika')
    image_url = None
    if slika and allowed_file(slika.filename):
        filename = secure_filename(slika.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        slika.save(filepath)
        image_url = url_for('static', filename='images/' + filename)
    
    novi_proizvod = Proizvod(
        naziv=naziv,
        kategorija=kategorija,
        opis=opis,
        cijena=cijena,
        stanje=stanje,
        image_url=image_url  # spremi putanju do slike
    )
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

@app.route('/uredi/<int:id>', methods=['GET', 'POST'])
def uredi_proizvod(id):
    proizvod = Proizvod.query.get_or_404(id)
    if request.method == 'POST':
        proizvod.naziv = request.form['naziv']
        proizvod.kategorija = request.form['kategorija']
        proizvod.opis = request.form.get('opis')
        proizvod.cijena = float(request.form['cijena'])
        proizvod.stanje = int(request.form['stanje'])
        # Ako korisnik pošalje novu sliku
        slika = request.files.get('slika')
        if slika and allowed_file(slika.filename):
            filename = secure_filename(slika.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            slika.save(filepath)
            proizvod.image_url = url_for('static', filename='images/' + filename)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('uredi-proizvod.html', proizvod=proizvod)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)