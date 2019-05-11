
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