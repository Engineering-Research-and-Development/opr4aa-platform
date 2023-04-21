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
source /test/env.sh

echo "LIVY_HOST: ${LIVY_HOST}"
echo "LIVY_PORT: ${LIVY_PORT}"


start_response_code=0
LOOPS=15
while [ "$start_response_code" != 200 ]; do

echo "Waiting Livy to start.."

  sleep 15
  let LOOPS--
  if [ $LOOPS -eq 0 ] ; then
    echo 'Livy has not started :( :('
    exit 1
  fi

  start_response_code=$(curl --write-out %{http_code} --silent --output /dev/null --location --request GET "http://${LIVY_HOST}:${LIVY_PORT}/batches" \
  --insecure
  )

done

echo "Sending run batch request..."

response_code=$(curl --write-out %{http_code} --silent --output /dev/null --location --request POST "http://${LIVY_HOST}:${LIVY_PORT}/batches" \
 --header 'Content-Type: application/json' \
 --data '{"file":"/algorithms/toupper.py", "args":["test string"]}' \
 --insecure
)

echo $response_code
if [ "$response_code" = 201 ]; then
    echo "${GREEN}PASSED${NC} ${TEST_NAME}.sh"
    exit 0
else
    echo "${RED}FAILED${NC} ${TEST_NAME}.sh"
    exit 1
fi
