# Bike Share Take Home Project
Bike Share take home project

## Introduction
The solution is implemented as a standalone API service written in Python programming language. 
Node.JS would definitely have provided with a faster API but due to time constraints, I picked 
Python. Moreover, the design of the code and the logic therein remains independent of the 
programming language used. 

### Source code
The source code resides in the folder `bike-share`. The design is modularized into:
bikes, stations and sponsors. Ideailly, each of them would have a relational DB table
that is accessed and maniupated by these individual files. The folder contains the following files:
* `main.py`: Contains the wrapper for the complete API including the API routes and accessing the other resources in the folder
* `bikes.py`: Contains the logic for accessing the APIs related to bikes. This depends on the `stations.py` module.
* `stations.py`: Contains the logic for accessing the APIs related to stations and depends on the `sponsors.py` module.
* `sponsors.py`: Contains the logic for accessing the APIs related to sponsors and depends on `stations.py` module.

### Dependencies
The solution utilizes the following three very proven python packages:
* [pandas](https://pypi.org/project/pandas/): This provides easy access to DB style implementations and tabular data manipulations.
* [Flask](https://pypi.org/project/Flask/): Provides an easy web-application framework.
* [Flask-RESTful](https://pypi.org/project/Flask-RESTful/): Provides a convenient wrapper to Flask to implement RESTful API.

## Usage
To 