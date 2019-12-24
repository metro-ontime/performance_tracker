import pandas as pd
from library.analysis.nextbus import parse_nextbus_response

# This script is intended to run immediately after
# downloading new vehicle position data.
# Generally we would do that every minute.
# For each line, the process involves:
# - grab the new JSON response from the API
# - grab the currently applicable schedule
# - grab the running list of tracked vehicle positions for this schedule period
# - append the new JSON to the running list
# - write the running list to disk

def preprocess_vehicles(ctx):
    lines = ctx.config["METRO_LINES"]
    agency = ctx.config["METRO_AGENCY"]
    preprocessed_path = ctx.datastore.get_abs_path(f"tracking/{agency}/preprocessed.csv")
    try:
        df = pd.read_csv(preprocessed_path, index_col=0)
    except:
        df = pd.DataFrame(columns=["line", "vehicle_id","direction","report_time","latitude","longitude","predictable"])

    for line in lines:
        try:
            data = ctx.tmp.load_json(f"tracking/{agency}/{line}/latest.json")
        except:
            ctx.logger(f"Vehicle data unavailable for line {line}")
            continue
        try:
            latest = parse_nextbus_response(data)
        except Exception as exc:
            ctx.logger(f"Error parsing vehicle JSON for line {line}: {exc}")
            continue
        df = pd.concat([df, latest], ignore_index=True, sort=False, join="inner")
    
    df = df.dropna()

    # Write to permanent datastore
    ctx.datastore.write(preprocessed_path, df.to_csv())
    return 0
