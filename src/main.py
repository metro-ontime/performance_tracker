import sys
import json
import pendulum
from library.context import Context
from actions import ACTIONS

def main(command, datetime=None):
    with open('fs_config.json', 'r') as infile:
        ctx = Context(json.load(infile))
    if command in ['PROCESS_VEHICLES', 'ESTIMATE_ARRIVALS'] and datetime is None:
        datetime = select_correct_datetime(pendulum.now())
    elif datetime is None:
        datetime = pendulum.now()

    outcome = ACTIONS[command](ctx, datetime)

    if outcome is 0:
        ctx.logger(f"{command} completed successfully")
        return 0
    else:
        ctx.logger(f"{command} failed")
        return 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide command.")
        exit()
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main(sys.argv[1], sys.argv[2])
