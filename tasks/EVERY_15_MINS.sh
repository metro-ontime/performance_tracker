python src/main.py PROCESS_VEHICLES &&
python src/main.py ESTIMATE_ARRIVALS &&
python src/main.py PRODUCE_SUMMARY &&
if [ "$DATASTORE_NAME" == "S3" ]
then
    python src/main.py UPLOAD_SUMMARY &&
    python src/main.py UPLOAD_PROCESSED_VEHICLES
fi