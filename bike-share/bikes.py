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

get_parser = reqparse.RequestParser()
get_parser.add_argument('q', dest='query', default='',
                        type=str, required=True,
                        choices=('', 'trips'),
                        help='Type of query - "", "trips"')
put_parser = reqparse.RequestParser()
put_parser.add_argument('action', type=str, required=True,
                        choices=('get', 'return'),
                        help='Type of action - "get" or "return". If "return", optionally provide drop-off station.')
put_parser.add_argument('station',
                        type=int, required=False,
                        help='Optional return station id.')

def bike_exists(bike_id):
    if bike_id not in BIKES.loc['id']:
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
        