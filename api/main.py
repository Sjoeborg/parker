import flask
from flask.templating import render_template
from flask.globals import request
from api import flaskapp
from api.flowbird import login_and_buy as flowbird_buy


@flaskapp.route("/buy", methods=["POST"])
def buy_ticket():
    order_dict = {
        "username": flask.request.form.get('username'),
        "password": flask.request.form.get('password'),
        "start_time": flask.request.form.get('start_time'),
        "duration": flask.request.form.get('duration'),
        "lat": flask.request.form.get('lat'),
        "long": flask.request.form.get('long'),
    }
    try:
        status = flowbird_buy(order_dict['username'], order_dict['password'],order_dict['start_time'], order_dict['duration'], order_dict['lat'], order_dict['long'])
    except AssertionError as e:
        text = 'Error: ' + str(e)
    if status == 'confirmed':
        text = f'Ticket at {order_dict["lat"], order_dict["long"]} confirmed. \n Start time: {order_dict["start_time"]}, duration: {order_dict["duration"]}'
    else:
        text = f'Failed. Status is {status}'
    return text