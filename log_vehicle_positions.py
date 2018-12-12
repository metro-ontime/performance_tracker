import sys
import os
from datetime import datetime
from logger.grabber import get_vehicles_from_Metro, get_vehicles_from_NextBus

if len(sys.argv) != 3:
    print('Please provide the agency and line number')
    exit()

agency = str(sys.argv[1])
agency_sanitized = agency.replace('-', '_')
line = str(sys.argv[2])

nextbusData = get_vehicles_from_NextBus(agency, line)
os.makedirs("data/vehicles", exist_ok=True)
now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
nextbusData.vehicles.to_csv(f"data/vehicles/{now}.csv")
