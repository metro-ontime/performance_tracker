python src/main.py PROCESS_VEHICLES &&
python src/main.py ESTIMATE_ARRIVALS &&
if [ "$DATASTORE_NAME" == "S3" ]
then
    python src/main.py UPLOAD_VEHICLES_AND_SUMMARY
fi