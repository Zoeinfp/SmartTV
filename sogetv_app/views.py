import base64
import os
import random
import time

from flask import Flask, request, render_template, jsonify, url_for, session
from werkzeug.utils import redirect
import sogetv_app.models
import sogetv_app.helpers

PASSWORD = ";4?DcUu$JKf?E7$y"


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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sogetv.db'
db = sogetv_app.models.SQLAlchemy(app)
db.create_all()
db.session.commit()


@app.route("/home", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def home():
    """
    Home
    :return: Index template
    """

    status = request.args.get('status', default=None, type=None)
    timestamp = time.strftime('%d %B %Y %H:%M:%S')
    timestamp_fullcalendar = time.strftime('%F')
    images = sogetv_app.models.ImageData.query.all()
    messages = sogetv_app.models.MessageData.query.all()
    messages_list = []
    quote_list = []
    text_list = []

    for m in messages:
        text_list.append(m.message)
        if ':' in m.message:
            quote_list.append(m.message)
        else:
            messages_list.append(m.message)

    quote = None
    if quote_list:
        quote = random.choice(quote_list)

    images_list = []
    for image in images:
        if not isinstance(image.image_string, str):
            image_src = 'data:image/png;base64,' + image.image_string.decode("utf-8")
            images_list.append(image_src)

    print("Status : ", status)

    my_events = sogetv_app.models.EventData.query.all()

    today_events = []
    for event in my_events:
        if event.end == timestamp_fullcalendar:
            today_events.append(event)

    if 'password' in session and session['password'] == PASSWORD:
        return render_template(template_name_or_list='index.html',
                               images=images_list,
                               messages=messages_list,
                               text=text_list,
                               status=status,
                               now=timestamp,
                               horoscope=sogetv_app.helpers.zodiac(),
                               quote=quote,
                               my_events=my_events,
                               today_events=today_events,
                               weather_data=sogetv_app.models.WeatherData.query.all())
    else:
        return render_template(template_name_or_list='login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    print(os.environ.get('password'))
    session['password'] = request.args.get('password')
    return redirect(url_for('home'))


@app.route('/text/', methods=['GET', 'POST'])
def add_text():
    """
    Request home with messages status
    :return: Index template with messages status
    """
    return redirect(url_for('home', status='messages'))


@app.route('/add_weather', methods=['GET', 'POST'])
def add_weather():
    """
    Add weather status
    :return: Index with add weather status
    """
    return redirect(url_for('home', status='weather'))


@app.route('/message', methods=['GET', 'POST'])
def message():
    """
    Create message
    :return: Index template
    """
    new_message = request.form.get('message')

    if new_message:
        from sogetv_app.helpers import create_new_message
        create_new_message(new_message)

    return redirect(url_for('home'))


@app.route('/update_message', methods=['GET', 'POST'])
def update_message():
    """
    Update message
    :return: Updated feedback
    """
    old_message = request.args.get('old_message')
    new_message = request.args.get('new_message')

    sogetv_app.models.MessageData.query.filter_by(message=old_message).delete()
    sogetv_app.models.db.session.commit()

    from sogetv_app.helpers import create_new_message
    create_new_message(new_message)

    return jsonify('Updated')


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    """
    Create weather data
    :return: Index template
    """
    if request.method == 'POST':
        new_city = request.form.get('city')

        if new_city:
            print("Request add for  " + new_city + " !")
            from sogetv_app.helpers import create_weather_data
            create_weather_data(new_city)

    return redirect(url_for('home'))


@app.route('/update_weather', methods=['GET', 'POST'])
def update_weather():
    """
    Update Weather
    :return: Index template
    """
    cities = sogetv_app.models.WeatherData.query.all()
    sogetv_app.models.WeatherData.query.delete()
    for city in cities:
        new_city = city.name
        from sogetv_app.helpers import create_weather_data
        create_weather_data(new_city)
    return redirect(url_for('home'))


@app.route('/remove_city', methods=['GET', 'POST'])
def remove_city():
    """
    Remove city
    :return: Index template
    """
    deleted_city = request.form['deleted_city']
    sogetv_app.models.WeatherData.query.filter_by(name=deleted_city).delete()
    print("Removing " + deleted_city + " from cities !")
    sogetv_app.models.db.session.commit()
    return redirect(url_for('home'))


@app.route('/images', methods=['GET', 'POST'])
def list_files():
    """
    List images files
    :return: Index template
    """
    return redirect(url_for('home', status='list_images'))


@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    """
    Add calendar status
    :return: Index template with calendar status
    """
    return redirect(url_for('home', status='calendar'))


@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    """
    Create event and add calendar status
    :return: Index template with calendar status
    """
    title = request.form.get('event_title')
    description = request.form.get('event_description')
    start = request.form.get('start_date_event')
    end = request.form.get('end_date_event')
    from sogetv_app.helpers import get_or_create_event
    get_or_create_event(title=title, description=description, start=start, end=end)
    return redirect(url_for('home', status="calendar"))


@app.route('/delete_event', methods=['GET', 'POST'])
def delete_event():
    """
    Delete event
    :return:
    """
    event_to_delete = request.args.get('delete_event')
    sogetv_app.models.EventData.query.filter_by(title=event_to_delete).delete()
    sogetv_app.models.db.session.commit()
    print('event deleted')
    print(event_to_delete)
    return jsonify('Deleted')


@app.route('/delete_message', methods=['GET', 'POST'])
def delete_message():
    """
    Delete message
    :return:
    """
    rm_msg_form = request.form.get('message')
    rm_msg_arg = request.args.get('old_message')

    if rm_msg_form:
        sogetv_app.models.MessageData.query.filter_by(message=rm_msg_form).delete()

    if rm_msg_arg:
        print('Delete message')
        print('message to delete', rm_msg_arg, 'end')
        sogetv_app.models.MessageData.query.filter_by(message=rm_msg_arg).delete()

    sogetv_app.models.db.session.commit()
    return jsonify('Deleted')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """
    Upload image file
    :return: Index template
    """
    image = request.files['image']
    image_string = base64.b64encode(image.read())
    from sogetv_app.helpers import save_image
    save_image(image_string)

    return render_template('index.html', init=True)


@app.route('/delete', methods=['GET', 'POST'])
def delete_file():
    """
    Delete image file
    :return:
    """
    image_to_delete = request.form.get('image')
    images = sogetv_app.models.ImageData.query.all()

    for image in images:
        if not isinstance(image.image_string, str):
            if image_to_delete == 'data:image/png;base64,' + image.image_string.decode("utf-8"):
                sogetv_app.models.ImageData.query.filter_by(image_string=image.image_string).delete()
                sogetv_app.models.db.session.commit()
    return redirect('home')
