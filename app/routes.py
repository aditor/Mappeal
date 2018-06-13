from flask import render_template
from flask import request
from app import app
from collections import defaultdict
import requests
import urllib
import xml.etree.ElementTree as ET
import json
import random



@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)

@app.route('/api/search', methods=["POST"])
def search():
    cityToSearch = request.json['city']

    city_borders = requests.get("https://api.teleport.org/api/urban_areas/slug%3A" + cityToSearch + "/").json()['bounding_box']['latlon']

    print("this is the request")
  
    places_to_visit = [generate_random_points(city_borders) for i in xrange(100)]

    # snapToRoadStr = map(toLatLonPair, places_to_visit)
    # snapRequest = '|'.join(map(str, snapToRoadStr)) 
    # print(snapRequest)
    # changedPoints = requests.get("https://roads.googleapis.com/v1/snapToRoads?path=" +snapRequest+ "&key=AIzaSyAeFC4kvVAYZHn0xPeQzcFMg7F_wFO7wA4").json()
    # //print(places_to_visit)
    return json.dumps(places_to_visit)


def generate_random_points(city_borders):
    latitude = random.uniform(city_borders['south'], city_borders['north'])
    longitude = random.uniform(city_borders['west'], city_borders['east'])
    return latitude, longitude


def toLatLonPair(x):
    return str(x[0]) + "," + str(x[1])

def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None
