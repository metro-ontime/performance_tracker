python src/main.py GET_VEHICLES &&
python src/main.py PREPROCESS_VEHICLES &&
if [ "$DATASTORE_NAME" == "S3" ]
then
    python src/main.py UPLOAD_PREPROCESSED
fi