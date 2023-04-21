#!/bin/bash

echo "Running all Draco tests..."
bash /opt/nifi/nifi-current/test/draco/_test_tc1_start_root_group.sh
bash /opt/nifi/nifi-current/test/draco/_test_tc2_draco_process_mnist.sh
