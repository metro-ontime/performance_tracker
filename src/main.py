import sys
import json
import pendulum
from context import Context
from get_vehicles import get_vehicles
from get_schedule import get_schedule
from process_schedule import process_schedule

with open('fs_config.json', 'r') as infile:
    config = json.load(infile)

def main(command, datetime=pendulum.now()):
    ctx = Context(config)
    actions = {
        'GET_VEHICLES': lambda ctx, dt: get_vehicles(ctx),
        'GET_SCHEDULE': lambda ctx, dt: get_schedule(ctx),
        'PROCESS_SCHEDULE': lambda ctx, dt: process_schedule(ctx, dt)
        # 'PROCESS_VEHICLES': process_vehicles,
        # 'ESTIMATE_ARRIVALS': estimate_arrivals,
    }
    output = actions[command](ctx, datetime)
    ctx.logger(output, datetime)
    return 0

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Please provide command.")
        exit()
    main(sys.argv[1])
