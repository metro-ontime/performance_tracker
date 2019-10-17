from library import (get_vehicles,
        preprocess_vehicles,
        upload_preprocessed,
        get_schedule,
        process_schedule,
        process_vehicles,
        produce_summary,
        upload_latest,
        estimate_arrivals)

ACTIONS = {
    'GET_VEHICLES': lambda ctx, dt: get_vehicles(ctx),
    'PREPROCESS_VEHICLES': lambda ctx, dt: preprocess_vehicles(ctx),
    'UPLOAD_PREPROCESSED': lambda ctx, dt: upload_preprocessed(ctx),
    'PROCESS_VEHICLE_DATA': lambda ctx, dt: process_vehicles(ctx, dt),
    'GET_SCHEDULE': lambda ctx, dt: get_schedule(ctx),
    'PROCESS_SCHEDULE': lambda ctx, dt: process_schedule(ctx, dt),
    'PRODUCE_SUMMARY': lambda ctx, dt: produce_summary(ctx, dt),
    'UPLOAD_SUMMARY': lambda ctx, dt: upload_latest(ctx, dt),
    'ESTIMATE_ARRIVALS': lambda ctx, dt: estimate_arrivals(ctx)
}
