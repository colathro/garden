from flask import Flask, render_template, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
import time
import threading
import Adafruit_ADS1x15
import Adafruit_DHT

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///garden.db'

db = SQLAlchemy(app)


class water_level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor = db.Column(db.Integer)
    voltage = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)

    def __init__(self, sensor, voltage, timestamp):
        self.sensor = sensor
        self.voltage = voltage
        self.timestamp = timestamp

    def serialize(self):
        return {
            "sensor": self.sensor,
            "voltage": self.voltage,
            "timestamp": self.timestamp
        }


class temphumidity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)

    def __init__(self, temp, humidity, timestamp):
        self.temp = temp
        self.humidity = humidity
        self.timestamp = timestamp

    def serialize(self):
        return {
            "temp": self.temp,
            "humidity": self.humidity,
            "timestamp": self.timestamp
        }


db.create_all()


def log_stats(db):
    while True:
        try:
            adc = Adafruit_ADS1x15.ADS1115()
            for i in range(4):
                # Read the specified ADC channel using the previously set gain value.
                voltage = adc.read_adc(i, gain=1)
                reading = water_level(sensor=i, voltage=voltage,
                                      timestamp=int(time.time()))
                db.session.add(reading)
            db.session.commit()
            print("Successfully logged water level.")
        except:
            print("Failed to log water level.")

        try:
            humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
            good_readings = False
            count = 0
            temp = None
            humidity = None
            while (not good_readings):
                count = count + 1
                humidity, temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
                if (humidity == None or temp == None):
                    good_readings = false
                    time.sleep(2)
                else:
                    good_readings = true
                if (count >= 10):
                    raise Exception("not good")
            reading = temphumidity(temp, humidity, int(time.time()))
            db.session.add(reading)
            db.session.commit()
            print("Successfully logged water level.")
        except:
            print("Failed to log water level.")
        time.sleep(600)


@app.route("/", defaults={'path': ''})
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')


@app.route("/api/water/all")
def water_all():
    return jsonify([i.serialize() for i in water_level.query.all()])


@app.route("/api/water/week")
def water_week():
    return jsonify([i.serialize() for i in water_level.query.all()])


@app.route("/api/startuplogs")
def startuplogs():
    with open("/tmp/rc.local.log", "r") as logfile:
        message = logfile.read()
        return render_template('logs.html', message=message,
                               time=time.ctime(os.path.getmtime("/tmp/rc.local.log")))


if __name__ == "__main__":
    thread = threading.Thread(target=log_stats, args=(db,))
    thread.daemon = True
    thread.start()
    app.run(host='0.0.0.0')
