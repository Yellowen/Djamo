# -----------------------------------------------------------------------------
#    Djamo - Yetanother Mongodb driver for Django
#    Copyright (C) 2012-2013 Yellowen
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# -----------------------------------------------------------------------------
"""
**Documents** by themselves does not have ability to save to database. To do
that you should use a ``collection`` object. Its easy to use collections
by subclassing the ``Collection`` base class.
"""

from pymongo.collection import Collection as MongoCollection

from djamo.documents import Document


class Collection (MongoCollection, object):
    """
    Djamo implementation of Mongodb collection.
    """

    #: Class that will be use as a document class for this collection. This
    #: class will be responsible for pickling and unpickling data to and
    #: from database.
    document = None

    #: Specify the name of collection in database level. In case of a None
    #: value current collection class name will use in lower case
    name = None

    def __init__(self, create=False, *args, **kwargs):
        from djamo.db import client

        self.name = self.name or self.__class__.__name__.lower()

        # Get the database instance from client
        self.db = client.get_database()

        super(Collection, self).__init__(self.db, self.name, create,
                                         *args, **kwargs)

    def _get_document(self):
        if self.document is not None:
            if issubclass(self.document, Document):
                return self.document

            raise TypeError("document property should be a 'Document' subclass")
        raise TypeError("document property should be not None value")

    def validate_document(self, doc):
        """
        Return a validated instance of the current collection document from
        provided doc parameter.

        :param doc: An instance of the current collection document or a dictionary
                    like object.
        """
        document = self._get_document()

        if isinstance(doc, document):
            return doc

        elif isinstance(doc, dict):
            # Create a new instance of the current collection's document with doc
            # data
            doc_obj = document(doc)
            return doc_obj
        else:
            raise TypeError("'doc_or_docs' should be dict or a list of dict like object")

    def _prepare_data(self, doc_or_docs):
        """
        validate doc_or_docs and create a dictionary data.
        """

        def to_data(document):
            return document.serialize()

        document = self._get_document()

        docs = doc_or_docs
        if isinstance(docs, list) or isinstance(docs, tuple):
            docs = map(self.validate_document, docs)

        elif isinstance(docs, dict):
            docs = [self.validate_document(docs)]

        else:
            raise TypeError("'doc_or_docs' should be dict or a list of dict like object")

        data = map(to_data, docs)

        return data

    def insert(self, doc_or_docs, *args, **kwargs):
        """
        Insert a document(s) into current collection. and return the ``_id``
        value (or list of ``_id`` values) of doc_or_docs or [None] if
        manipulate is False and the documents passed as doc_or_docs do not
        include an ``_id`` field.

        :param doc_or_docs: a document or list of documents to be inserted.

        :param manipulate: (optional): If True manipulate the documents before
                           inserting.

        :param check_keys: (optional): If True check if keys start with ``$`` or
                           contain ``.``, raising InvalidName in either case.

        :param continue_on_error: (optional): If True, the database will not
                                  stop processing a bulk insert if one fails
                                  (e.g. due to duplicate IDs). This makes bulk
                                  insert behave similarly to a series of single
                                  inserts, except lastError will be set if any
                                  insert fails, not just the last one. If
                                  multiple errors occur, only the most recent
                                  will be reported by error().

        :param w: (optional) (integer or string) If this is a replica set,
                  write operations will block until they have been replicated
                  to the specified number or tagged set of servers. w=<int>
                  always includes the replica set primary (e.g. w=3 means write
                  to the primary and wait until replicated to two secondaries).
                  Passing w=0 disables write acknowledgement and all other
                  write concern options.

        :param wtimeout: (optional): (integer) Used in conjunction with w.
                         Specify a value in milliseconds to control how
                         long to wait for write propagation to complete.
                         If replication does not complete in the given
                         timeframe, a timeout exception is raised.

        :param j: (optional): If True block until write operations have
                  been committed to the journal. Ignored if the server is
                  running without journaling.

        :param fsync: (optional): If True force the database to fsync all
                      files before returning. When used with j the server
                      awaits the next group commit before returning.

        """
        data = self._prepare_data(doc_or_docs)
        return super(Collection, self).insert(data, *args, **kwargs)

    def save(self, doc_to_docs, *args, **kwargs):
        """
        save a document(s) into current collection. and return the ``_id``
        value (or list of ``_id`` values) of doc_or_docs or [None] if
        manipulate is False and the documents passed as doc_or_docs do not
        include an ``_id`` field.

        :param doc_or_docs: a document or list of documents to be inserted.

        :param manipulate: (optional): If True manipulate the documents before
                           inserting.

        :param check_keys: (optional): If True check if keys start with ``$`` or
                           contain ``.``, raising InvalidName in either case.

        :param w: (optional) (integer or string) If this is a replica set,
                  write operations will block until they have been replicated
                  to the specified number or tagged set of servers. w=<int>
                  always includes the replica set primary (e.g. w=3 means write
                  to the primary and wait until replicated to two secondaries).
                  Passing w=0 disables write acknowledgement and all other
                  write concern options.

        :param wtimeout: (optional): (integer) Used in conjunction with w.
                         Specify a value in milliseconds to control how
                         long to wait for write propagation to complete.
                         If replication does not complete in the given
                         timeframe, a timeout exception is raised.

        :param j: (optional): If True block until write operations have
                  been committed to the journal. Ignored if the server is
                  running without journaling.

        :param fsync: (optional): If True force the database to fsync all
                      files before returning. When used with j the server
                      awaits the next group commit before returning.

        """
        data = self._prepare_data(doc_or_docs)
        return super(Collection, self).save(data, *args, **kwargs)


    def update(self, spec, doc, *args, **kwargs):
        """
        Update a document(s) in this collection.

        :param spec: A dict or SON instance specifying elements which must
                     be present for a document to be updated

        :param doc: a dict or SON instance specifying the document to be used
                    for the update or (in the case of an upsert) insert - see
                    docs on MongoDB update modifiers

        :param upsert: (optional): perform an upsert if True

        :param manipulate: (optional): If True manipulate the documents before
                           inserting.

        :param check_keys: (optional): If True check if keys start with ``$`` or
                           contain ``.``, raising InvalidName in either case.

        :param multi: (optional): update all documents that match spec,
                      rather than just the first matching document. The
                      default value for multi is currently False, but this
                      might eventually change to True. It is recommended
                      that you specify this argument explicitly for all update
                      operations in order to prepare your code for that change.

        :param w: (optional) (integer or string) If this is a replica set,
                  write operations will block until they have been replicated
                  to the specified number or tagged set of servers. w=<int>
                  always includes the replica set primary (e.g. w=3 means write
                  to the primary and wait until replicated to two secondaries).
                  Passing w=0 disables write acknowledgement and all other
                  write concern options.

        :param wtimeout: (optional): (integer) Used in conjunction with w.
                         Specify a value in milliseconds to control how
                         long to wait for write propagation to complete.
                         If replication does not complete in the given
                         timeframe, a timeout exception is raised.

        :param j: (optional): If True block until write operations have
                  been committed to the journal. Ignored if the server is
                  running without journaling.

        :param fsync: (optional): If True force the database to fsync all
                      files before returning. When used with j the server
                      awaits the next group commit before returning.

        """
        document = self._get_document()

        update_document = map(document.deserialize_item, doc.items())
        super(Collection, self).update(spec, update_document, *args, **kwargs)
