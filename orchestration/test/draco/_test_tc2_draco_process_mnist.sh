#!/bin/bash
GREEN=$'\e[0;32m'
RED=$'\e[0;31m'
CYAN=$'\e[0;36m'
NC=$'\e[0m'

TEST_NAME="_test_tc2_draco_process_mnist.sh"
echo "========================================================
${CYAN}Starting ${TEST_NAME} ${NC}
========================================================"

# Load ENV variables
source /opt/nifi/nifi-current/test/env.sh

# Test specific variables
DRACO_INPUT_FOLDER="/opt/nifi/nifi-current/input"
DRACO_OUTPUT_FOLDER="/opt/nifi/nifi-current/output"
TEST_IMAGE_PATH="/test_input/Figure_0.png"
GROUP_ID=root

echo "GROUP_ID: ${GROUP_ID}"
echo "NIFI_WEB_HTTPS_PORT: ${NIFI_WEB_HTTPS_PORT}"
echo "SINGLE_USER_CREDENTIALS_USERNAME: ${SINGLE_USER_CREDENTIALS_USERNAME}"
echo "SINGLE_USER_CREDENTIALS_PASSWORD: ${SINGLE_USER_CREDENTIALS_PASSWORD}"

token=$(curl -sS --location --request POST "https://draco:${NIFI_WEB_HTTPS_PORT}/nifi-api/access/token" \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode "username=${SINGLE_USER_CREDENTIALS_USERNAME}" \
--data-urlencode "password=${SINGLE_USER_CREDENTIALS_PASSWORD}" \
--insecure
)

LOOPS=15
while [ -z "$token" ]; do

echo "Fetching NiFi Access Token.."

  sleep 15
  let LOOPS--
  if [ $LOOPS -eq 0 ] ; then
    echo 'NiFi has not started :( :('
    exit 1
  fi

  token=$(curl -sS --location --request POST "https://draco:${NIFI_WEB_HTTPS_PORT}/nifi-api/access/token" \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "username=${SINGLE_USER_CREDENTIALS_USERNAME}" \
  --data-urlencode "password=${SINGLE_USER_CREDENTIALS_PASSWORD}" \
  --insecure
  )

done

echo "Starting process group: ${GROUP_ID}"

start_result=$(curl --write-out %{http_code} --silent --output /dev/null --location --request PUT "https://draco:${NIFI_WEB_HTTPS_PORT}/nifi-api/flow/process-groups/${GROUP_ID}" \
 --header 'Content-Type: application/json' \
 --header "Authorization: Bearer ${token}" \
 --data '{"id":"'${GROUP_ID}'", "state":"RUNNING"}' \
 --insecure
)

if [ "$start_result" != 200 ]; then
    echo "${RED}FAILED${NC} ${TEST_NAME}.sh"
    exit 1
fi

output_files_count=$(ls ${DRACO_OUTPUT_FOLDER} | wc -l)

echo "Ingesting test image file ${TEST_IMAGE_PATH} into draco at ${DRACO_INPUT_FOLDER}"
cp ${TEST_IMAGE_PATH} ${DRACO_INPUT_FOLDER}

if [ $? != 0 ]; then
   echo "${RED}FAILED${NC} ${TEST_NAME}.sh"
   exit 1
fi

echo "Waiting for processing..."

sleep 150s

if [ "$output_files_count" -eq "$(ls ${DRACO_OUTPUT_FOLDER} | wc -l)" ]; then
  echo "${RED}FAILED${NC} ${TEST_NAME}.sh"
  curl --silent --output /dev/null --location --request PUT "https://draco:${NIFI_WEB_HTTPS_PORT}/nifi-api/flow/process-groups/${GROUP_ID}" \
   --header 'Content-Type: application/json' \
   --header "Authorization: Bearer ${token}" \
   --data '{"id":"'${GROUP_ID}'", "state":"STOPPED"}' \
   --insecure
  exit 1
fi

echo "Stopping process group: ${GROUP_ID}"
curl --silent --output /dev/null --location --request PUT "https://draco:${NIFI_WEB_HTTPS_PORT}/nifi-api/flow/process-groups/${GROUP_ID}" \
   --header 'Content-Type: application/json' \
   --header "Authorization: Bearer ${token}" \
   --data '{"id":"'${GROUP_ID}'", "state":"STOPPED"}' \
   --insecure
sleep 5
echo "${GREEN}PASSED${NC} ${TEST_NAME}.sh"
exit 0
