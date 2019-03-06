import logging 
logging.basicConfig(format='%(asctime)s.%(msecs)03d; %(levelname)s; %(funcName)s:%(lineno)d; %(message)s', 
                    level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
from bikes import Bike, Bikes
from stations import Station, Stations
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

api.add_resource(Bike, '/bike/<int:id>')
api.add_resource(Bikes, '/bikes')
api.add_resource(Station, '/station/<int:id>')
api.add_resource(Stations, '/stations')

if __name__ == '__main__':
    app.run(debug=True)
    