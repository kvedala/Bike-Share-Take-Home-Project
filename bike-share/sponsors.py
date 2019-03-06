import logging
import pandas as pd
from flask_restful import Resource

class Sponsor(Resource):
    def __init__(self):
        self.Sponsors = pd.DataFrame([
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
        ])
        
    def get(self):
        return self.Sponsors, 200