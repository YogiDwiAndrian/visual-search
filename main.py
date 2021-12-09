import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from datetime import datetime
from flask import Flask, request, render_template
import tensorflow as tf
from tensorflow import keras

from database import select
from connection import connect

model = keras.models.load_model("static/model/model_vgg.h5")

def transform_image(pillow_image):
    data = np.asarray(pillow_image)
    data = np.expand_dims(data, axis=0)
    images = np.vstack([data])
    images = tf.image.resize(data, [128, 128])
    return images


def predict(x):
    predictions = model(x)
    pred = predictions[0]
    label = np.argmax(pred)
    # {'backpacks': 0, 'belts': 1, 'blazers': 2, 'boots': 3, 'bottom': 4, 'caps': 5, 'casual': 6, 'clutch': 7, 'coats': 8, 'cocktail': 9, 'flats': 10,
    # 'gloves': 11, 'hairaccessories': 12, 'handbags': 13, 'hats': 14, 'heels': 15, 'jackets': 16, 'jeans': 17, 'jewelry': 18, 'jumpsuit': 19, 'legging': 20, 
    # 'loafers': 21, 'makeup': 22, 'maxi': 23, 'midi': 24, 'mini': 25, 'onepiece': 26, 'pants': 27, 'ponchos': 28, 'sandals': 29, 'satchel': 30, 'scarves': 31, 
    # 'shorts': 32, 'skirts': 33, 'slides': 34, 'sneakers': 35, 'sunglasses': 36, 'sweatpants': 37, 'top': 38, 'twopiece': 39, 'watches': 40, 'wedges': 41}
    return label

fe = FeatureExtractor()
conn = connect()
# Read image features

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        file = request.files["query_img"]

        # Save query img
        img = Image.open(file.stream) # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        rgb_im = img.convert('RGB')
        rgb_im.save(uploaded_img_path)

        # Prediction class
        tensor = transform_image(rgb_im)
        category = predict(tensor)
        features, img_paths = select(conn, category)

        # Run search
        query = fe.extract(img)
        # Mmenhitung jarak euclidean
        dists = np.linalg.norm(features-query, axis=1)
        # indexing 30 hasil teratas
        ids = np.argsort(dists)[:30]  
        scores = [(dists[id], img_paths[id]) for id in ids]


        return render_template("index.html", query_path=uploaded_img_path, scores=scores)
    else:
        return render_template("index.html")


if __name__=="__main__":
    app.run()