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
that is accessed and maniupated by these individual files. For simplicity, in this 
revision, the three data-tables are hard-coded and reside in memory during execution 
and are non-persistent. The folder contains the following files:
* `main.py`: Contains the wrapper for the complete API including the API routes and accessing the other resources in the folder
* `bikes.py`: Contains the logic for accessing the APIs related to bikes. This depends on the `stations.py` module.
* `stations.py`: Contains the logic for accessing the APIs related to stations and depends on the `sponsors.py` module.
* `sponsors.py`: Contains the logic for accessing the APIs related to sponsors and depends on `stations.py` module.

### Dependencies
The solution utilizes the following three very proven python packages:
* [pandas](https://pypi.org/project/pandas/): This provides easy access to DB style implementations and tabular data manipulations.
* [Flask](https://pypi.org/project/Flask/): Provides an easy web-application framework.
* [Flask-RESTful](https://pypi.org/project/Flask-RESTful/): Provides a convenient wrapper to Flask to implement RESTful API.

## Installation
1. To install, clone/download the repository to local drive. 
2. Open a command prompt in this folder and execute the following commands:
    1. On OSX/Linux bash
    ```
    $ export FLASK_APP=bike-share/main.py
    $ flask run
    ```
    2. On Windows command line
    ```
    C:\Bike-Share-Take-Home-Project> set FLASK_APP=bike-share\\main.py
    C:\Bike-Share-Take-Home-Project> flask run
    ```
  3. This should start the Flask API server on `http://127.0.0.1:5000`. Please verify the URL from the messages printed on the command-prompt. 

The APIs are now available to be invoked using `curl` or any of the numerous other API validation tools.

## API Usage
### Bikes
1. `GET /bikes`:
  Returns the complete bikes DB table in JSON format. The bikes are identified by an integer *id*.
2. `POST /bikes`:
  Adds a new bike to the system. The home station is randomly assigned based on the weighted score of the station i.e., higher the score,  greater the probability of the getting assigned a bike.
3. `DELETE /bike/<int:id>`:
  Deletes the bike, whose id is provided in the query, from the DB. The statistics from the use of the bike, in the stations are retained.
4. `GET /bike/<int:id>?q=`: 
  Retrieves information about a particular bike. The response is returned in JSON format. the query parameter `q` is optional and can be *empty* or *'trips'*. If *?q=empty*, complete details of the bike from the bike DB are returned. If *?q=trips*, the number of trips made by the bike are returned in JSON.
