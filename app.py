import flask  # Allows the development of web application
import requests  # Allows sending HTTP requests with python to external API
from flask import Flask, request, render_template  # Functions on flask
import re  # Check if the string contains the conditions I defined
from datetime import datetime # date & time functions


'''
This is a web app that shows the weather for the next 7 days.
-------------------------------------------------------------------
Functionality: Receives input from the user, and checks if it
contains only letters and spaces. sends the location that the
user entered to an external API, verifies that the received
status code is 200, filters unwanted information, and displays
the page with the results. If there is a problem with the input
or status code, it will return an error message to the user.
-------------------------------------------------------------------
Moduls:
flask - allows the development of web application
requests - allows sending HTTP requests with python to external API
Flask, request, render_template - functions on flask
re - check if the string contains the conditions I defined
-------------------------------------------------------------------
Code review:
Daniel Kohav, 21.12.22
-------------------------------------------------------------------
Written by:
Tom Katzav
'''

app = Flask(__name__)


@app.route('/', methods=['GET'])  # Render home template
def home():
    return flask.send_file("templates/home.html")


def filter_info(info):
    '''
    Gets a json object and filters out irrelevant information.
    returns a string with the necessary information.
    '''
    result = []
    for i in range(7):
        dicts = {}
        date1 = info['days'][i]['datetime']
        date_obj = datetime.strptime(date1, '%Y-%m-%d')
        date1 = date_obj.strftime('%d/%m/%Y')
        day_temp = int((info['days'][i]['hours'][12]['temp'] - 32) * 5 / 9)
        night_temp = int((info['days'][i]['hours'][0]['temp'] - 32) * 5 / 9)
        humidity = int(info['days'][i]['hours'][12]['humidity'])
        keys = ['date', 'day_temp', 'night_temp', 'humidity']
        values = [date1, day_temp, night_temp, humidity]
        for j in range(len(keys)):
            dicts[keys[j]] = values[j]
        result.append(dicts)
    return result


@app.route('/', methods=['POST'])
def weather():
    '''
    Receives the user input, checks if it
    contains only characters A-Z, a-z, and spaces.
    sends a get request to external API,
    and verifies that the status code is 200.
    returns the filtered information to the user.
    '''
    location = request.form.get('user_input')
    if re.match(r'^[a-z A-Z]+$', location) is None:
        return flask.send_file("templates/error_massage.html")
    api = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/ \
            {location}/next6days?key=KNJHCXPMRQUHGP26KUMR5JWQE'
    response = requests.get(api)
    if response.status_code != 200:
        return flask.send_file("templates/error_massage.html")
    info = response.json()
    filter_data = filter_info(info)
    country = info['resolvedAddress']
    return render_template('result.html', title='Weather App', country=country, data=filter_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
