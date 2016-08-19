from zodb_dynamicstorage.server import DynamicStorageZEOServer
from ZEO.runzeo import ZEOOptions
from ZODB.config import FileStorage
import socket


class Config(object):
    blob_dir = '/opt/zeoserver/data/blobs'
    path = '/opt/zeoserver/data/db'
    name = '1'
    read_only = False

    def getSectionName(self):
        return '1'


if __name__ == '__main__':
    options = ZEOOptions()
    options.address = ('0.0.0.0', 8100)
    options.family = socket.AF_INET
    options.invalidation_queue_size = 100
    fs = FileStorage(Config())
    options.storages = [fs]
    s = DynamicStorageZEOServer(options)
    s.main()
