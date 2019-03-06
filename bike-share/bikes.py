import logging 
import pandas as pd
from flask_restful import Resource, abort, fields, marshal_with, reqparse

bike_fields = {
    'id': fields.Integer,
    'station': fields.Integer,
    'is_free': fields.Boolean,
    'trips': fields.Integer
}

BIKES = pd.DataFrame({}, columns=bike_fields.keys(), dtype='uint8')
num_bikes = 0

get_parser = reqparse.RequestParser()
get_parser.add_argument('q', dest='query', default='',
                        type=str, required=False,
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
    if bike_id not in BIKES['id'] or BIKES.empty:
        abort(404, message="Bike ID: {} does not exist!".format(bike_id))

class Bike(Resource):
    '''
        Class for actions on a single bike
    '''
    def get(self, id):
        bike_exists(id)
        args = get_parser.parse_args()
        if args['query'] == '':
            return BIKES.loc[BIKES['id'] == id].to_json(orient='records'), 200
        elif args['query'].lower() == 'trips':
            return BIKES.loc[BIKES['id'] == id, 'trips'], 200
        else:
            return '\{bike/get/{} - something seriously wrong!!\}'.format(id), 400

    def put(self, id):
        from stations import is_station_free, remove_bike_from_station, add_bike_to_station, increment_trip_count
        bike_exists(id)
        args = put_parser.parse_args()
        if args['action'].lower() == 'get':
            if BIKES.loc[BIKES['id'] == id, 'is_free']:
                BIKES.loc[BIKES['id'] == id, 'is_free'] = False
                return BIKES.loc[BIKES['id'] == id].to_json(), 200
            else:
                abort(400, message="Bike ID {} is not free!".format(id))
        elif args['action'].lower() == 'return':
            if BIKES.loc[BIKES['id'] == id, 'is_free']:
                abort(400, message="Bike ID {} is already returned!".format(id))
            else:
                BIKES.loc[BIKES['id'] == id, 'is_free'] = True
                BIKES.loc[BIKES['id'] == id, 'trips'] += 1
                
                # assume to increment the trip count at station where the 
                # bike was checked out from irrespective of the drop-off station
                increment_trip_count(BIKES.loc[BIKES['id'] == id, 'station'].values[0])
                
                if args['station'] >= 0:
                    if is_station_free(args['station']):
                        remove_bike_from_station(id, BIKES.loc[BIKES['id'] == id, 'station'].values[0])
                        BIKES.loc[BIKES['id'] == id, 'station'] = args['station']
                        add_bike_to_station(BIKES['id'] == id, BIKES.loc[BIKES['id'] == id, 'station'].values[0])
                        msg = 'Returned to new station: {}'.format(args['station'])
                    else:
                        msg = 'No space left in proposed station, returned to original station.'
                else:    
                    msg = 'Returned to original station.'
                return msg, 200
    
    def delete(self, id):
        from stations import remove_bike_from_station
        global BIKES
        bike_exists(id)
        remove_bike_from_station(id, BIKES.loc[BIKES['id'] == id, 'station'].values[0])
        BIKES = BIKES.loc[BIKES['id'] != id]
        return 'Deleted Bike ID: {}'.format(id), 204

    
class Bikes(Resource):
    '''
        Class for actions on a list of bikes
    '''
    def get(self):
        if BIKES.empty:
            return "{No bikes in the record}", 400
        return BIKES.to_json(orient='records'), 200
    
    def post(self):
        """
        Adds a new bike to the system.
        """
        from stations import random_station, add_bike_to_station, is_station_free
        global BIKES
        global num_bikes
        new_station = random_station()
        tries = 0
        
        # the randomly selected station may or maynot have a free space for a new bike. 
        # keep trying a maximum of 40 times (total capacity)
        while not is_station_free(new_station) and tries < 40:
            new_station = random_station()
            tries += 1
        if tries == 40:
            abort(404, message="Unable to add any more bikes. Probably all stations are full.")
        
        num_bikes += 1
        new_bike = {
            'id': num_bikes,
            'station': new_station,
            'is_free': True,
            'trips': 0
        }
        
        if BIKES.empty:
            BIKES = pd.DataFrame([new_bike])
        else:
            BIKES = BIKES.append(new_bike, ignore_index=True)
        add_bike_to_station(num_bikes, new_station)
        return str(new_bike), 201

