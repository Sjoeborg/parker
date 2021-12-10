import flask
from api import flaskapp
from api import flowbird, parkster, easypark
from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    username = fields.String(required=True, error_messages={"required": {"message": "Username required"}})
    password = fields.String(required=True, error_messages={"required": {"message": "Password required"}})
    start_time = fields.String(required=False)
    duration = fields.String(required=False)
    lat = fields.String(required=True, error_messages={"required": {"message": "Lat required"}})
    lon = fields.String(required=True, error_messages={"required": {"message": "Lon required"}})

class PriceSchema(Schema):
    username = fields.String(required=True, error_messages={"required": {"message": "Username required"}})
    password = fields.String(required=True, error_messages={"required": {"message": "Password required"}})
    end_date = fields.String(required=True, error_messages={"required": {"message": "end_date required"}})
    lat = fields.String(required=True, error_messages={"required": {"message": "Lat required"}})
    lon = fields.String(required=True, error_messages={"required": {"message": "Lon required"}})

@flaskapp.route("/flowbird", methods=["POST"])
def buy_flowbird():
    status = None
    try:
        order_dict = UserSchema().load(flask.request.form.to_dict())
    except ValidationError as err:
        return err.messages, 400
    try:
        status = flowbird.login_and_buy(order_dict['username'], order_dict['password'],order_dict['lat'], order_dict['lon'],order_dict['start_time'], order_dict['duration'])
    except AssertionError as e:
        return 'Error: ' + str(e), 400
    if status == 'confirmed':
        return f'Flowbird ticket at {order_dict["lat"], order_dict["lon"]} confirmed.', 200
    else:
        return f'Failed. Status is {status}', 400

@flaskapp.route("/easypark", methods=["POST"])
def buy_easypark():
    status = None
    try:
        order_dict = UserSchema().load(flask.request.form.to_dict())
    except ValidationError as err:
        return err.messages, 400
    try:
        status = easypark.login_and_buy(order_dict['username'], order_dict['password'],order_dict['lat'], order_dict['lon'])
    except AssertionError as e:
        return 'Error: ' + str(e), 400
    if status == 'confirmed':
        return f'Easypark ticket at {order_dict["lat"], order_dict["lon"]} confirmed.', 200
    else:
        return f'Failed. Status is {status}', 400

@flaskapp.route("/parkster", methods=["POST"])
def buy_parkster():
    status = None
    try:
        order_dict = UserSchema().load(flask.request.form.to_dict())
    except ValidationError as err:
        return err.messages, 400
    try:
        status = parkster.buy_from_location(order_dict['username'], order_dict['password'],order_dict['lat'], order_dict['lon'])
    except AssertionError as e:
        return 'Error: ' + str(e), 400
    if status == 'confirmed':
        return f'Parkster ticket at {order_dict["lat"], order_dict["lon"]} confirmed.', 200
    else:
        return f'Failed. Status is {status}', 400

@flaskapp.route("/price", methods=["GET"])
def price():
    try:
        order_dict = PriceSchema().load(flask.request.form.to_dict())
    except ValidationError as err:
        return err.messages, 400
    result, code = easypark.get_price(order_dict['username'], order_dict['password'], order_dict['lat'], order_dict['lon'], order_dict['end_date'])
    return result, code
    
    