import flask, requests, json
from flask.templating import render_template
from flask.globals import request
import flowbird
app = flask.Flask(__name__)


@app.route("/buy", methods=["POST"])
def buy_ticket():
    order_dict = {
        "username": flask.request.form.get('username'),
        "password": flask.request.form.get('password'),
        "start_time": flask.request.form.get('start_time'),
    }
    confirm_url = flowbird.login_and_buy(order_dict['username'], order_dict['password'],order_dict['start_time'])
    return confirm_url
app.run()