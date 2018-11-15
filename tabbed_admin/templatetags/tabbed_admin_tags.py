# -*- coding: utf-8 -*-

from django import template
from django.contrib.admin.helpers import Fieldset
from django.template.loader import render_to_string
from django.core.exceptions import ImproperlyConfigured

register = template.Library()

@register.simple_tag(takes_context=True)
def render_tab_fieldsets_inlines(context, entry):
    """
    Render the fieldsets and inlines for a tab.
    """
    admin_form = context['adminform']
    ### I changed the template variable to refer to our custom defined templates in our TabbedModelAdmin
    template = admin_form.model_admin.template

    if 'request' not in context:
        raise ImproperlyConfigured(
            '"request" missing from context. Add django.core.context'
            '_processors.request to your'
            'TEMPLATE_CONTEXT_PROCESSORS')
    request = context['request']
    obj = context.get('original', None)
    
    inline_matching = {}
    if "inline_admin_formsets" in context:
        inline_matching = dict((inline.opts.__class__.__name__, inline)
                               for inline in context["inline_admin_formsets"])
    
    ### I changed the readonly_fields to reference that modelAdmin forms readonly_field variable directly
    if entry['type'] == 'fieldset':
        name = entry['name']
        f = Fieldset(
            admin_form.form,
            name,
            readonly_fields=admin_form.readonly_fields,
            model_admin=admin_form.model_admin,
            **entry['config']
        )
        context["fieldset"] = f
        return render_to_string(template, context.flatten(), request=request)
    elif entry['type'] == 'inline':
        try:
            inline_admin_formset = inline_matching[entry["name"]]
            context["inline_admin_formset"] = inline_admin_formset
            return render_to_string(inline_admin_formset.opts.template,
                                    context.flatten(), request=request)
        except KeyError:  # The user does not have the permission
            pass
    return ''

### My admin.py django-tabbed-admin example class with working custom templates.

# class MyAdminView(TabbedModelAdmin):

#     # Define your model like in the docs.
#     model = MyModel
 
#     ##Define all your fields/fieldset params like you would normally in admin.ModelAdmin
#     list_select_related = ['your_fields']
#     list_display = ['your_fields']
#     list_display_links = ['your_fields']
#     list_filter = ['your_fields']
#     autocomplete_fields = ['your_fields']
#     search_fields = ['your_fields']
#     readonly_fields = ['your_fields']
#     fieldsets = [
#         ('Model Information',{'fields': [('field_1','field_2','field_3','field_4',)]})
#     ]
#     save_as = True
#     inlines = [MyModelInline]
    
#     ##django-tabbed-admin fieldset stuff##
#     tab_for_model = (
#         MyModelInline,
#     )
#     tabs = [
#         ('Model Information', fieldsets),
#         ('My Inline Model', tab_for_model)
#     ]

#     ### Define custom templates

#     # I copied the change_form and fieldset templates from the following paths
#     # into my custom admin template directoy.

#     # '/lib/python3.5/site-packages/tabbed_admin/templates/tabbed_admin/'
#     change_form_template = 'path_to_your_model_templates/change_form.html'
    
#     # I got a weird Key error in the old fieldset.html template that django.admin uses,
#     # I think it has something to do with the new read_only/has_view permissions within the admin since 2.0

#     # '/lib/python3.5/site-packages/django/contrib/admin/templates/admin/includes/fieldset.html'
#     template = 'path_to_your_model_templates/fieldset.html'

#     # Added customer jquery static references.
#     # Don't forget to add TABBED_ADMIN_USE_JQUERY_IU = True to your settings.py 
#     class Media:
#         js = [
#             'admin/js/recipe_calc.js',
#             'admin/js/list_filter_collaspe.js'
#         ]
#         css = {'all':(
#             'tabbed_admin/css/jquery-ui-1.11.4.min.css',
#             'tabbed_admin/css/tabbed_admin.css'
#             )
#         }