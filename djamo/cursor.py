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

from pymongo.cursor import Cursor


class DjamoCursor(Cursor):

    def __send_message(self, message):
        """Send a query or getmore message and handles the response.
        """
        db = self.__collection.database
        kwargs = {"_must_use_master": self.__must_use_master}
        kwargs["read_preference"] = self.__read_preference
        kwargs["tag_sets"] = self.__tag_sets
        kwargs["secondary_acceptable_latency_ms"] = (
            self.__secondary_acceptable_latency_ms)
        if self.__connection_id is not None:
            kwargs["_connection_to_use"] = self.__connection_id
        kwargs.update(self.__kwargs)

        try:
            response = db.connection._send_message_with_response(message,
                                                                 **kwargs)
        except AutoReconnect:
            # Don't try to send kill cursors on another socket
            # or to another server. It can cause a _pinValue
            # assertion on some server releases if we get here
            # due to a socket timeout.
            self.__killed = True
            raise

        if isinstance(response, tuple):
            (connection_id, response) = response
        else:
            connection_id = None

        self.__connection_id = connection_id

        try:
            response = helpers._unpack_response(response, self.__id,
                                                self.__as_class,
                                                self.__tz_aware,
                                                self.__uuid_subtype)

        except AutoReconnect:
            # Don't send kill cursors to another server after a "not master"
            # error. It's completely pointless.
            self.__killed = True
            db.connection.disconnect()
            raise
        self.__id = response["cursor_id"]

        print "-Djamo-"*100
        # starting from doesn't get set on getmore's for tailable cursors
        if not self.__tailable:
            assert response["starting_from"] == self.__retrieved, (
                "Result batch started from %s, expected %s" % (
                    response['starting_from'], self.__retrieved))

        self.__retrieved += response["number_returned"]
        self.__data = deque(response["data"])

        if self.__limit and self.__id and self.__limit <= self.__retrieved:
            self.__die()
