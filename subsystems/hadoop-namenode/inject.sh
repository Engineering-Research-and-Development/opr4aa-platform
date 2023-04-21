#!/bin/bash
echo "
========================================================

Starting inject.sh

========================================================
"

while [[ "$(curl --insecure -s -o /dev/null -w ''%{http_code}'' http://localhost:9870)" != "200" ]]
do
echo "
========================================================

Waiting for Hadoop to load...

========================================================
"
    sleep 5s
done

echo "
========================================================

Hadoop started!

========================================================
"

hdfs dfs -mkdir /input
hdfs dfs -mkdir /output
hdfs dfs -mkdir /algorithms
hdfs dfs -mkdir /processed

echo "
========================================================

Created folder /input
Created folder /output
Created folder /algorithms
Created folder /processed

========================================================
"
