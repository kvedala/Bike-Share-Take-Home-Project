# Bike Share Take Home Project
Bike Share take home project prompt

## Instructions

Welcome to your technical take home challenge!

Fork this github repository and use it as a starting place for your solution. The final result should be a RESTful api (and implemented service) that can be tested via curl requests, an updated readme or document describing how to use the api, and a link to your code. 

Your project should be able to be built and tested by your reviewer. 

This is merely an exercise and not a full blown deployment; the following are **out of scope** but may be implemented if it makes your, the implementor's, life easier.

* Database, for this exercise it is acceptable to store state in local memory on your service deployment instance.
* Users and Authentication, yes a real bike share obviously needs both of these things, but for the sake of time and complexity please **do not** include them in the system. 

If you get stuck, relax, re-read the question, and think of creative solutions and workarounds, and do your best. The challenge is designed to be open ended, so there is no single correct solution. Implement the requirements as described any way you see fit and fill in the gaps if your design needs details that are not specified in the requirements.

Good luck! 

## Metro Bike Share Requirements

A new bike sharing service, called Metro Bike Share, allows individuals to check bikes out of stations and return them at other stations throughout a metropolitan area.

Metro Bike Share is a RESTful service that consists of many Bikes, Stations, and Sponsors

### Metro Bike Share
The base system for managing bikes

* Individual Bikes and Sponsors can be added to the Bike Share system
* When a new Bike is added to the system, it should be randomly assigned to a home station with available capacity


### Bikes
Obviously no bike share is complete without bikes!

* New Bikes should be able to be created and added to Metro Bike Share.
* Bikes should be able to be checked out of a station and returned to any other station.
* On a per-Bike basis, a queriable trip counter should exist, which shows how many times a bike was checked out and returned. A checkout followed by a return counts as one trip. So a bike that was checked out, returned, and then checked out (but not yet returned), would show a trip counter of 1. When it’s returned, the trip counter would increment to 2.

### Stations

Stations are places where bikes can be rented from. We also have a number of corporate sponsors who want to put their logos on stations. 

* Stations can hold up to either 3, 5, or 10 bikes.
* Bikes should be able to be checked out of a station and returned to any other station with available capacity.
* Allow any number of sponsors to be assigned to stations.
* A station does not allow a bike to be checked in or added if it is already at capacity.

### Adding a new bike to the Bike Share
It is required that we be able to add new bikes into the system throughout it's life cycle. Bikes should be randomly assigned to a "home" station (with remaining capacity) according to a probabilistic station weight, so specific stations gain new bikes faster than others.

* We want to bias new bikes station assignment to a “home” station by station weight.
  * Note that bikes can only have one home station and the odds must add up to 100% across all stations
  * When a bike is assigned to a full station, try to assign it to another station. If all stations are full, return an error.

### Sponsors
As a monetization strategy we want to sell ads on stations to coporate sponsors. In order to show return on investment we need be able to return interaction numbers on a per sponsor basis. 

* A sponsor interaction is any time a bike is checked out or returned to a station with that sponsor attached.
* New sponsors can be added to the bike share at any time.
* Sponsors can be added or removed from individual stations. 
* On a per-Sponsor basis, a queriable interaction counter should exist to track the number of lifetime interactions for a given sponsor.


## Testing

* Write code to test your design.

For your tests, use:

```
# initial data
Station 1: 10
Station 2: 5
Station 3: 3
Station 4: 10

Station 1: Sponsor A and Sponsor B
Station 2: Sponsor B and Sponsor C
Station 3: Sponsor C
Station 4: Sponsor A, Sponsor C, and Sponsor D

Station 1: 50% chance of a bike being assigned to this home station
Station 2: 20% chance of a bike being assigned to this home station
Station 3: 20% chance of a bike being assigned to this home station
Station 4: 10% chance of a bike being assigned to this home station
```

Add several bikes to the system and ensure they can be checked out and returned. 
