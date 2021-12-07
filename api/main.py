import flask
from flask.templating import render_template
from flask.globals import request
from api import flaskapp


@flaskapp.route("/buy", methods=["POST"])
def buy_ticket():
    order_dict = {
        "username": flask.request.form.get('username'),
        "password": flask.request.form.get('password'),
        "start_time": flask.request.form.get('start_time'),
    }
    confirm_url = login_and_buy(order_dict['username'], order_dict['password'],order_dict['start_time'])
    return confirm_url