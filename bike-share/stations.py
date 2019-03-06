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
    """
    Function to check for a valid station and abort if invalid.
    """
    if station_id not in STATIONS['id']:
        abort(404, message="Station ID: {} does not exist!".format(station_id))

def is_station_free(station_id):
    """
    Function to check if a station is running full capacity.
    
    :return: True if free space available and False otherwise.
    """
    if len(STATIONS.loc[station_id, 'bike_id']) == STATIONS.loc[station_id, 'capacity']:
        return False
    return True

def add_bike_to_station(bike_id, station_id):
    """
    Function to update db with bikes assigned to station.
    """
    is_station_free(station_id)
    if bike_id in STATIONS.loc[station_id, 'bike_id']:
        abort(404, message="Shouldn't be seeing this! Bike is already assigned to the station.")
    STATIONS.loc[station_id, 'bike_id'].append(bike_id)
    
def remove_bike_from_station(bike_id, station_id):
    """
    Function to update db with bikes assigned to station.
    """
    if bike_id in STATIONS.loc[station_id, 'bike_id']:
        abort(404, message="Shouldn't be seeing this! Bike is not assigned to the station.")
    STATIONS.loc[station_id, 'bike_id'].remove(bike_id)

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
    