with open(f"data/line_info/{line_no}/shape.json") as data:
    track = json.load(data)
with open(f"data/line_info/{line_no}/stations.json") as data:
    station_names = json.load(data)["items"]
line = Line(line_no, track, stations, schedule_today)
