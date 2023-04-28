from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os

WTF_CSRF_SECRET_KEY=os.environ.get('CSRF_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
csrf = CSRFProtect(app)
Bootstrap(app)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create Table
# with app.app_context():
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    loud_music = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)
# db.create_all()

class AddCafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = StringField("Has Sockets?", validators=[DataRequired()])
    rating = StringField("Rating max.5", validators=[DataRequired()])
    has_wifi = StringField("Has WiFi?", validators=[DataRequired()])
    loud_music = StringField("Loud Music?", validators=[DataRequired()])
    seats = StringField("Number of Seats", validators=[DataRequired()])
    coffee_price = StringField("Coffee Price", validators=[DataRequired()])
    submit = SubmitField("Add Cafe")


@app.route("/")
def home():
    all_cafes = Cafe.query.all()
    db.session.commit()
    return render_template("index.html", cafes=all_cafes)

#Create Record
@app.route("/add", methods=["GET","POST"])
def add_cafe():
    form = AddCafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
        name = form.name.data,
        map_url = form.map_url.data,
        img_url = form.img_url.data,
        location = form.location.data,
        has_sockets = int(form.has_sockets.data),
        rating = int(form.rating.data),
        has_wifi = int(form.has_wifi.data),
        loud_music = int(form.loud_music.data),
        seats = form.seats.data,
        coffee_price = form.coffee_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_cafe.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
