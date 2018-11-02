import urllib.request
from .metroResponse import MetroResponse
from .nextBusResponse import NextBusResponse

def get_vehicles_from_Metro(agency, line):
    url = f"http://api.metro.net/agencies/{agency}/routes/{line}/vehicles/"
    return MetroResponse(make_request(url))

def get_vehicles_from_NextBus(agency, line):
    url = f"http://webservices.nextbus.com/service/publicJSONFeed?command=vehicleLocations&a={agency}&r={line}"
    return NextBusResponse(make_request(url))

def make_request(url):
    request = urllib.request.Request(url)
    request.add_header('Accept', 'application/json')
    response = urllib.request.urlopen(request)
    return response
