from ZEO.runzeo import ZEOOptions
from ZEO.runzeo import ZEOServer
from ZEO.StorageServer import LockManager
from ZEO.StorageServer import StorageServer
from ZEO.StorageServer import StubTimeoutThread
from ZEO.StorageServer import TimeoutThread
from ZODB.config import FileStorage
from ZEO.monitor import StorageStats

import os


class FileStorageOptions(ZEOOptions):

    def getSectionName(self):
        return self.name


class DynamicStorages(object):

    def __init__(self, server, base_config):
        self.server = server
        self.base_config = base_config
        self.storages = {}

    def __getitem__(self, name):
        try:
            return self.storages[name]
        except KeyError:
            self.create_storage(name)
            return self.storages[name]

    def get(self, name, default=None):
        try:
            return self.storages[name]
        except KeyError:
            self.create_storage(name)
            if name not in self.storages:
                return default
            return self.storages[name]

    def create_storage(self, storage_name):
        options = FileStorageOptions()
        options.blob_dir = os.path.join(self.base_config.blob_dir, storage_name)
        if not os.path.exists(options.blob_dir):
            os.makedirs(options.blob_dir)
        path = os.path.join(self.base_config.path, storage_name)
        if not os.path.exists(path):
            os.makedirs(path)
        options.path = os.path.join(path, 'Data.fs')
        options.name = storage_name
        options.read_only = self.base_config.read_only
        fs = FileStorage(options)
        self.storages[storage_name] = fs.open()

        # need some more registration...
        self.server.zeo_storages_by_storage_id[storage_name] = []
        self.server.stats[storage_name] = stats = StorageStats(
            self.server.zeo_storages_by_storage_id[storage_name])
        if self.server.transaction_timeout is None:
            # An object with no-op methods
            timeout = StubTimeoutThread()
        else:
            timeout = TimeoutThread(self.server.transaction_timeout)
            timeout.setName("TimeoutThread for %s" % storage_name)
            timeout.start()
        self.server.lock_managers[storage_name] = LockManager(storage_name, stats, timeout)

        self.server._setup_invq(storage_name, self.storages[storage_name])

    def __iter__(self):
        return iter(self.storages)

    def iteritems(self):
        return self.storages.items()
    items = iteritems

    def __contains__(self, name):
        return name in self.storages


class DynamicStorageServer(StorageServer):

    def __init__(self, addr, base_config, **kwargs):
        self.transaction_timeout = kwargs.get('transaction_timeout')
        StorageServer.__init__(
            self, addr, DynamicStorages(self, base_config), **kwargs)


class DynamicStorageZEOServer(ZEOServer):

    def create_server(self):
        options = self.options
        self.server = DynamicStorageServer(
            options.address,
            options.storages[0].config,
            read_only=options.read_only,
            client_conflict_resolution=options.client_conflict_resolution,
            invalidation_queue_size=options.invalidation_queue_size,
            invalidation_age=options.invalidation_age,
            transaction_timeout=options.transaction_timeout,
            ssl=options.ssl)

    def open_storages(self):
        """
        override this, storage are opened lazily as they are requested
        from the DynamicStorageServer
        """
        self.storages = {}
