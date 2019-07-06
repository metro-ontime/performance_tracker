from lib.get_vehicles import get_vehicles
from lib.get_schedule import get_schedule
from lib.process_schedule import process_schedule

ACTIONS = {
    'GET_VEHICLES': lambda ctx, dt: get_vehicles(ctx),
    'GET_SCHEDULE': lambda ctx, dt: get_schedule(ctx),
    'PROCESS_SCHEDULE': process_schedule,
    'GET_AND_PROCESS_SCHEDULE': lambda ctx, dt: (get_schedule(ctx), process_schedule(ctx, dt))
}
