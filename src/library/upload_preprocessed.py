def upload_preprocessed(ctx):
    agency = ctx.config["METRO_AGENCY"]
    src = ctx.tmp.get_abs_path(f"tracking/{agency}/preprocessed.csv")
    dest = f"tracking/{agency}/preprocessed.csv"
    ctx.datastore.upload(dest, src)
    return 0
