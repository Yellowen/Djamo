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
from djamo.cursor import DjamoCursor


class DjamoCollection (MongoCollection, object):
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

    #: Index list for current collection, each element will be a index
    #: dictionary according to mongodb standards. Each element should
    #: be a list with index dictionary as its first element and index
    #: options as its second.
    indexes = []

    cursor = DjamoCursor

    def __init__(self, create=False, *args, **kwargs):
        from djamo.db import client

        self.name = self.name or self.__class__.__name__.lower()

        # Get the database instance from client
        self.db = client.get_database()

        super(DjamoCollection, self).__init__(self.db, self.name, create,
                                         *args, **kwargs)

        if self.indexes:
            map(lambda x: self.ensure_index(x[0], **x[1]),
                self.indexes)

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
            # Return the serialized value of the document
            return document.serialize()

        document = self._get_document()

        docs = doc_or_docs

        if isinstance(docs, list) or isinstance(docs, tuple):
            # If docs were a list or tuple of documents, validate each one
            # and get a document instance with their data for each document
            docs = map(self.validate_document, docs)

        elif isinstance(docs, dict):
            docs = [self.validate_document(docs)]

        else:
            raise TypeError("'doc_or_docs' should be dict or a list of dict like object")

        data = map(to_data, docs)

        return data

    def _prepare_query(self, query):
        """
        Prepare query (spec).
        """
        if query is not None:

            document = self._get_document()

            # Deserialize each item in query by deserialize_item classmethod
            # of document.
            query_list = map(document.deserialize_item, query.items())

            # Create a new dictionary from the list of deserialized queries
            query = {}
            map(lambda x: query.update(x),
                query_list)

            return query

        return None

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
        return super(DjamoCollection, self).insert(data, *args, **kwargs)

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
        return super(DjamoCollection, self).save(data, *args, **kwargs)


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
        spec = self._prepare_query(spec)
        doc = self._prepare_query(doc)
        return super(DjamoCollection, self).update(spec, doc, *args, **kwargs)

    def remove(self, spec_or_id=None, **kwargs):
        """
        Remove a document(s) from this collection. returns A document (dict)
        describing the effect of the remove or None if write acknowledgement
        is disabled.

        .. warning: Calls to remove() should be performed with care, as removed
                    data cannot be restored

        If spec_or_id is None, all documents in this collection will be removed.
        This is not equivalent to calling drop_collection(), however, as
        indexes will not be removed.

        By default an acknowledgment is requested from the server that the
        remove was successful, raising OperationFailure if an error occurred.
        Passing ``w=0`` disables write acknowledgement and all other write
        concern options.

        :param spec_or_id: (optional): a dictionary specifying the documents to
                           be removed OR any other type specifying the value of
                           "_id" for the document to be removed

        :param w: (optional): (integer or string) If this is a replica set,
                  write operations will block until they have been replicated
                  to the specified number or tagged set of servers. w=<int>
                  always includes the replica set primary (e.g. w=3 means write
                  to the primary and wait until replicated to two secondaries).
                  Passing w=0 disables write acknowledgement and all other write
                  concern options.

        :param wtimeout: (optional) (integer) Used in conjunction with w.
                         Specify a value in milliseconds to control how long
                         to wait for write propagation to complete. If
                         replication does not complete in the given timeframe,
                         a timeout exception is raised.

        :param j: (optional) If True block until write operations have been
                             committed to the journal. Ignored if the server is
                             running without journaling.

        :param fsync: (optional) If True force the database to fsync all files
                      before returning. When used with j the server awaits the
                      next group commit before returning.
        """
        super(DjamoCollection, self).remove(spec_or_id, *args, **kwargs)

    def find(self, spec=None, fields=None, *args, **kwargs):
        """
        make queries on database and current collection.

        The spec argument is a prototype document that all results
        must match. For example:

            from .models import UserCollection

            collection = UserCollection()
            collection.find({"username": "Okarin"})

        only matches documents that have a key "username" with value "Okarin".
        Matches can have other keys in addition to "Okarin. The fields argument
        is used to specify a subset of fields that should be included in the
        result documents. By limiting results to a certain subset of fields
        you can cut down on network traffic and decoding time.

        :param spec: (optional) a SON object specifying elements which must be
                     present for a document to be included in the result set.

        :pram fields: (optional) a list of field names that should be returned
                      in the result set or a dict specifying the fields to
                      include or exclude. If fields is a list ``_id`` will
                      always be returned. Use a dict to exclude fields from the
                      result (e.g. fields={`_id`: False}).

        :param skip: (optional) the number of documents to omit (from the start
                     of the result set) when returning the results
        :param limit: (optional) the maximum number of results to return

        :param timeout: (optional) if True, any returned cursor will be subject
                        to the normal timeout behavior of the mongod process.
                        Otherwise, the returned cursor will never timeout at
                        the server. Care should be taken to ensure that cursors
                        with timeout turned off are properly closed.

        :param snapshot: (optional) if True, snapshot mode will be used for this
                         query. Snapshot mode assures no duplicates are
                         returned, or objects missed, which were present at both
                         the start and end of the query`s execution. For
                         details, see the snapshot documentation.

        :param tailable: (optional) the result of this find call will be a
                         tailable cursor - tailable cursors aren`t closed when
                         the last data is retrieved but are kept open and the
                         cursors location marks the final document`s position.
                         if more data is received iteration of the cursor will
                         continue from the last document received. For details,
                         see the tailable cursor documentation.

        :param sort: (optional) a list of (key, direction) pairs specifying the
                     sort order for this query. See sort() for details. max_scan
                     (optional): limit the number of documents examined when
                     performing the query.

        :param as_class: (optional) class to use for documents in the query
                         result (default is document_class)

        :param slave_okay: (optional) if True, allows this query to be run
                           against a replica secondary.

        :param await_data: (optional) if True, the server will block for some
                           extra time before returning, waiting for more data
                           to return. Ignored if tailable is False.

        :param partial: (optional) if True, mongos will return partial results
                        if some shards are down instead of returning an error.

        :param manipulate: (optional) If True (the default), apply any outgoing
                           SON manipulators before returning.

        :param network_timeout: (optional) specify a timeout to use for this
                                query, which will override the MongoClient-level
                                default

        :param read_preference: (optional) The read preference for this query.

        :param tag_sets: (optional) The tag sets for this query.

        :param secondary_acceptable_latency_ms: (optional) Any replica-set
                                                member whose ping time is
                                                within
                                                secondary_acceptable_latency_ms
                                                of the nearest member may
                                                accept reads.
                                                Default 15 milliseconds.
                                                Ignored by mongos and must be
                                                configured on the command line.
                                                See the localThreshold option
                                                for more information.
        """
        # TODO: use a validate parameter in this method to pass to deserialize
        # method of document
        document = self._get_document()
        spec = self._prepare_query(spec)
        result = super(DjamoCollection, self).find(spec, fields, as_class=document,
                                              *args, **kwargs)

        return result
        # deserialize each dictionary and return the document instances
        # list
        deserialized_result = map(lambda x: document().deserialize(x),
                                  result)

        return deserialized_result

    def find_one(self, spec_or_id=None, *args, **kwargs):
        """
        Get a single document from the database. All arguments to find() are
        also valid arguments for find_one(), although any limit argument will
        be ignored. Returns a single document, or None if no matching document
        is found.

        :param spec_or_id: (optional) a dictionary specifying the query to be
                           performed OR any other type to be used as the value
                           for a query for "_id".
        """
        document = self._get_document()
        result = self.find(spec_or_id, limit=-1, *args, **kwargs)
        if result:
            deserialized_result = document().deserialize(result[0])
            return deserialized_result
        return {}
