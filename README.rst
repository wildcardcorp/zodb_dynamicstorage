Introduction
============

This package aims to give you the ability to create dynamic storage for
the ZODB ZEO server.

What this means in practice is that you do not need to know ahead of time,
the configuration for all the blob directories and Data.fs files you use.

Long term objective is to be able to use this to have one Plone site use
one Data.fs and blob storage directory.

This can make dramatically increase the ease of moving sites around from server
to server when you use multi-site deployments.


See `src/zodb_dynamicstorage/scripts/client.py` and
`src/zodb_dynamicstorage/scripts/server.py` for examples.
