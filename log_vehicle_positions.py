import sys
import os
import requests
import pendulum
from logger.nextBusData import NextBusData

if len(sys.argv) != 3:
    print("Please provide the agency and line number")
    exit()

agency = str(sys.argv[1])
line = str(sys.argv[2])

now = pendulum.now("UTC")
url = f"http://webservices.nextbus.com/service/publicJSONFeed?command=vehicleLocations&a={agency}&r={line}"
nextBusResponse = requests.get(url)
data = NextBusData(nextBusResponse.json())
print(data.vehicles)
# os.makedirs("data/vehicles", exist_ok=True)
# data.vehicles.to_csv(f"data/vehicles/{now.format("YYYY-MM-DDTHH:mm:ssZ")}.csv")
