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

@app.route('/api/search')
def search():
    output = json.dumps(request.json['stuff'])
    print("this is the request" + output)
    # zID = 'X1-ZWz1ggc591y5fv_6h6e1'
    # address = urllib.quote("Las Vegas Blvd") 
    # # request.args.get('fname', default = "",type = str)
    # city = request.args.get('city', default = "",type = str)
    # # https://en.wikipedia.org/wiki/ISO_3166-1
    # overpass_url = "http://overpass-api.de/api/interpreter"
    # overpass_query = """
    # [out:json];
    # area[name = "New York"];
    # (
    #     way["building"~"residential|housing|terrace|detached|apartments|hotel"](area);
    # );
    # out center;
    # """
    # response = requests.get(overpass_url, 
    #                         params={'data': overpass_query})
    # data = response.json()["elements"]
    # places = []
    # for loc in data:
    # 	di = {}
    # 	di['center'] = loc['center']
    # 	di['type'] = loc['tags']['building']
    # 	try:
    #        di['addr'] = loc['tags']['addr:street']
    #        di['name'] = loc['tags']['name']
    #     except KeyError:
    #        pass

    #     places.append(di)

    # finalDict = {}
    # finalDict['payload'] = places

    # toPass = json.dumps(finalDict)


    # user = {'username': 'TEST!'}

    # return render_template('index.html', placeArr=toPass)
    return {'test':"SANDWICH"};


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