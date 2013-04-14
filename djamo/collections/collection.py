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

from .base import BaseCollection


class Collection (BaseCollection):

    def update_all(self, spec, doc, *args, **kwargs):
        """
        Update all the documents which matched to spec.

        :param spec: A dict or SON instance specifying elements which must
                     be present for a document to be updated

        :param doc: A dict or SON instance specifying the document to be used
                    for the update or (in the case of an upsert) insert - see
                    docs on MongoDB update modifiers
        """
        kwargs["multi"] = True

        return self.update(spec, doc, *args, **kwargs)
