from flask import render_template
from flask import request
from app import app
from collections import defaultdict
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import urlparse
import numpy as np
import requests
import urllib
import xml.etree.ElementTree as ET
import json
import random
import urllib
import time


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)

@app.route('/analyze', methods=["POST"])
def analyze():
    app = ClarifaiApp(api_key="c306175f36704228af8ccef5332045dd")
    model = app.models.get('general-v1.3')

    allPoints = request.json['pleasework']
    print(allPoints)

    image = ClImage(url='https://samples.clarifai.com/metro-north.jpg')
    aiRes = model.predict([image])
    # print(aiRes)
    return "doneeeee"


@app.route('/api/search', methods=["POST"])
def search():
    cityToSearch = request.json['city']
    # print(test)
    cityBorders = requests.get("https://api.teleport.org/api/urban_areas/slug%3A" + cityToSearch + "/").json()['bounding_box']['latlon']

    print("this is the request")
  
    placesToVisit = [generateRandomPoints(cityBorders) for i in xrange(100)]
    analysis = streetViewAnalyze(placesToVisit)
    # snapToRoadStr = map(toLatLonPair, places_to_visit)
    # snapRequest = '|'.join(map(str, snapToRoadStr)) 
    # print(snapRequest)
    # changedPoints = requests.get("https://roads.googleapis.com/v1/snapToRoads?path=" +snapRequest+ "&key=AIzaSyAeFC4kvVAYZHn0xPeQzcFMg7F_wFO7wA4").json()
    # //print(places_to_visit)
    
# RETURN BOTH THE ARRAY AND ALSO THE ANALYZED RESULTS IN A SINGLE JSON OBJECT
# {arr: [], analyzed: []}
    return json.dumps(analysis)


def generateRandomPoints(cityBorders):

    midLon = (cityBorders['west'] + cityBorders['east']) / 2
    midLat = (cityBorders['south'] + cityBorders['north']) / 2

    gaussianLat = np.random.normal(midLat, 0.05)
    gaussianLon = np.random.normal(midLon, 0.05)

    strLatLon = str(gaussianLat) + "," + str(gaussianLon)

    payload = {'key': 'AIzaSyAeFC4kvVAYZHn0xPeQzcFMg7F_wFO7wA4', 'latlng': strLatLon}
    latLonPair = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=payload).json()['results'][0]['geometry']['location']

    snappedLat = latLonPair['lat']
    snappedLon = latLonPair['lng']

    # print(str(snappedLat) + "," + str(snappedLon))

    # return gaussianLat, gaussianLon
    return snappedLat, snappedLon

def streetViewAnalyze(pointsArr):
    app = ClarifaiApp(api_key="c306175f36704228af8ccef5332045dd")
    model = app.models.get('general-v1.3')
    imageList = []
    allPoints = {}

    for lat,lon in pointsArr:
        params = { 'heading' : "151.78", 
        'size' : "600x400",
        'pitch' : "-0.76",
        'location' : str(lat) + ","+ str(lon)}
        encoded = urllib.urlencode(params)
        streetViewURL = "https://maps.googleapis.com/maps/api/streetview?" + encoded
        imageList.append(ClImage(url=streetViewURL))
    
    A, B = split_list(imageList)
    firstBatch = processImages(model.predict(A), allPoints)
    secondBatch = processImages(model.predict(B), allPoints)

    firstBatch.update(secondBatch)

    # print(firstBatch)
    # print(len(secondBatch))
    return firstBatch
    # time.sleep(10)
    # secondBatch = model.predict(B)
    # print(len(secondBatch))

    

def processImages(outPut, allPoints):
    processed = outPut['outputs']
    for image in processed:
        conceptList = image['data']['concepts']
        conceptsToExport = []
        url = image['input']['data']['image']['url']
        latlon = urlparse.parse_qs(urlparse.urlparse(url).query)['location'][0]
        for concept in conceptList:
            info = {}
            info['name'] = concept['name']
            info['value'] = concept['value']
            conceptsToExport.append(info)
        allPoints[latlon] = conceptsToExport
    return allPoints


def split_list(a_list):
    half = len(a_list)/2
    return a_list[:half], a_list[half:]



def toLatLonPair(x):
    return str(x[0]) + "," + str(x[1])

def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None
