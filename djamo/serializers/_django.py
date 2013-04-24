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

from .base import Serializer


class DjangoUser(Serializer):
    """
    Serializer for Django users, This class will de-serialize the data from the
    database to a django user and serialize the user normally to its user id.
    """

    def __init__(self, user_field="pk", *args, **kwargs):
        from django.conf import settings

        self.user_field = user_field

        if settings.AUTH_USER_MODEL != "auth.User":
            from django.contrib.auth import get_user_model
            self._user_model = get_user_model()

        else:
            from django.contrib.auth.models import User
            self._user_model = User

        super(DjangoUser, self).__init__(*args, **kwargs)

    def validate(self, key, value):
        """
        Check for a valid Django user in given value
        """
        super(DjangoUser, self).validate(key, value)

        if not isinstance(value, (self._user_model, int)):
            raise self.ValidationError("value of '%s' is not a Django"
            " user or an integer" % key)

    def serialize(self, value, **kwargs):
        """
        Convert the Django User instance to an string.
        """

        if isinstance(value, self._user_model):
            return getattr(value, self.user_field)

        raise TypeError(
            "'value' should be an instance of '%s'" % self._user_model.__name__
        )

    def deserialize(self, value):
        """
        Restore the string to Djano User.
        """
        params = {self.user_field: value}
        return self._user_model.objects.get(**params)

    def is_valid_value(self, value):
        if isinstance(value, self._user_model):
            return True
        return False
