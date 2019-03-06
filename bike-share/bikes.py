import logging 
import pandas as pd
from flask_restful import Resource, abort, fields, marshal_with, reqparse

bike_fields = {
    'id': fields.Integer,
    'station': fields.Integer,
    'is_free': fields.Boolean,
    'trips': fields.Integer
}

BIKES = pd.DataFrame([{}])

def bike_exists(bike_id):
    if bike_id > BIKES.shape[0] or bike_id <= 0:
        abort(404, message="Bike ID: {} does not exist!".format(bike_id))

class Bike(Resource):
    '''
        Class for actions on a single bike
    ''' 
    def get(self, id):
        bike_exists(id)
        return BIKES.loc[id-1].to_json(), 200
    
    def post(self, id):
        bike_exists(id)


class Bikes(Resource):
    '''
        Class for actions on a list of bikes
    '''
    def get(self):
        return BIKES.to_json(), 200
        