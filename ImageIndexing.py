from os import path
from saved_kdt import KDT
from . import util
class ImageIndexing:
    def __init__(self,pth,database=None):
        self.kdt=KDT.KDT(path.join(pth,'KDT'),max_cluster=1)
        if(database is None):
            database=util.db(path.join(pth,'db'))
        self.database=database