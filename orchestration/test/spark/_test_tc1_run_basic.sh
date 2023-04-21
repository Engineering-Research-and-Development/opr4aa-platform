#!/bin/bash
GREEN=$'\e[0;32m'
RED=$'\e[0;31m'
CYAN=$'\e[0;36m'
NC=$'\e[0m'

TEST_NAME="_test_tc1_run_basic.sh"
echo "========================================================
${CYAN}Starting ${TEST_NAME} ${NC}
========================================================"

# Load ENV variables
source /tmp/test/env.sh

echo "process_start_datetime: ${process_start_datetime}"
echo "SPARK_JOB_LOG_PATH: ${SPARK_JOB_LOG_PATH}"
echo "SPARK_JOB_LOG_FILE: ${SPARK_JOB_LOG_FILE}"


echo "Submitting Spark Job..."

spark-submit /tmp/algorithms/wordcount.py test_file 2>&1 | tee -a "$SPARK_JOB_LOG_FILE"

sleep 10

log_line=$(more ${SPARK_JOB_LOG_FILE} | egrep 'RUNNING')
echo $log_line


if [ -z "$log_line" ]; then
	echo "${RED}FAILED${NC} ${TEST_NAME}.sh"
    exit 1
else
	echo "${GREEN}PASSED${NC} ${TEST_NAME}.sh"
    exit 0
fi
