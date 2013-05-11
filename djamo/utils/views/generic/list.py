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
from django.views.generic.list import MultipleObjectMixin as MOM
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import TemplateResponseMixin, View


class MultipleObjectMixin(MOM):

    collection = None

    def get_queryset(self):
        """
        Get the list of items for this view. This must be an iterable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """
        if self.queryset is not None:
            queryset = self.queryset
            if hasattr(queryset, 'clone'):
                queryset = queryset.clone()

        elif self.collection is not None:
            collection = self.collection()
            queryset = collection.find()
        else:
            raise ImproperlyConfigured("'%s' must define 'queryset' or 'collection'"
                                       % self.__class__.__name__)
        return queryset

    def get_context_object_name(self, object_list):
        """
        Get the name of the item to be used in the context.
        """
        if self.context_object_name:
            return self.context_object_name

        elif hasattr(object_list, 'collection'):
            return '%s_list' % \
                   object_list.collection().__class__.__name__.lower()

        elif self.collection is not None:
            try:
                return "%s_list" % \
                       self.collection.document.__class__.__name__.lower()
            except AssertionError:
                return None
        else:
            return None


class BaseListView(MultipleObjectMixin, View):
    """
    A base view for displaying a list of objects.
    """
    pass


class MultipleObjectTemplateResponseMixin(TemplateResponseMixin):
    """
    Mixin for responding with a template and list of objects.
    """
    template_name_suffix = '_list'

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        try:
            names = super(MultipleObjectTemplateResponseMixin, self).get_template_names()
        except ImproperlyConfigured:
            # If template_name isn't specified, it's not a problem --
            # we just start with an empty list.
            names = []

        # If the list is a queryset, we'll invent a template name based on the
        # app and document name. This name gets put at the end of the template
        # name list so that user-supplied names override the automatically-
        # generated ones.
        if hasattr(self.object_list, 'collection'):
            opts = self.object_list.collection._meta
            names.append("%s/%s%s.html" % (opts.app_label, opts.document_name, self.template_name_suffix))

        return names


class ListView(MultipleObjectTemplateResponseMixin, BaseListView):
    """
    Render some list of objects, set by `self.model` or `self.queryset`.
    `self.queryset` can actually be any iterable of items, not just a queryset.
    """
    pass
