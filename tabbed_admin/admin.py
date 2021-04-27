from django.conf import settings
from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin, ModelAdmin
from django.db.models.constants import LOOKUP_SEP
from django.utils.translation import ugettext_lazy as _

from .settings import USE_JQUERY_UI, JQUERY_UI_CSS, JQUERY_UI_JS

class AdminBaseWithSelectRelated(BaseModelAdmin):
    """
    Admin Base using list_select_related for get_queryset related fields
    """
    list_select_related = False
    def get_queryset(self, request):

        if self.list_select_related == False:
            return super(AdminBaseWithSelectRelated, self).get_queryset(request)
        else:
            return super(AdminBaseWithSelectRelated, self).get_queryset(request).select_related(*self.list_select_related)

    def form_apply_select_related(self, form):

        if self.list_select_related == False:
            pass
        else:
            for related_field in self.list_select_related:
                splitted = related_field.split(LOOKUP_SEP)

                if len(splitted) > 1:
                    field = splitted[0]
                    related = LOOKUP_SEP.join(splitted[1:])
                    form.base_fields[field].queryset = form.base_fields[field].queryset.select_related(related)

class AdminInlineWithSelectRelated(admin.TabularInline, AdminBaseWithSelectRelated):
    """
    Admin Inline using list_select_related for get_queryset and get_formset related fields
    """
    template = 'tabbed_admin/edit_inline/tabular_inline_table.html'
    def get_formset(self, request, obj=None, **kwargs):
        formset = super(AdminInlineWithSelectRelated, self).get_formset(request, obj, **kwargs)
        self.form_apply_select_related(formset.form)
        return formset

class TabbedModelAdmin(admin.ModelAdmin, AdminBaseWithSelectRelated):
    tabs = None
    formatted_tabs = {}

    # Needs a specific template to display the tabs
    change_form_template = 'tabbed_admin/change_form.html'

    def get_form(self, request, obj=None, **kwargs):
        form = super(TabbedModelAdmin, self).get_form(request, obj, **kwargs)
        self.form_apply_select_related(form)
        return form

    def get_fieldsets(self, request, obj=None):
        """
        Overwrites BaseModelAdmin fieldsets to add fieldsets passed by the
        tabs.
        If the tabs attribute is not set, use the default ModelAdmin method.
        """
        tabs_fieldsets = self.get_formatted_tabs(request, obj)['fieldsets']
        if self.tabs is not None:
            self.fieldsets = ()
        self.fieldsets = self.add_tabbed_item(tabs_fieldsets, self.fieldsets)
        return super(TabbedModelAdmin, self).get_fieldsets(request, obj)

    def get_inline_instances(self, request, obj=None):
        """
        Overwrites BaseModelAdmin fieldsets to add fieldsets passed by the
        tabs.
        If the tabs attribute is not set, use the default ModelAdmin method.
        """
        if self.tabs is not None:
            self.inlines = ()
        tabs_inlines = self.get_formatted_tabs(request, obj)['inlines']
        self.inlines = self.add_tabbed_item(tabs_inlines, self.inlines)

        try:
            # django >=1.7
            return super(TabbedModelAdmin, self)\
                .get_inline_instances(request, obj)
        except TypeError:
            return super(TabbedModelAdmin, self).get_inline_instances(request)

    def add_tabbed_item(self, items_to_add, collection):
        """
        Adds tabbed items (inlines or fieldsets) to their corresponding
        attribute.
        """
        if items_to_add:
            for item in items_to_add:
                if item not in collection:
                    if type(collection) == tuple:
                        collection = collection + (item, )
                    elif type(collection) == list:
                        collection.append(item)
        return collection

    def get_tabs(self, request, obj=None):
        """
        Returns the tabs attribute.
        """
        return self.tabs

    def get_formatted_tabs(self, request, obj=None):
        """
        Returns the formated tabs attribute.
        """
        if self.tabs:
            self.parse_fieldsets_inlines_from_tabs(request, obj)
        return self.formatted_tabs

    def parse_fieldsets_inlines_from_tabs(self, request, obj=None):
        """
        Parses the self.tabs attribute. Checks its integrity and populates
        self._tabs_fieldsets and self._tabs_inlines attributes.
        """
        tabs_fieldsets = ()
        tabs_inlines = ()
        self.formatted_tabs['fields'] = []
        for tab in self.get_tabs(request, obj):
            # Checks that each tab if formated with 2 arguments, verbose name
            # of the tab and the tab configuration.
            if type(tab) not in [tuple, list]:
                raise TypeError(_(u'Each tab entry must be either a list or a tuple'))
            if len(tab) != 2:
                raise ValueError(_(u'Each tabs entry must contain 2 arguments: a verbose name and the tab setup.'))
            if type(tab[1]) not in [tuple, list]:
                raise TypeError(_(u'A tab definition must be either a list or a tuple'))
            # So far all went well, lets parse the tab configuration, we go
            # through each item. If its a tuple or a list we consider its a
            # fieldset, otherwise its a tuple.
            formatted_tab = {'name': tab[0], 'entries': []}
            for tab_entry in tab[1]:
                formatted_tab_entry = {}
                if type(tab_entry) in [tuple, list]:
                    tabs_fieldsets = tabs_fieldsets + (tab_entry, )
                    formatted_tab_entry = {'type': 'fieldset',
                                           'name': tab_entry[0],
                                           'config': tab_entry[1]}
                else:
                    tabs_inlines = tabs_inlines + (tab_entry, )
                    formatted_tab_entry = {'type': 'inline',
                                           'name': tab_entry.__name__}
                formatted_tab['entries'].append(formatted_tab_entry)
            self.formatted_tabs['fields'].append(formatted_tab)
        self.formatted_tabs['fieldsets'] = tabs_fieldsets
        self.formatted_tabs['inlines'] = tabs_inlines

    def add_view(self, request, form_url='', extra_context=None):
        """
        Overwrites add_view to insert the tabs config for the template.
        """
        if extra_context is None:
            extra_context = {}
        extra_context.update({'tabs': self.get_formatted_tabs(request)})
        return super(TabbedModelAdmin, self)\
            .add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Overwrites change_view to insert the tabs config for the template.
        """
        try:
            # django 1.4
            change_view = super(TabbedModelAdmin, self)\
                .change_view(request, object_id, form_url=form_url,
                             extra_context=extra_context)
        except TypeError:
            # django 1.3
            change_view = super(TabbedModelAdmin, self)\
                .change_view(request, object_id, extra_context=extra_context)
        if hasattr(change_view, 'context_data'):
            change_view.context_data.update(
                {'tabs': self.get_formatted_tabs(request,
                 change_view.context_data.get('original'))}
            )
        return change_view

    class Media:
        """
        Extends media class to add custom jquery ui if
        TABBED_ADMIN_USE_JQUERY_UI is set to True.
        """
        if USE_JQUERY_UI:
            css = {'all': (JQUERY_UI_CSS, 'tabbed_admin/css/tabbed_admin.css', )}
            js = (JQUERY_UI_JS,)


