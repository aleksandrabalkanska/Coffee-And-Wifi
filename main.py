from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, TimeField, SelectField
from wtforms.validators import DataRequired
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    cafe_location = URLField('Cafe Location on Google Maps(URL)', validators=[DataRequired()])
    open_time = TimeField('Opening Time e.g. 8AM', validators=[DataRequired()])
    close_time = TimeField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    rating = SelectField('Coffee Rating',
                         choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"], validators=[DataRequired()])
    wifi_strength = SelectField('Wifi Strength Rating',
                                choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"], validators=[DataRequired()])
    power_socket = SelectField('Power Socket Availability',
                               choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"], validators=[DataRequired()])

    submit = SubmitField('Submit')



# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    new_cafe = [value for key, value in form.data.items()][:-2]
    if form.validate_on_submit():
        with open('cafe-data.csv', mode='a', newline='', encoding='utf-8') as csv_file:
            new_data = csv.writer(csv_file)
            csv_file.write('\n')
            new_data.writerow(new_cafe)
            return redirect('cafes')
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
