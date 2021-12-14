import os
from PIL import Image
if(os.environ.get("KERAS_BACKEND", None) == 'plaidml'):
    os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"   # nopep8
if("plaidml" in os.environ.get("KERAS_BACKEND", None)):
    import keras

else:
    from tensorflow import keras

from keras.models import load_model
import keras.backend as K


class Encoder:
    def __init__(self, h5):
        self.model = load_model(h5)
        self.w = self.model.get_input_at(0).shape.dims[1]


class ImageAugmentation:
    def __init__(self):
        pass

    def __call__(self, image, w=128, n=100):
        ret = []
        for i in range(n):
            pass
