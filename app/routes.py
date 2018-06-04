from flask import render_template
from flask import request
from app import app
from collections import defaultdict
import requests
import urllib
import xml.etree.ElementTree as ET
import json

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)

@app.route('/api/search', methods=["POST"])
def search():
    inputLat = json.dumps(request.json['stuff'][0])
    inputLon = json.dumps(request.json['stuff'][1])
    print("this is the request")

    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];
    area["ISO3166-1"="US"][admin_level=2];
    (
        way(around:10000,"""+str(inputLat)+""","""+str(inputLon)+""")["building"~"residential|housing|terrace|detached|apartments|hotel"](area);
    );
    out center;
    """
    print(overpass_query);
    response = requests.get(overpass_url, 
                            params={'data': overpass_query})
    data = response.json()["elements"]
    places = []
    for loc in data:
    	di = {}
    	di['center'] = loc['center']
    	di['type'] = loc['tags']['building']
    	try:
           di['addr'] = loc['tags']['addr:street']
           di['name'] = loc['tags']['name']
        except KeyError:
           pass

        places.append(di)

    finalDict = {}
    finalDict['payload'] = places

    toPass = json.dumps(finalDict)


    # user = {'username': 'TEST!'}

    # return render_template('index.html', placeArr=toPass)
    return toPass


def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None

    # with open('data2.txt', 'w') as outfile:
    #     json.dump(data, outfile)

    # print("DATAAA" + str(data))
    # pp_json(str(data))



    # total = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=' + zID + '&address=' + address + '&citystatezip=' + cityzip
    # print("HERES THE URL" + total)
    # r = requests.get(total)
    # treeRoot = ET.parse(r.content)

    # for result in root.findall('result'):
    #     rank = country.find('rank').text
    #     name = country.get('name')
    #     print(name, rank)