import os
from PIL import Image
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"   # nopep8
import keras

from keras.models import load_model
import keras.backend as K
from . import misc
import random
import numpy as np
from typing import List


class ImageSizeCantFit(Exception):
    pass


class Encoder:
    # use pretrainded autoencoder to low down the image vector dimension
    def __init__(self, h5):
        self.model = load_model(h5)
        self.image_size = self.model.get_input_at(0).shape.dims[1]

    def __call__(self, images: List[Image.Image]) -> np.ndarray:
        arrs = []
        for img in images:
            w, h = img.size
            if(w != self.image_size or h != self.image_size):
                raise ImageSizeCantFit(
                    "Image size doesn't fit with encoder input")
            arr = img2arr(img)
            arrs.append(arr)
        arrs = np.array(arrs)
        return self.model.predict(arrs)


def img2arr(image):
    arr = np.asarray(image).astype(np.float16)
    arr = arr/127.5-1
    return arr


class ImageAugmentation:
    def __init__(self, n=50):
        self.n = 50

    def __call__(self, image: Image.Image, image_size=128, n=None):
        if(n is None):
            n = self.n
        w, h = image.size
        ret = [[{'original': True, "w": w, "h": h}, image.resize(
            (image_size, image_size), Image.LANCZOS)]]
        for i in range(n):
            # crop
            box = misc.random_crop_box(w, h)
            img = image.crop(box)

            # rotate
            rotation = random.choice([-90, 0, 90, 180])+random.random()*45-22.5
            img = img.rotate(rotation, expand=True)
            img = img.resize((image_size, image_size), Image.LANCZOS)
            x0, y0, x1, y1 = box

            info = {'box': box, 'rotation': rotation,
                    'original': False, 'rel_box': (x0/w, y0/h, x1/w, y1/h)}
            ret.append([info, img])
        return ret
