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
from six import with_metaclass


class DocumentMeta(type):
    """
    Meta class for Document object.
    """

    def __new__(cls, name, bases, obj_dict):
        if "keys" in obj_dict:
            obj_dict["_keys"] = obj_dict["keys"]
            del obj_dict

        return type.__new__(cls, name, bases, obj_dict)



class Document(dict):
    """
    Djamo implementation of Document.
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
        # user provieded data on "keys" attribute in document
        # defination.
        for key in _keyset - keyset:
            # for each key that user provided in the "keys"
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
        Validate the current document against provided validators.
        """

        map(self._validate_value, self)
