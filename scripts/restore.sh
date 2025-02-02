#!/bin/bash

# Check if backup timestamp is provided
if [ -z "$1" ]; then
    echo "Please provide backup timestamp (YYYYMMDD_HHMMSS)"
    exit 1
fi

TIMESTAMP=$1
BACKUP_DIR="/backups"
APP_DIR="/app/data"
CONFIG_DIR="/app/config"

# Download from S3
aws s3 cp s3://email-validator-backups/app_data/app_data_$TIMESTAMP.tar.gz $BACKUP_DIR/
aws s3 cp s3://email-validator-backups/config/config_$TIMESTAMP.tar.gz $BACKUP_DIR/

# Restore backups
tar -xzf $BACKUP_DIR/app_data_$TIMESTAMP.tar.gz -C /
tar -xzf $BACKUP_DIR/config_$TIMESTAMP.tar.gz -C /

# Clean up downloaded files
rm $BACKUP_DIR/app_data_$TIMESTAMP.tar.gz
rm $BACKUP_DIR/config_$TIMESTAMP.tar.gz

echo "Restore completed successfully"