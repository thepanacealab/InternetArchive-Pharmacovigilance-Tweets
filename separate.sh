SRC_DIR=/mnt/local/hdd/ramya_work/drugs_tweets/drug_tweets_twitter/2016/Dec
LOG_DIR=/mnt/local/hdd/ramya_work/Log
ARCHIVE_DIR=$SRC_DIR/archive
LOG_FILE=$LOG_DIR/decompress_$(date +%Y%m%d_%H%M%S).log
echo "Logfile name is $LOG_FILE"
echo "$(date +%Y%m%d_%H%M%S): Starting $0" > $LOG_FILE

cd $SRC_DIR
for tar_file in ${SRC_DIR}/*.tar
do
  echo "$(date +%Y%m%d_%H%M%S): Extracting ${tar_file} from ${SRC_DIR}" >> $LOG_FILE
  tar -xf $tar_file
  if [[ $? -ne 0 ]]; then
    echo "$(date +%Y%m%d_%H%M%S): Failed to extract ${tar_file}" >> $LOG_FILE
    exit 1
  fi
  mv $tar_file $ARCHIVE_DIR
  echo "$(date +%Y%m%d_%H%M%S): Moved $tar_file to $ARCHIVE_DIR after successful processing" >> $LOG_FILE
done

echo "$(date +%Y%m%d_%H%M%S): Successfully completed extracting all tar files" >> $LOG_FILE
echo "$(date +%Y%m%d_%H%M%S): Uncompressing all bz2 files from ${SRC_DIR}" >> $LOG_FILE

find . -type f -name '*.bz2' -exec bzip2 -d {} \;
if [[ $? -ne 0 ]]; then
  echo "$(date +%Y%m%d_%H%M%S): Failed to uncompress some bz2 files" >> $LOG_FILE
  exit 1
fi
echo "$(date +%Y%m%d_%H%M%S): Successfully completed compressing bz2 files" >> $LOG_FILE

