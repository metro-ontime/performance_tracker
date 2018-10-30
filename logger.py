from logger.Database import Database
from logger.Grabber import get_vehicles_from_Metro, get_vehicles_from_NextBus

agency = 'lametro-rail'
agency_sanitized = agency.replace('-', '_')
line = '804'

db = Database('log.db')

metroData = get_vehicles_from_Metro(agency, line)
nextbusData = get_vehicles_from_NextBus(agency, line)

nextbusData.vehicles.to_sql('nextbusLog_gold', db.connection, if_exists='append')
metroData.vehicles.to_sql('metroLog_gold', db.connection, if_exists='append')
db.save_and_close()