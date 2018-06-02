from flask import render_template
from flask import request
from app import app
import requests
import urllib

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)

@app.route('/search')
def search():
    print("this is the address" + request.args.get('address', default = "",type = str))
    zID = 'X1-ZWz1ggc591y5fv_6h6e1'
    address = urllib.quote("Las Vegas Blvd") 
    # request.args.get('fname', default = "",type = str)
    cityzip = 'Nevada'
    total = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=' + zID + '&address=' + address + '&citystatezip=' + cityzip
    print("HERES THE URL" + total)
    r = requests.get(total)
    print(r.content)
    user = {'username': 'TEST!'}
    return render_template('index.html', title='TEST', user=user)