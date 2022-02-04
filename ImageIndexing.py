from os import path
from .saved_kdt import KDT

from . import io_util, ImageProcessing


class ImageIndexing:
    def __init__(self, pth, encoder_h5, database=None, image_augmentation=None):
        self.kdt = KDT.KDT(path.join(pth, 'KDT'), max_cluster=1)
        self.pth = pth
        if(database is None):
            database = io_util.db(path.join(pth, 'db'))
        self.database = database

        if(image_augmentation is None):
            image_augmentation = ImageProcessing.ImageAugmentation()
        self.image_augmentation = image_augmentation

        self.encoder = ImageProcessing.Encoder(encoder_h5)

        self.image_size = self.encoder.image_size

    def vec_id(self, vec):
        # convert numpy float to float for JSON serialize
        vec = tuple([float(f) for f in vec])
        if(vec in self.kdt):
            nn = self.kdt.get_nn(vec, 1)
            dist, vec, node = nn[0]
            assert dist < 1e-3
        else:
            self.kdt.add_vec(vec)

        i = io_util.hashi(vec, length=40)
        while(True):
            s = io_util.base32(i, length=8)
            if(s in self.database):
                vec1 = self.database[s].get('vec')
                d = KDT.dist(vec1, vec)
                if(d > 1e-4):
                    i += 1
                    continue
                else:
                    break
            else:
                self.database[s] = {'vec': vec}
                self.database.save(s)
                break
        return s

    def _add_image(self, image, data=None):
        images = self.image_augmentation(image, image_size=self.image_size)
        for i in images:
            print(i)
        metas, images = [i for i, j in images], [j for i, j in images]
        vecs = self.encoder(images)
        le = len(images)
        for i in range(le):
            meta = metas[i]
            vec = vecs[i]
            vec_id = self.vec_id(vec)
            if(meta.get('original')):
                original_vec = vec_id
                svpth = path.join(self.pth, 'images', "%s.jpg" % vec_id)
                io_util.ensure_dir(svpth)
                image.save(svpth)
        for i in range(le):
            meta = metas[i]
            meta['original_vec'] = original_vec
            vec_id = self.vec_id(vecs[i])
            self.database[vec_id]['meta'] = meta
            if(meta.get('original') and data):
                self.database[vec_id]['user'] = data
            print(self.database[vec_id])
            self.database.save(vec_id)

    def _query_image(self, image, n=5):
        images = self.image_augmentation(
            image, image_size=self.image_size, n=0)
        metas, images = [i for i, j in images], [j for i, j in images]
        vecs = self.encoder(images)
        vec = vecs[0]
        nns = self.kdt.get_nn(vec, n)
        ret = []
        for dist, vec, node in nns:
            vec_id = self.vec_id(vec)
            if(vec_id in self.database):
                if('meta' in self.database[vec_id]):
                    az = {}
                    az.update(self.database[vec_id])
                    az.pop("vec")
                    ret.append((dist, az))
                else:
                    print("no meta??", list(self.database[vec_id]))

            else:
                print("no %s??" % vec_id)
        return ret


if(__name__ == "__main__"):
    from PIL import Image
    from os import path
    encoder_h5 = r"M:\Weiyun Sync\code\ae1\autoencoder\saved\jbb19had\encoder.h5"
    pwd = path.dirname(__file__)

    indexing = ImageIndexing(path.join(pwd, "meow"), encoder_h5)
    img = r"M:\Weiyun Sync\code\nsfw_keras\datas\neg\$@K8L{JNR@KVF%O{CBUNW7G.jpg"
    img = Image.open(img)
    indexing._add_image(img)
    print(indexing._query_image(img))
