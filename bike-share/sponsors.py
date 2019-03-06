import logging
import pandas as pd
from flask_restful import Resource, abort, fields, marshal_with, reqparse

SPONSORS = pd.DataFrame([
            {
                'id': 1,
                'name': 'Sponsor A',
                'interactions': 0
            },
            {
                'id': 2,
                'name': 'Sponsor B',
                'interactions': 0
            },
            {
                'id': 3,
                'name': 'Sponsor C',
                'interactions': 0
            },
            {
                'id': 4,
                'name': 'Sponsor D',
                'interactions': 0
            }
        ]
num_sponsors = SPONSORS.shape[0]

def sponsor_exists(id):
    """
    Function to check for a valid sponsor and abort if invalid.
    """
    if id not in SPONSORS['id']:
        abort(404, message="Sponsor ID: {} does not exist!".format(id))
    
def increment_sponsor_interaction(id):
    SPONSORS.loc[SPONSORS['id'] == id, 'interactions'] += 1
    
def sponsor_id_from_name(sname):
    """
    Helper function 
    """
    if sname in SPONSORS['name']:
        return SPONSORS.loc[SPONSORS['name'] == sname, 'id'].values[0]
    else:
        abort(404, message='Sponsor "{}" not found!'.format(sname))

def sponsor_name_from_id(id):
    """
    Helper function 
    """
    if id in SPONSORS['id']:
        return SPONSORS.loc[SPONSORS['id'] == id, 'name'].values[0]
    else:
        abort(404, message='Sponsor ID {} not found!'.format(id))
    
get_parser = reqparse.RequestParser()
get_parser.add_argument('q', dest='query', default='',
                        type=str, required=False,
                        choices=('', 'trips'),
                        help='Type of query - "", "trips"')

class Sponsor(Resource):
    """
    Class for Sponsor API interactions
    """
    def get(self, id):
        sponsor_exists(id)
        args = get_parser.parse_args()
        if args['query'] == '':
            return SPONSORS.loc[SPONSORS['id'] == id].to_json(orient='records'), 200
        elif args['query'].lower() == 'trips':
            return str({"interactions": SPONSORS.loc[SPONSORS['id'] == id, 'interactions'].values[0]}), 200
        else:
            return '\{sponsor/get/{} - something seriously wrong!!\}'.format(id), 400
        
    def delete(self, id):
        from stations import remove_sponsor_from_station
        global SPONSORS
        sponsor_exists(id)
        remove_sponsor_from_station(id)
        SPONSORS = SPONSORS.loc[SPONSORS['id'] != id]
        return 'Deleted Sponsor ID: {}'.format(id), 204

post_parser = reqparse.RequestParser()
post_parser.add_argument('name', default='',
                        type=str, required=True,
                        help='Name of the station')
    
class Sponsors(Resource):
    '''
        Class for actions on a list of sponsors
    '''
    def get(self):
        if SPONSORS.empty:
            return "{No sponsors in the record}", 400
        return SPONSORS.to_json(orient='records'), 200
    
    def post(self):
        """
        Adds a new bike to the system.
        """
        from stations import random_station, add_bike_to_station, is_station_free
        global SPONSORS
        global num_sponsors
    
        args = get_parser.parse_args()
        num_sponsors += 1
        new_sponsor = {
            'id': num_sponsors,
            'name': args['name'],
            'interactions': 0
        }
        
        if SPONSORS.empty:
            SPONSORS = pd.DataFrame([new_sponsor])
        else:
            SPONSORS = SPONSORS.append(new_sponsor, ignore_index=True)
        return str(new_sponsor), 201

