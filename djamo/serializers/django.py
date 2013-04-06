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

from django.contrib.auth import get_user_model

from .base import Serializer


class DjangoUser(Serializer):
    """
    Serializer for Django users, This class will de-serialize the data from the
    database to a django user and serialize the user normally to its user id.
    """

    def __init__(self, user_field="pk", *args, **kwargs):
        self.user_field = user_field
        self._user_model = get_user_model()

        super(DjangoUser, self).__init__(*args, **kwargs)

    def serialize(self, value):
        """
        Convert the Django User instance to an string.
        """
        if isinstance(value, self._user_model):
            return getattr(value, self.user_field)

        raise TypeError(
            "'value' should be an instance of '%s'" % self._user_model
        )

    def deserialize(self, value):
        """
        Restore the string to Djano User.
        """
        params = {self.user_field: value}
        return self._user_model.objects.get(**params)
