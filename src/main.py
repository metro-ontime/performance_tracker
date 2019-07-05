import sys
import json
import pendulum
from context import Context
from query_vehicles import query_vehicles

with open('config.json', 'r') as infile:
    config = json.load(infile)

def main(command, datetime=pendulum.now()):
    ctx = Context(config)
    actions = {
        'QUERY_VEHICLES': lambda ctx, dt: query_vehicles(ctx)
        # 'PROCESS_VEHICLES': process_vehicles,
        # 'ESTIMATE_ARRIVALS': estimate_arrivals,
        # 'QUERY_SCHEDULE': query_schedule,
        # 'PROCESS_SCHEDULE': process_schedule
    }
    output = actions[command](ctx, datetime)
    ctx.logger(output, datetime)
    return 0

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Please provide command.")
        exit()
    main(sys.argv[1])
