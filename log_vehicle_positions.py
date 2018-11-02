import sys
from logger.database import Database
from logger.grabber import get_vehicles_from_Metro, get_vehicles_from_NextBus

if len(sys.argv) != 3:
    print('Please provide the agency and line number')
    exit()

agency = str(sys.argv[1])
agency_sanitized = agency.replace('-', '_')
line = str(sys.argv[2])

metroData = get_vehicles_from_Metro(agency, line)
nextbusData = get_vehicles_from_NextBus(agency, line)

db = Database('data/log.db')
nextbusData.vehicles.to_sql('nextbusLog_gold', db.connection, if_exists='append')
metroData.vehicles.to_sql('metroLog_gold', db.connection, if_exists='append')
db.save_and_close()
