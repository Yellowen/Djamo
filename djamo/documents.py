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
        if "keys" in obj_dict:
            obj_dict["_keys"] = obj_dict["keys"]
            del obj_dict

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
                            "validators": [String(max_length=30)]}
                   }

    .. Note:: Remember that provide a ``keys`` attribute is optional
    """

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            super(Document, self).__init__(args[0])
        else:
            super(Document, self).__init__(kwargs)

        # User provided keys in subclass
        _keyset = set(self._keys)

        # The keys that user passed to init method
        keyset = set(self.keys())

        # Create a key and put a default value in it base on
        # user provieded data on ``keys`` attribute in document
        # defination.
        for key in _keyset - keyset:
            # for each key that user provided in the ``keys``
            # dictionary on document difination
            if "default" in self._keys[key]:
                self[key] == self._keys[key]["default"]

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
        validator classes and current document validate_<key>
        """

        # Call each validator
        if key in self._keys and "validators" in self._keys[key]:
            map(self._keys["validators"],
                lambda x: x.validate(self[key]))

        # Call current document validate_<key>
        validator = getattr(self, "validate_%s" % key, None)
        if validator:
            validator()


    def validate(self):
        """
        Validate the current document against provided validators and
        current document validate_<key> method for each ``key``.
        """

        map(self._validate_value, self)

    def serialize(self):
        pass

    def deserialize(self, data):
        pass

    class ValidationError(Exception):
        """
        This exception will raise by validators objects or the validation
        methods in case of any validation problem.
        """
        pass
