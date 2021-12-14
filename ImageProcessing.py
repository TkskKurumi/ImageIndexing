import os
from PIL import Image
from numpy.lib.function_base import _parse_gufunc_signature
if(os.environ.get("KERAS_BACKEND", None) == 'plaidml'):
    os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"   # nopep8
if("plaidml" in os.environ.get("KERAS_BACKEND", None)):
    import keras

else:
    from tensorflow import keras

from keras.models import load_model
import keras.backend as K
import misc
import random
import numpy as np


class ImageSizeCantFit(Exception):
    pass


class Encoder:
    # use pretrainded autoencoder to low down the image vector dimension
    def __init__(self, h5):
        self.model = load_model(h5)
        self.image_size = self.model.get_input_at(0).shape.dims[1]

    def __call__(self, images):
        arrs = []
        for img in images:
            w, h = img.size
            if(w != self.image_size or h != self.image_size):
                raise ImageSizeCantFit("Image size doesn't fit with encoder input")
            arr = img2arr(img)
            arrs.append(arr)
        arrs = np.array(arrs)
        return self.model.predict(arrs)


def img2arr(image):
    arr = np.asarray(image).astype(np.float16)
    arr = arr/127.5-1
    return arr


class ImageAugmentation:
    def __init__(self):
        pass

    def __call__(self, image: Image.Image, image_size=128, n=50):
        w, h = image.size
        min_size = min(w, h)*0.07
        ret = []
        for i in range(n):
            # crop
            le, ri = misc.random_interval(mingap=min_size, scale=w)
            size = ri-le
            up = random.randrange(h-size)
            lo = up + size
            img = Image.crop((le, up, ri, lo))

            # rotate
            rotation = random.choice([-90, 0, 90, 180])+random.random(45)-22.5
            img = img.rotate(rotation, expand=True)
            img = img.resize((image_size, image_size), Image.LANCOS)

            ret.append(img)
        return ret
