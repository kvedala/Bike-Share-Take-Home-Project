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

def increment_sponsor_interaction(id):
    SPONSORS.loc[SPONSORS['id'] == id, 'interactions'] += 1
    
def sponsor_id_from_name(sname):
    if sname in SPONSORS['name']:
        return SPONSORS.loc[SPONSORS['name'] == sname, 'id'].values[0]
    else:
        abort(404, message='Sponsor "{}" not found!'.format(sname))

def sponsor_name_from_id(id):
    if id in SPONSORS['id']:
        return SPONSORS.loc[SPONSORS['id'] == id, 'name'].values[0]
    else:
        abort(404, message='Sponsor ID {} not found!'.format(id))
    
class Sponsor(Resource):
    def get(self):
        return SPONSORS, 200