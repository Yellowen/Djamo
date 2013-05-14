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

from django.forms import Form
from django.forms.forms import DeclarativeFieldsMetaclass

from djamo.utils import six
from djamo.options import Options


class DocumentFormMeta(DeclarativeFieldsMetaclass):
    """
    Meta class for DocumentForm object. This class is responsible for creating
    ``DocumentForm`` instances.

    .. Note:: This class is for Djamo internal usage.
    """

    def __new__(cls, name, bases, attrs):

        new_class = super(DocumentFormMeta, cls).__new__(cls, name, bases, attrs)

        if hasattr(new_class, "Meta"):
            meta = getattr(new_class, 'Meta', None)
            delattr(new_class, "Meta")
        else:
            meta = None

        setattr(new_class, "_meta", Options(meta))
        return new_class


class DocumentForm(six.with_metaclass(DocumentFormMeta, Form)):
    """
    A ModelForm like class to use with Djamo documents.

    Its usage is like Django ModelForm with some extra functionallities. take
    a look at this example::

        from djamo.utils.forms import DocumentFrom

        class StudentForm(DocumentForm):
            class Meta:
                document = Student
                include = ["name", "age"]
                attributes = {"name": TextInput(
                                          attrs={"placeholder": "Name ..."})}


    """
    def __init__(self, *args, **kwargs):

        super(DocumentForm, self).__init__(*args, **kwargs)

        include_list = set(self._meta.include)
        exclude_list = set(self._meta.exclude)

        try:

            fields = self._meta.document._fields
        except AttributeError:
            fields = {}

        if include_list - set(fields.keys()):
            raise AssertionError("You have some fields in 'include' attribute"
                                 "of 'Meta' class")

        fields_keys = set(fields.keys()) - exclude_list

        for key in fields_keys:
            attrs = self._meta.attributes.get(key, {})
            self.fields[key] =  fields[key].form_field_factory(key, **attrs)
