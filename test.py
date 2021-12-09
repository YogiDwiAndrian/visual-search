from database import insert, check, select
from connection import connect
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model, load_model
import numpy as np
import os
from PIL import Image
from pathlib import Path
from feature_extractor import FeatureExtractor
fe = FeatureExtractor()


# conn = connect()
# image_path = select(conn, 2)
# # total = np.sum(feature)
# print(image_path)

img = Image.open('static/uploaded/2021-11-30T20.17.34.722419_P_8.jpg') # PIL image
feature = fe.extract(img)

# bagi = feature / norm
print(f"fitur : {feature}")
# print(f"fitur 2: {norm}")

# print(f"return asli : {bagi}")

# c = np.array([ 5, 2 ])
# print(np.linalg.norm(c))
# print(c / np.linalg.norm(c))

# for img_path in sorted(Path(f"./static/dataset/scarves").glob("*jpg")):
#     feature = fe.extract(img=Image.open(img_path))
#     insert(feature, id[0],  conn)


