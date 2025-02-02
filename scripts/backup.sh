#!/bin/bash

# Get current timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Backup directories
BACKUP_DIR="/backups"
APP_DIR="/app/data"
CONFIG_DIR="/app/config"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Create backup of application data
tar -czf $BACKUP_DIR/app_data_$TIMESTAMP.tar.gz $APP_DIR

# Create backup of configuration files
tar -czf $BACKUP_DIR/config_$TIMESTAMP.tar.gz $CONFIG_DIR

# Upload to S3
aws s3 cp $BACKUP_DIR/app_data_$TIMESTAMP.tar.gz s3://email-validator-backups/app_data/
aws s3 cp $BACKUP_DIR/config_$TIMESTAMP.tar.gz s3://email-validator-backups/config/

# Clean up local backups older than 7 days
find $BACKUP_DIR -type f -mtime +7 -name '*.tar.gz' -delete