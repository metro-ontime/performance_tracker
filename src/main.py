#!/usr/bin/env python3.6
import sys
import json
import pendulum
import traceback
from library.context import Context
from actions import ACTIONS

def main(command, datetime=None):
    ctx = Context()
    if datetime is None:
        datetime = pendulum.now(ctx.config["TIMEZONE"])
    else:
        try:
            datetime = pendulum.from_format(datetime, 'YYYY-MM-DD', tz=ctx.config["TIMEZONE"])
            ctx.logger(f"Running in date override mode with date {datetime.format('YYYY-MM-DD')}.")
            ctx.logger("This is an experimental feature and may generate incorrect data.")
        except:
            ctx.logger("Failed to parse custom datetime argument")
            return 1
    try:
        outcome = ACTIONS[command](ctx, datetime)
    except Exception as exc:
        ctx.logger(exc)
        traceback.print_tb(exc.__traceback__)
        ctx.logger(f"{command} failed")
        return 1

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
