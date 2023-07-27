from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    room = db.Column(db.String(200), nullable=False)
    option = db.Column(db.String(200), nullable=False)
    arrival = db.Column(db.Text, nullable=False)
    departure = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Booking %r>' % self.id

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/booking', methods=['POST','GET'])
def booking():
    if request.method == 'POST':
        name = request.form['name']
        room = request.form['room']
        option = request.form['option']
        arrival = request.form['arrival']
        departure = request.form['departure']
        booking = Booking(name=name, room=room, option=option, arrival=arrival, departure=departure)
        try:
            db.session.add(booking)
            db.session.commit()
            return redirect('/')
        except:
            return 'error'
    else:
        return render_template('booking.html')


@app.route('/record')
def record():
    bookinges = Booking.query.order_by(Booking.date).all()
    return render_template('record.html',bookinges=bookinges)

@app.route('/record/<int:id>')
def book_detail(id):
    booking = Booking.query.get(id)
    return render_template("record_detail.html", booking=booking)

@app.route ('/record/<int:id>/del')
def book_delete (id):
    booking = Booking.query.get_or_404(id)
    try:
        db.session.delete(booking)
        db.session.commit()
        return redirect('/record')
    except:
        return "Oops,Booking can't be deleted"

@app. route('/record/<int:id>/update', methods= ['POST', 'GET'])
def book_update(id):
    booking = Booking.query.get(id)
    if request.method == "POST":
        booking.name = request.form['name']
        booking.room = request.form['room']
        booking.option = request.form['option']
        booking.arrival = request.form['arrival']
        booking.departure = request.form['departure']
        try:
            db.session.commit()
            return redirect('/record')
        except:
            return "Oops,Booking can't be updated"
    else:
        return render_template("book_update.html",booking=booking)


@app.route('/president')
def president():
    return render_template('president.html')

@app.route('/luxe')
def luxe():
    return render_template('luxe.html')

@app.route('/family')
def family():
    return render_template('family.html')

@app.route('/standart')
def standart():
    return render_template('standart.html')

@app.route('/check')
def check():
    return render_template('check.html')


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/room')
def room():
    return render_template('room.html')


@app.route('/option')
def option():
    return render_template('option.html')

@app.route('/images')
def images():
    return render_template('images.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'),404

if __name__ == '__main__':
    app.run(debug=True)
