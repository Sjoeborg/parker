import flask
from api import flaskapp
from api.flowbird import login_and_buy as flowbird_buy
from api.easypark import login_and_buy as easypark_buy
from api.parkster import buy_from_location as parkster_buy

@flaskapp.route("/flowbird", methods=["POST"])
def flowbird():
    status = None
    order_dict = {
        "username": flask.request.form.get('username'),
        "password": flask.request.form.get('password'),
        "start_time": flask.request.form.get('start_time'),
        "duration": flask.request.form.get('duration'),
        "lat": flask.request.form.get('lat'),
        "lon": flask.request.form.get('lon'),
    }
    try:
        status = flowbird_buy(order_dict['username'], order_dict['password'],order_dict['lat'], order_dict['lon'],order_dict['start_time'], order_dict['duration'])
    except AssertionError as e:
        text = 'Error: ' + str(e)
    if status == 'confirmed':
        text = f'Flowbird ticket at {order_dict["lat"], order_dict["lon"]} confirmed.'
    else:
        text = f'Failed. Status is {status}'
    return text

@flaskapp.route("/easypark", methods=["POST"])
def easypark():
    status = None
    order_dict = {
        "username": flask.request.form.get('username'),
        "password": flask.request.form.get('password'),
        "duration": flask.request.form.get('duration'),
        "lat": float(flask.request.form.get('lat')),
        "lon": float(flask.request.form.get('lon')),
    }
    try:
        status = easypark_buy(order_dict['username'], order_dict['password'],order_dict['lat'], order_dict['lon'])
    except AssertionError as e:
        text = 'Error: ' + str(e)
    if status == 'confirmed':
        text = f'Easypark ticket at {order_dict["lat"], order_dict["lon"]} confirmed.'
    else:
        text = f'Failed. Status is {status}'
    return text

@flaskapp.route("/parkster", methods=["POST"])
def parkster():
    status = None
    order_dict = {
        "username": flask.request.form.get('username'),
        "password": flask.request.form.get('password'),
        "lat": float(flask.request.form.get('lat')),
        "lon": float(flask.request.form.get('lon')),
    }
    try:
        status = parkster_buy(order_dict['username'], order_dict['password'],order_dict['lat'], order_dict['lon'])
    except AssertionError as e:
        text = 'Error: ' + str(e)
    if status == 'confirmed':
        text = f'Parkster ticket at {order_dict["lat"], order_dict["lon"]} confirmed.'
    else:
        text = f'Failed. Status is {status}'
    return text