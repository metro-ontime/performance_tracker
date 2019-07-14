from library.get_vehicles import get_vehicles
from library.prepare_vehicles import prepare_vehicles
from library.get_schedule import get_schedule
from library.process_schedule import process_schedule
from library.process_vehicles import process_vehicles

ACTIONS = {
    'GET_VEHICLES': lambda ctx, dt: get_vehicles(ctx),
    'PREPARE_VEHICLES': lambda ctx, dt: prepare_vehicles(ctx),
    'GET_SCHEDULE': lambda ctx, dt: get_schedule(ctx),
    'PROCESS_SCHEDULE': process_schedule,
    'PROCESS_VEHICLES': process_vehicles
}
