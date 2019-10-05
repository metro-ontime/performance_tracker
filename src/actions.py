from library import (get_vehicles,
        preprocess_vehicles,
        upload_preprocessed,
        get_preprocessed_data,
        get_schedule,
        process_schedule,
        process_vehicles,
        upload_latest,
        estimate_arrivals)

ACTIONS = {
    'GET_VEHICLES': lambda ctx, dt: get_vehicles(ctx),
    'PREPROCESS_VEHICLES': lambda ctx, dt: preprocess_vehicles(ctx),
    'UPLOAD_PREPROCESSED': lambda ctx, dt: upload_preprocessed(ctx),
    'GET_PREPROCESSED_DATA': lambda ctx, dt: get_preprocessed_data(ctx),
    'PROCESS_VEHICLES': lambda ctx, dt: process_vehicles(ctx, dt),
    'GET_SCHEDULE': lambda ctx, dt: get_schedule(ctx),
    'PROCESS_SCHEDULE': lambda ctx, dt: process_schedule(ctx, dt),
    'UPLOAD_SUMMARY': lambda ctx, dt: upload_latest(ctx, dt),
    'ESTIMATE_ARRIVALS': lambda ctx, dt: estimate_arrivals(ctx)
}
