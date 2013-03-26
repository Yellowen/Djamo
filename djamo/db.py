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
from django.conf import settings


class Client(MongoClient):
    """
    Client class for Djamo that is responsible for connection management.
    """

    def __init__(self, **kwargs):
        if hasattr(settings, "DJAMO"):
            if isinstance(settings.DJAMO, dict):

                # Retrieve Mongo server information form settings.py
                host = settings.DJAMO.get("host", "localhost")
                port = int(settings.DJAMO.get("port", 27017))
                db_name = settings.DJAMO.get("name", None)
                max_pool_size = settings.DJAMO.get("max_pool_size", 10)
                tz_awar = settings.USE_TZ

                # TODO: Use our Document implementation
                document_class = settings.DJAMO.get("document_class",
                                                         dict)
                max_age = settings.DJAMO.get("MAX_AGE",
                                                  400)

                # Calculate the client expiration date
                self.expire_time = time.time() + max_age

                if not db_name:
                    raise TypeError("settings.DJAMO does not have 'name' key")

                self._connection = MongoClient(host, port,
                                               max_pool_size,
                                               document_class,
                                               tz_awar,
                                               **kwargs)

                # Get the Database from connection object
                self._db = getattr(self._connection, db_name)

                # TODO: Implement database authentication

            else:
                raise TypeError("settings.DJAMO should be a dictionary")
        else:
            raise AttributeError("settings does not have DJAMO attribute.")

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


client = Client()
