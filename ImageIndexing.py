from os import path
from re import S
import ImageProcessing
from saved_kdt import KDT
from . import io_util, ImageProcessing


class ImageIndexing:
    def __init__(self, pth, encoder_h5, database=None, image_augmentation=None):
        self.kdt = KDT.KDT(path.join(pth, 'KDT'), max_cluster=1)

        if(database is None):
            database = io_util.db(path.join(pth, 'db'))
        self.database = database

        if(image_augmentation is None):
            image_augmentation = ImageProcessing.ImageAugmentation()
        self.image_augmentation = image_augmentation

        self.encoder = ImageProcessing.Encoder(encoder_h5)

        self.image_size=self.encoder.image_size

    def _add_image(self,image):
        images=self.image_augmentation(image_size=self.image_size)
        
        encoded=self.encoder(images)

        