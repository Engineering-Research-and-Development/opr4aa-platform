import logging
import os

# Disable all logging messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # FATAL
logging.getLogger('tensorflow').setLevel(logging.FATAL)

import sys
import tensorflow as tf
import numpy as np
from PIL import Image 
import base64
import io
import requests
from pyspark.sql import SparkSession
import json

spark = SparkSession\
        .builder\
        .getOrCreate()

# Read input file from first argument
response = requests.get(sys.argv[1])
base64encoded = base64.b64encode(response.content).decode('ascii')
imgdata = base64.b64decode(str(base64encoded))
input = Image.open(io.BytesIO(imgdata))
input = np.array(input)
input = input.astype('float32')
input = input / 255.0
input = np.array([input, ])

# Load per-trained model
model = tf.keras.models.load_model('/algorithms/classifier-model/')
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Make prediction
predictions = model.predict(input, verbose=0)

input_file_path = sys.argv[1].rsplit("?")[0]
input_file_path = input_file_path.rsplit("webhdfs/v1")[-1]
input_file_name = input_file_path.rsplit("/")[-1]

# Return label in json object
json_data = {"source_image": input_file_name, "label": class_names[np.argmax(predictions[0])]}
json_string = json.dumps(json_data)

# Upload Result to HDFS
os.system("echo '{json_string}' | hadoop dfs -put - hdfs://hadoop-namenode:9014{output_file_path}"\
    .format(json_string=json_string, output_file_path=sys.argv[2]))
os.system("hadoop dfs -mv hdfs://hadoop-namenode:9014{input_file_path} hdfs://hadoop-namenode:9014/processed/{input_file_name}"
          .format(input_file_path=input_file_path,input_file_name=input_file_name))

