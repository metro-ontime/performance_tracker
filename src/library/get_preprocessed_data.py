def get_preprocessed_data(ctx):
    if(ctx.config['DATASTORE_NAME'] == 'S3'):
        agency = ctx.config["METRO_AGENCY"]
        try:
            dest = ctx.tmp.get_abs_path(f"tracking/{agency}/preprocessed.csv")           
            src = f"tracking/{agency}/preprocessed.csv"
            ctx.datastore.download(dest, src)
            return 0
        except Exception as e:
            ctx.logger(e)
    else:
        ctx.logger('Datastore set to local filesystem, skipping get_preprocessed_data')
        return 0
            
