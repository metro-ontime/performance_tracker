from library import (get_vehicles,
        record,
        preprocess_vehicles,
        get_schedule,
        process_schedule,
        process_vehicles,
        upload_latest,
        estimate_arrivals)

ACTIONS = {
    'RECORD': lambda ctx, dt: record(ctx, dt),
    'GET_VEHICLES': lambda ctx, dt: get_vehicles(ctx),
    'PREPROCESS_VEHICLES': lambda ctx, dt: preprocess_vehicles(ctx),
    'PROCESS_VEHICLES': lambda ctx, dt: process_vehicles(ctx, dt),
    'GET_SCHEDULE': lambda ctx, dt: get_schedule(ctx),
    'PROCESS_SCHEDULE': lambda ctx, dt: process_schedule(ctx, dt),
    'UPLOAD_VEHICLES_AND_SUMMARY': lambda ctx, dt: upload_latest(ctx, dt),
    'ESTIMATE_ARRIVALS': lambda ctx, dt: estimate_arrivals(ctx, dt)
}
