import csv
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, URL

class LoginForm(FlaskForm):
    cafe_name = StringField(label="Cafe Name",validators=[DataRequired(message="bhar de bc")])
    location = StringField(label="Cafe Location On Google Maps(URL)", validators=[DataRequired(), URL(require_tld=True)])
    open_time = StringField(label="Opening Time e.g. 8am", validators=[DataRequired()])
    close_time = StringField(label="Closing Time e.g. 5:30pm")
    coffee_rating = SelectField(label="Coffee Rating", validators=[DataRequired()], choices=[("low", "☕"),("medium", "☕☕"),("high","☕☕☕"),("Good","☕☕☕☕"),("Excellent","☕☕☕☕☕")])
    wifi_rating = SelectField(label="Wifi Power Rating", validators=[DataRequired()], choices=[("low","💪"),("medium","💪💪"),("high","💪💪💪"),("good","💪💪💪💪"),("excellent","💪💪💪💪💪")])
    power_availability = SelectField(label="Power Socket Availability", validators=[DataRequired()], choices=[("low","🔌"),("medium","🔌🔌"), ("high","🔌🔌🔌"),("good","🔌🔌🔌🔌"),("excellent","🔌🔌🔌🔌🔌")])

    submit = SubmitField(label='Add Cafe')



app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = "dniuehfiuwefhui"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cafes')
def cafes():
    with open('Cafe_Data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafe.html', cafes=list_of_rows, no_of_cafes=len(list_of_rows))

@app.route('/add',methods=["GET","POST"])
def add_cafe():
    form = LoginForm()
    if form.validate_on_submit() :
        with open("Cafe_Data.csv",encoding="utf-8", mode='a') as csv_file:
            csv_file.write(f"{form.cafe_name.data},"
                           f"{form.location.data.replace(',','%2C')},"
                           f"{form.open_time.data},"
                           f"{form.close_time.data},"
                           f"{form.coffee_rating.data},"
                           f"{form.wifi_rating.data},"
                           f"{form.power_availability.data}\n")
            return redirect(url_for('add_cafe'))



    return render_template("add.html", form=form)


if __name__ == "__main__":
    app.run(debug=True,port=5001)