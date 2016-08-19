from persistent import Persistent
import transaction


class Foobar(Persistent):
    pass


if __name__ == '__main__':
    from ZEO.ClientStorage import ClientStorage
    from ZODB.DB import DB

    # default storage '1'
    clientstorage = ClientStorage(('127.0.0.1', 8100), '1')
    db = DB(clientstorage)

    conn = db.open()
    root = conn.root()

    root['foobar'] = Foobar()
    transaction.commit()

    # use anthor storage name...
    clientstorage = ClientStorage(('127.0.0.1', 8100), 'foobar')
    db = DB(clientstorage)

    conn = db.open()
    root = conn.root()

    root['foobar'] = Foobar()
    transaction.commit()
