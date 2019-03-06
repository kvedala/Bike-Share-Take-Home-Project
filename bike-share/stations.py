import logging
import pandas as pd
from flask_restful import Resource, abort, fields, marshal_with, reqparse

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
    if len(STATIONS.loc[STATIONS['id'] == station_id, 'bike_id'].values[0]) == STATIONS.loc[STATIONS['id'] == station_id, 'capacity'].values[0]:
        return False
    return True

def remove_sponsor_from_station(sponsor_id, station_id=0):
    """
    Function to update db with sponsor assigned to station.
    """
    station_exists(station_id)
    if station_id > 0:
        if sponsor_id not in STATIONS.loc[STATIONS['id'] == station_id, 'sponsor'].values[0]:
            abort(404, message="Sponsor is not assigned to the station.")
        STATIONS.loc[STATIONS['id'] == station_id, 'sponsor'].values[0].remove(sponsor_id)
    else: # remove sponsor from all stations
        for idx, row in STATIONS.iterrows():
            if sponsor_id in row['sponsor']:
                STATIONS.loc[idx, 'sponsor'].values[0].remove(sponsor_id)
    
    
def add_sponsor_to_station(station_id, sponsor_id):
    """
    Function to update db with sponsor assigned to station.
    """
    station_exists(station_id)
    if sponsor_id in STATIONS.loc[STATIONS['id'] == station_id, 'sponsor'].values[0]:
        abort(404, message="Sponsor is already assigned to the station.")
    STATIONS.loc[STATIONS['id'] == station_id, 'sponsor'].values[0].append(sponsor_id)

def add_bike_to_station(bike_id, station_id):
    """
    Function to update db with bikes assigned to station.
    """
    is_station_free(station_id)
    if bike_id in STATIONS.loc[STATIONS['id'] == station_id, 'bike_id'].values[0]:
        abort(404, message="Shouldn't be seeing this! Bike is already assigned to the station.")
    STATIONS.loc[STATIONS['id'] == station_id, 'bike_id'].values[0].append(bike_id)
    
def remove_bike_from_station(bike_id, station_id):
    """
    Function to update db with bikes assigned to station.
    """
    if bike_id not in STATIONS.loc[STATIONS['id'] == station_id, 'bike_id'].values[0]:
        abort(404, message="Shouldn't be seeing this! Bike is not assigned to the station.")
    STATIONS.loc[STATIONS['id'] == station_id, 'bike_id'].values[0].remove(bike_id)
    
def increment_trip_count(station_id):
    """
    Function to increment db with station trip count and corresponding sponsor interactions by 1.
    """
    from sponsors import increment_sponsor_interaction
    
    STATIONS.loc[STATIONS['id'] == station_id, 'trips'] += 1
    for sponsor_id in STATIONS.loc[STATIONS['id'] == station_id, 'sponsor'].values[0]:
        increment_sponsor_interaction(sponsor_id)

get_parser = reqparse.RequestParser()
get_parser.add_argument('q', dest='query', default='',
                        type=str, required=False,
                        choices=('', 'trips'),
                        help='Type of query - "", "trips"')
put_parser = reqparse.RequestParser()
put_parser.add_argument('action', type=str, required=True,
                        choices=('add', 'remove'),
                        help='Type of action - "add" or "remove" sponsor from the station.')
put_parser.add_argument('sponsor_id', default=0,
                        type=int, required=False,
                        help='Sponsor id to remove.')
put_parser.add_argument('sponsor_name', default='',
                        type=str, required=False,
                        help='Sponsor name to remove.')

class Station(Resource):
    '''
        Class for actions on a single station
    '''
    def get(self, id):
        station_exists(id)
        args = get_parser.parse_args()
        if args['query'] == '':
            return STATIONS.loc[STATIONS['id'] == id].to_json(orient='records'), 200
        elif args['query'].lower() == 'trips':
            return str({"trips": STATIONS.loc[STATIONS['id'] == id, 'trips'].values[0]}), 200
        else:
            return '\{station/get/{} - something seriously wrong!!\}'.format(id), 400
        
    def put(self, id):
        from sponsors import sponsor_id_from_name
        station_exists(id)
        args = put_parser.parse_args()
        if args['sponsor_id'] == 0 and args['sponsor_name'] == '':
            abort(404, message='At least sponsor_id or sponsor_name must be provided.')

        if args['action'].lower() == 'add':
            if args['sponsor_id'] > 0:
                if args['sponsor_id'] not in STATIONS.loc[STATIONS['id'] == id, 'sponsor'].values[0]:
                    STATIONS.loc[STATIONS['id'] == id, 'sponsor'].values[0].append(args['sponsor_id'])
                    return 'Sponsor added', 200
            else:
                sponsor_id = sponsor_id_from_name(args['sponsor_name'])
                if sponsor_id not in STATIONS.loc[STATIONS['id'] == id, 'sponsor'].values[0]:
                    STATIONS.loc[STATIONS['id'] == id, 'sponsor'].values[0].append(sponsor_id)
                return 'Sponsor added', 200
            return '\{\}', 205
        elif args['action'].lower() == 'remove':
            if args['sponsor_id'] > 0:
                if args['sponsor_id'] in STATIONS.loc[STATIONS['id'] == id, 'sponsor'].values[0]:
                    STATIONS.loc[STATIONS['id'] == id, 'sponsor'].values[0].remove(args['sponsor_id'])
                    return 'Sponsor removed', 200
            else:
                sponsor_id = sponsor_id_from_name(args['sponsor_name'])
                if sponsor_id in STATIONS.loc[STATIONS['id'] == id, 'sponsor'].values[0]:
                    STATIONS.loc[STATIONS['id'] == id, 'sponsor'].values[0].remove(sponsor_id)
                return 'Sponsor removed', 200
            return '\{\}', 205

class Stations(Resource):
    '''
        Class for actions on a list of stations
    '''
    def get(self):
        if STATIONS.empty:
            return "{No stations in the record}", 400
        return STATIONS.to_json(orient='records'), 200
