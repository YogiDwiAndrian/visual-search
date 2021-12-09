from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import Model, load_model
import numpy as np

class FeatureExtractor:
    # Membuat object dari class
    def __init__(self):
        # load model dari input sampai layer dense3
        base_model = load_model('static/model/model_vgg.h5')
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer("dense").output)
        pass

    def extract(self, img):
        img = img.resize((128, 128)).convert("RGB")
        a = image.img_to_array(img) 
        b = np.expand_dims(a, axis=0)
        x = preprocess_input(b)
        feature = self.model.predict(x)[0]
        return feature / np.linalg.norm(feature)