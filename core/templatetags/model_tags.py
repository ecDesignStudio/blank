from django import template
from dynamic_preferences.registries import global_preferences_registry

from django.conf import settings
from apps.contact.forms import ContactForm

register = template.Library()

@register.inclusion_tag('templatetags/contact.html')
def block_contact(show_map=True, show_datas=True, show_form=True):
    global_preferences = global_preferences_registry.manager()

    context = {
        'show_map':show_map,
        'show_datas':show_datas,
        'show_form':show_form,
        'form':ContactForm,
        'address':global_preferences['contact__address'],
        'telephone':global_preferences['contact__telephone'],
        'email':global_preferences['contact__email'],
        'latitude':global_preferences['contact__latitude'],
        'longitude':global_preferences['contact__longitude'],
        'text_map':global_preferences['contact__text_map'],
        'site_key': settings.RECAPTCHA_PUBLIC_KEY if settings.RECAPTCHA_PUBLIC_KEY else None
    }

    return context
