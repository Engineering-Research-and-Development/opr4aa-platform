#!/bin/bash
GREEN=$'\e[0;32m'
RED=$'\e[0;31m'
CYAN=$'\e[0;36m'
NC=$'\e[0m'

TEST_NAME="_test_tc1_create_folder.sh"
echo "========================================================
${CYAN}Starting ${TEST_NAME} ${NC}
========================================================"

# Load ENV variables
source /test/env.sh

echo "HADOOP_HOST: ${HADOOP_NAMENODE_HOST}"
echo "HADOOP_NAMENODE_PORT: ${HADOOP_NAMENODE_PORT}"


while [[ "$(curl --insecure -s -o /dev/null -w ''%{http_code}'' http://${HADOOP_NAMENODE_HOST}:${HADOOP_NAMENODE_PORT})" != "200" ]]
do
echo "Waiting for Hadoop to load..."
    sleep 5s
done

echo "Hadoop started!"

echo "Creating a folder /test on HDFS"

hdfs dfs -mkdir /test

echo "Waiting for creation..."
sleep 3

delete_result=$(hdfs dfs -rm -r /test) # Should return "Deleted /test" if folder has been created

if [ "$delete_result" = "Deleted /test" ]; then
    echo "${GREEN}PASSED${NC} ${TEST_NAME}.sh"
    exit 0
else
    echo "${RED}FAILED${NC} ${TEST_NAME}.sh"
    exit 1
fi
