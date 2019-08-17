import pandas as pd
from library.analysis.nextbus import NextBusData

def prepare_vehicles(ctx):
    lines = ctx.config["METRO_LINES"]
    agency = ctx.config["METRO_AGENCY"]
    for line in lines:
        data = ctx.tmp.load_json(f"tracking/{agency}/{line}/latest.json")
        try:
            latest = NextBusData(data).vehicles
        except:
            return 1
        
        df_path = ctx.tmp.get_abs_path(f"tracking/{agency}/{line}/preprocessed.csv")
        try:
            df = pd.read_csv(df_path, index_col=0)
            df = pd.concat([df, latest], ignore_index=True, sort=False, join="inner")
        except:
            df = latest

        ctx.tmp.write(df_path, df.to_csv())

    return 0
