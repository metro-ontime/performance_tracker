import pandas as pd
from library.analysis.nextbus import NextBusData

def preprocess_vehicles(ctx):
    lines = ctx.config["METRO_LINES"]
    agency = ctx.config["METRO_AGENCY"]
    preprocessed_path = ctx.tmp.get_abs_path(f"tracking/{agency}/preprocessed.csv")
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
            latest = NextBusData(data).vehicles
        except Exception as exc:
            ctx.logger(f"Error parsing vehicle JSON for line {line}: {exc}")
            continue
        df = pd.concat([df, latest], ignore_index=True, sort=False, join="inner")

    ctx.tmp.write(preprocessed_path, df.to_csv())
    return 0
