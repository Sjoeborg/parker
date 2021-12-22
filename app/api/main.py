import flask
import cv2
import numpy as np
import nanoid
import os
import pickle
import datetime
from . import endpoints as api
from .. import db, Photos
from .integrations import easypark,flowbird, parkster
from marshmallow import Schema, fields, ValidationError
import tensorflow.lite as tflite

dir = os.path.dirname(__file__)
loaded_model = tflite.Interpreter(os.path.join(dir, '../model.tflite'))
loaded_model.allocate_tensors()
output = loaded_model.get_output_details()[0]  # Model has single output.
input = loaded_model.get_input_details()[0]


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

@api.route("/flowbird", methods=["POST"])
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

@api.route("/easypark", methods=["POST"])
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

@api.route("/parkster", methods=["POST"])
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

@api.route("/price", methods=["GET"])
def price():
    try:
        order_dict = PriceSchema().load(flask.request.form.to_dict())
    except ValidationError as err:
        return err.messages, 400
    result, code = easypark.search_and_get_price(order_dict['username'], order_dict['password'], order_dict['lat'], order_dict['lon'], order_dict['end_date'])
    return result, code
    
@api.route("/photo", methods=["POST"])
def receive_photo():
    code = 400
    pickle_file = flask.request.data
    img = pickle.loads(pickle_file)
    #store_in_db(img)
    img = preprocess(img)
    pred = submit_photo(img)
    code = 200
    return pred, code

def store_in_db(data):
    id = nanoid.generate()
    new_photo = Photos(
        id=id,
        data=data,
        date=datetime.datetime.now())
    db.session.add(new_photo)
    db.session.commit()

@api.route("/result", methods=["GET"])
def get_prediction():
    id = flask.request.args.get('id')
    photo = Photos.query.filter_by(id=id).first()
    if photo:
        if photo.prediction is not None:
            return photo.prediction, 200
        else:
            return 'No prediction yet', 200
    else:
        return 'No photo with that id', 400

@api.route("/photo", methods=["GET"])
def get_photo():
    id = flask.request.args.get('id')
    photo = Photos.query.filter_by(id=id).first()
    if photo:
        try:
            return photo.data, 200
        except:
            return 'No photo', 200
    else:
        return 'No photo with that id', 400

def preprocess(img):
    img = img.astype("float32") / 255.0
    img = img.reshape(1, 28, 28, 1)
    return img

def submit_photo(img):
    loaded_model.set_tensor(input['index'], img)
    loaded_model.invoke()
    predictions = np.argmax(loaded_model.get_tensor(output['index']))
    return str(predictions)