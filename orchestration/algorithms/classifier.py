import logging
import os

# Disable all logging messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # FATAL
logging.getLogger('tensorflow').setLevel(logging.FATAL)

import sys
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image 
import base64
import io
import json

# Read input file from sys.stdin
base64encoded = base64.b64encode(sys.stdin.buffer.read()).decode('ascii')
imgdata = base64.b64decode(str(base64encoded))
input = Image.open(io.BytesIO(imgdata))
input = np.array(input)
input = input.astype('float32')
input = input / 255.0
input = np.array([input, ])

# Load per-trained model
model = tf.keras.models.load_model('classifier-model')
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Make prediction
predictions = model.predict(input, verbose=0)

# Return label in json object
json_data = {"label": class_names[np.argmax(predictions[0])]}
sys.stdout.write(json.dumps(json_data))
