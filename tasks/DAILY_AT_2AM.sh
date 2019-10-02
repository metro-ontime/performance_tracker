python src/main.py GET_SCHEDULE &&
python src/main.py PROCESS_SCHEDULE &&
if [ "$DATASTORE_NAME" == "S3" ]
then
    python src/main.py UPLOAD_SCHEDULE
fi