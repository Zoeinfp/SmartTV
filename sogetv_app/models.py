from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_string = db.Column(db.String(50), primary_key=False)


class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), primary_key=False)
    temperature = db.Column(db.String(50), primary_key=False)
    description = db.Column(db.String(50), primary_key=False)
    icon = db.Column(db.String(50), primary_key=False)


class EventData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), primary_key=False)
    description = db.Column(db.String(256), primary_key=False)
    start = db.Column(db.String(50), primary_key=False)
    end = db.Column(db.String(50), primary_key=False)


class MessageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(64000), primary_key=False)
