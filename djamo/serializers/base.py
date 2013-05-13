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
All the serializers should be a subclass of the **Serializer** class.

.. NOTE: Since all the serializers are subclasses of the Serializer class
         all of them have the basic parameters of Serializer like ``required``
"""


class Serializer(object):
    """
    Base class for all the serializer classes. A serializer is a class that
    is responsible for serializing/de-serializing a value for an specific
    field of a document that specified by user in document class.

    :param verbose: Verbose name of the current field.

    :param required: If ``True`` the field is required and should have a value
                     in transaction time. default ``False``

    :param default: Default value of the field.

    :param help_text: Help text to show with forms that represent this field.

    :param form_class: A form field class to use in factory
                       (default: CharField)

    :param form_widget: A form widget *object* to use with form_class
                        (default: TextInput)

    """


    def __init__(self, verbose=None, required=False, default=None,
                 help_text=None, form_class=None, form_widget=None):


        self._required = required
        self._default = default
        self.verbose = verbose or self.__class__.__name__.lower()
        self.help_text = help_text
        self.form_class = form_class
        self.form_widget = form_widget

        if not self.form_class:
            from django.forms import CharField
            self.form_class = CharField

    def validate(self, key, value):
        """
        Validate the ``value`` parameter against current serializer policy
        and riase
        :py:exception: `~djamo.serializers.Serializer.ValidationError`
        if value was not valid.
        """
        if self._required and not value:
            raise self.ValidationError("'%s' field is required" % key)

    def serialize(self, value, **kwargs):
        """
        Serialize the given value.
        """
        return value

    def deserialize(self, value):
        """
        De-serialize the given value
        """
        return value

    @property
    def default_value(self):
        """
        The default value specified by user.
        """
        return self._default

    @property
    def is_required(self):
        """
        Return True if _required set to true.
        """
        return self._required

    def is_valid_value(self, value):
        """
        Check the value against current serializer policy. The difference
        between this method and ``validate`` method is that this method
        just check value to possiblity of a valid value. But ``validate``
        check other parameter too like field requirement.
        """
        raise self.NotImplemented()

    def form_field_factory(self, **kwargs):
        """
        A form field factory to create and returns and instance of a suitable
        form field for current document field.

        :param **kwargs: All the kwargs will pass to form_class constructer.
        """

        construct_data = {
            "label": self.verbose,
            "required": self._required,
            "initial": self._default,
            "help_text": self.help_text,
        }

        if self.form_widget:
            construct_data["widget"] = self._form_widget

        construct_data.update(kwargs)

        return self.form_class(**construct_data)

    class ValidationError(Exception):
        """
        This exception will raise in case of any validation problem.
        """
        pass

    class NotImplemented(Exception):
        """
        This exception will raise if any necessary methods does not
        override in subclasses.
        """
        pass
