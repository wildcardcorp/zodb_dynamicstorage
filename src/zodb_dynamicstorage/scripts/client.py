from ZODB.blob import Blob
from persistent import Persistent
import transaction
from tempfile import mkdtemp


class Foobar(Persistent):
    pass


if __name__ == '__main__':
    from ZEO.ClientStorage import ClientStorage
    from ZODB.DB import DB

    # default storage '1'
    clientstorage = ClientStorage(
        ('127.0.0.1', 8100), '1',
        blob_dir=mkdtemp())
    db = DB(clientstorage)

    conn = db.open()
    root = conn.root()

    root['foobar'] = Foobar()
    blob = Blob()
    bfile = blob.open('w')
    bfile.write('foobar')
    bfile.close()
    root['foobarblob'] = blob
    transaction.commit()

    # use anthor storage name...
    clientstorage = ClientStorage(
        ('127.0.0.1', 8100), 'foobar',
        blob_dir=mkdtemp())
    db = DB(clientstorage)

    conn = db.open()
    root = conn.root()

    root['foobar'] = Foobar()
    blob = Blob()
    bfile = blob.open('w')
    bfile.write('foobar')
    bfile.close()
    root['foobarblob'] = blob
    transaction.commit()
