import base64
import os
import time
from io import BytesIO
from PIL import Image

from flask import Flask, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
import requests


class VueFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='(%',
        block_end_string='%)',
        variable_start_string='((',
        variable_end_string='))',
        comment_start_string='(#',
        comment_end_string='#)'
    ))


app = VueFlask(__name__, template_folder='templates', static_folder='static')

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sogetv.db'

db = SQLAlchemy(app)

GIT_TOKEN = '8b5da14674a9d607eb5a0fa944cc90b9bf3d5747'


class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_string = db.Column(db.String(50), primary_key=False)


class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), primary_key=False)
    temperature = db.Column(db.String(50), primary_key=False)
    description = db.Column(db.String(50), primary_key=False)
    icon = db.Column(db.String(50), primary_key=False)


db.create_all()
db.session.commit()


@app.route("/")
def home(status=None):
    images = ImageData.query.all()

    images_list = []
    for image in images:
        if not isinstance(image.image_string, str):
            image_src = 'data:image/png;base64,' + image.image_string.decode("utf-8")
            images_list.append(image_src)

    return render_template('index.html', images=images_list, status=status, weather_data=WeatherData.query.all())


def save_image(image_string):
    new_image = ImageData(image_string=image_string)
    db.session.add(new_image)
    db.session.commit()
    return True


@app.route('/update_weather', methods=['GET', 'POST'])
def update_weather():
    cities = WeatherData.query.all()
    WeatherData.query.delete()
    for city in cities:
        new_city = city.name
        create_weather_data(new_city)
    return home()


@app.route('/rm', methods=['GET', 'POST'])
def rm():
    deleted_city = request.form['deleted_city']
    WeatherData.query.filter_by(name=deleted_city).delete()
    print("Removing " + deleted_city + " from cities !")
    db.session.commit()
    return render_template(template_name_or_list='index.html',
                           timestamp=time.strftime('%d %B %Y %H:%M:%S'),
                           weather_data=WeatherData.query.all())


@app.route('/add/', methods=['GET', 'POST'])
def add_files():
    return home(status='upload')


def create_weather_data(new_city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=254d0bd84bee0354b5b34e17f870cf04'

    r = requests.get(url.format(new_city)).json()

    name = new_city
    temperature = r['main']['temp']
    description = r['weather'][0]['description'],
    icon = r['weather'][0]['icon'],
    print(new_city)
    get_or_create_weather_data(name=name, temperature=temperature, description=description[0], icon=icon[0])
    return name


def get_or_create_weather_data(name, temperature, description, icon):
    exists = db.session.query(WeatherData.id).filter_by(name=name).scalar() is not None

    if exists:
        return db.session.query(WeatherData).filter_by(name=name).first()
    else:
        new_weather_obj = WeatherData(name=name, temperature=temperature, description=description, icon=icon)
        db.session.add(new_weather_obj)
        db.session.commit()
        return name


@app.route('/add_weather', methods=['GET', 'POST'])
def add_weather():
    return home(status='weather')


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        new_city = request.form.get('city')

        if new_city:
            print("Request add for  " + new_city + " !")
            create_weather_data(new_city)

    return render_template(template_name_or_list='index.html',
                           timestamp=time.strftime('%d %B %Y %H:%M:%S'),
                           weather_data=WeatherData.query.all())


@app.route('/images')
def list_files():
    images = ImageData.query.all()

    images_list = []
    for image in images:
        if not isinstance(image.image_string, str):
            image_src = 'data:image/png;base64,' + image.image_string.decode("utf-8")
            images_list.append(image_src)

    return render_template('index.html', list=images_list)


@app.route('/delete', methods=['POST'])
def delete_file():
    image_to_delete = request.form.get('image')
    images = ImageData.query.all()

    for image in images:
        if not isinstance(image.image_string, str):
            if image_to_delete == 'data:image/png;base64,' + image.image_string.decode("utf-8"):
                ImageData.query.filter_by(image_string=image.image_string).delete()
                db.session.commit()
    return home()


@app.route('/upload', methods=['POST'])
def upload_file():
    image = request.files['image']
    image_string = base64.b64encode(image.read())
    save_image(image_string)

    # fh = open("imageToSave.png", "wb")
    # fh.write(str.decode('base64'))
    # fh.close()

    # file = request.files['image']
    # f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    # file.save(f)

    # fh = open("imageToSave.png", "wb")
    # fh.write(str.decode('base64'))
    # fh.close()

    return render_template('index.html', init=True)


if __name__ == "__main__":
    app.run()
