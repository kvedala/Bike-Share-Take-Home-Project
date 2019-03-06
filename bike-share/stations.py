import logging
import pandas as pd
from flask_restful import Resource, abort, fields, marshal_with

station_fields = {
    'id': fields.Integer,
    'sponsor': fields.List(fields.Integer),
    'probability': fields.Integer,
    'capacity': fields.Integer,
    'bike_id': fields.List(fields.Integer)
}

STATIONS = pd.DataFrame([
            {
                'id': 1,
                'sponsor': [1, 2],
                'probability': 50,
                'capacity': 10,
                'bike_id': [],
                'trips': 0
            },
            {
                'id': 2,
                'sponsor': [2, 3],
                'probability': 20,
                'capacity': 5,
                'bike_id': [],
                'trips': 0
            },
            {
                'id': 3,
                'sponsor': [3],
                'probability': 20,
                'capacity': 13,
                'bike_id': [],
                'trips': 0
            },
            {
                'id': 4,
                'sponsor': [1, 3, 4],
                'probability': 10,
                'capacity': 10,
                'bike_id': [],
                'trips': 0
            }
        ])


def random_station():
    """
    Randomly selects a station based on probability weights for each station.
    
    :return: station_id randomly selected station id
    """
    from random import choices
    return choices(STATIONS.loc[:,'id'].values, STATIONS.loc[:,'probability'].values)[0]

    
def station_exists(station_id):
    if station_id > STATIONS.shape[0] or station_id <= 0:
        abort(404, message="Station ID: {} does not exist!".format(station_id))

class Station(Resource):
    '''
        Class for actions on a single station
    '''
    def get(self, id):
        station_exists(id)
        return STATIONS.loc[id-1].to_json(), 200

class Stations(Resource):
    '''
        Class for actions on a list of stations
    '''
    def get(self):
        return STATIONS.to_json(orient='records'), 200
    