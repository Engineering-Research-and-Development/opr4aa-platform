#!/bin/bash

NIFI_WEB_HTTPS_PORT=8443
SINGLE_USER_CREDENTIALS_USERNAME=admin
SINGLE_USER_CREDENTIALS_PASSWORD=ctsBtRBKHRAx69EqUghvvgEvjnaLjFEB

HADOOP_NAMENODE_HOST=localhost
HADOOP_NAMENODE_PORT=9870

LIVY_HOST=localhost
LIVY_PORT=8998

process_start_datetime=$(date +%Y%m%d%H%M%S)
SPARK_JOB_LOG_PATH="/tmp"
SPARK_JOB_LOG_FILE="${SPARK_JOB_LOG_PATH}/spark_test_${process_start_datetime}.log"