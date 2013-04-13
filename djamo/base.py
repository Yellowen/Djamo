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
import time

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class Client(object):
    """
    Client class for Djamo that is responsible for connection management.
    """

    def __init__(self, config=None, **kwargs):
        if not config:
            from django.conf import settings
            from django.core.signals import request_finished

            if hasattr(settings, "DJAMO"):
                if isinstance(settings.DJAMO, dict):
                    # Retrieve Mongo server information form settings.py
                    config = settings.DJAMO

                else:
                    raise TypeError("settings.DJAMO should be a dictionary")
            else:
                raise AttributeError("settings does not have DJAMO attribute.")

        host = config.get("host", "localhost")
        port = int(config.get("port", 27017))
        db_name = config.get("name", None)
        max_pool_size = config.get("max_pool_size", 10)
        tz_awar = config.get("USE_TZ", False)

        # TODO: Use our Document implementation
        document_class = config.get("document_class",
                                    dict)

        # Connection aging options
        max_age = config.get("max_age",
                             400)
        # Calculate the client expiration date
        self.expire_time = time.time() + max_age

        if not db_name:
            raise TypeError("Djamo does not have 'name' key")

        try:
            self._connection = MongoClient(host, port,
                                           max_pool_size,
                                           document_class,
                                           tz_awar,
                                           **kwargs)
        except ConnectionFailure:
            # TODO: Add some loggin here
            raise

        # Get the Database from connection object
        self._db = getattr(self._connection, db_name)
        self.db_name = db_name

        # TODO: Implement database authentication

        if not config:
            # Terminate connection after request finish.
            # This is the default action until Django 1.5
            # Django 1.6 will use Aging by default
            request_finished.connect(self.terminate_connection)

    @property
    def is_expired(self):
        """
        Return True if the current client is expired and should be close.
        """
        if time.time() > self.expire_time:
            return True
        return False

    def get_database(self):
        return self._db

    def drop_database(self):
        self._connection.drop_database(self.db_name)

    def terminate_connection(self, *args, **kwargs):
        self._connection.disconnect()
