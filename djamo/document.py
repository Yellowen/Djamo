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
To create document you should subclass the **Document** or any subclasses of
that.
"""
from six import with_metaclass


class DocumentMeta(type):
    """
    Meta class for Document object. This class is responsible for creating
    ``Document`` instances.

    .. Note:: This class is for Djamo internal usage.
    """

    def __new__(cls, name, bases, obj_dict):

        # Create the empty _keys dictionary
        obj_dict["_fields"] = {}
        if "fields" in obj_dict:

            # replace _keys with "keys" property
            obj_dict["_fields"] = obj_dict["fields"]
            del obj_dict["fields"]

        return type.__new__(cls, name, bases, obj_dict)


class Document(with_metaclass(DocumentMeta, dict)):
    """
    Djamo implementation of Document. Each document can have any
    number of key/value pairs as user want, there is no limit. But
    if user wants to provides some options and details about an
    specific key he/she should add a ``keys`` property to their
    subclass. ``keys`` is a dictionary object. Each key of ``keys``
    property would be a document key and its value would be
    another dictionary with some specific key/value. for example::

        class students (Document):
            keys = {"name": {"required": True},
                    "uid": {"default": "0000000",
                            "serializer": UID()}
                   }

    .. Note:: Remember that provide a ``keys`` attribute is optional
    """

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            super(Document, self).__init__(args[0])
        else:
            super(Document, self).__init__(kwargs)

        # User provided keys in subclass
        _keyset = set(self._fields)

        # The keys that user passed to init method
        keyset = set(self.keys())

        # Create a key and put a default value in it base on
        # user provieded data on ``keys`` attribute in document
        # defination.
        for key in _keyset - keyset:
            # for each key that user provided in the ``fileds``
            # dictionary on document difination
            if self._fields[key].default_value:
                self[key] == self._fields[key].default_value

    def __getattr__(self, name):
        if name in self.keys():
            return self[name]

        raise AttributeError("No attribute called '%s'." % name)

    def __setattr__(self, name, value):
        if name in self.keys():
            self[name] = value
        else:
            raise AttributeError("No attribute called '%s'." % name)

    def __delattr__(self, name):
        if name in self.keys():
            del self[name]
        else:
            raise AttributeError("No attribute called '%s'." % name)

    def _validate_value(self, key):
        """
        Validate a value of an specific key against user provided
        validator of the serializer class and current document validate_<key>
        """
        # Call each validator
        if key in self._fields:
            self._fields["key"].validate((self[key]))

        # Call current document validate_<key>
        validator = getattr(self, "validate_%s" % key, None)
        if validator:
            validator(self[key])


    def validate(self):
        """
        Validate the current document against provided validators of serializer
        and current document validate_<key> method for each ``key``.
        """

        map(self._validate_value, self)

    def _serialize_key(self, key):
        """
        Serialize each key/value and return a tuple like:
        (key, serialized_value)
        """
        if key in self._fields:
            return (key, self._fields[key].serialize(self[key]))

        return (key, self[key])

    def serialize(self):
        """
        This method is responsible for serializing document data to put
        into database. The important thing to know here is that this method
        use serializer of each key to serialize and deserialize data. If
        no serializer sepcified, ``serialize`` method will treat data
        just like common python data types withou serialization.

        This method will return a dictionary from serialized data.

        """
        self.validate()
        return dict(map(self._serialize_key, self))

    def _deserialize_key(self, item):
        """
        de-serialize each key/value using a serializer.
        """
        key, value = item

        if key in self._fields:
            self[key] = self._fields[key].deserialize(value)
            return True

        self[key] = value

    def deserialize(self, data=None, validate=True, clear=True):
        """
        This method is responsible for de-serializing document data from
        database. If there was a serializer for a key it will call that
        otherwise simply treat the value like a python data type.

        :param data: (optional) A dict-like data to de-serialize in current
                     Document instance. If no data provided deserialize
                     method will use current keys/values of docuemnt
                     and serialize them in their place.

        :param validate: (optional) de-serializer will validate de-serialized
                         data after de-serializing process. *default*: **True**

        :param clear: (optional) This argument cause all the current data of
                      this Document instance clear before deserialization.
        """

        if data and not isinstance(data, dict):
            raise TypeError("'data' should be dict-like object")

        if data and clear:
            # Clear current keys and values
            self.clear()

        if not data:
            data = self
            print "no data"

        map(self._deserialize_key, (data.items()))

        if validate:
            self.validate()

        return self

    @classmethod
    def deserialize_item(cls, item):
        """
        Deserialize a query that stored in ``item`` tuple like: (key, value)
        """
        fields = getattr(cls, "fields", None)
        if fields and isinstance(fields, dict):
            if item[0] in fields:
                # deserialize the value using serializer specified by user
                return fields[item(0)].deserialize(item[1])

        return {item[0]: item[1]}
