from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext as _

from core.decorators import check_recaptcha
from dynamic_preferences.registries import global_preferences_registry
from core.decorators import check_recaptcha
from meta.views import Meta

global_preferences = global_preferences_registry.manager()

from .forms import ContactForm

@check_recaptcha
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = _('subject')
            body = {
                'name': form.cleaned_data['name'],
                'telephone': form.cleaned_data['telephone'],
                'email': form.cleaned_data['email'],
                'text':form.cleaned_data['text'],
            }
            message = "\n".join(body.values())
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, settings.ADMINS)
                form.save()
                messages.success(request, _('your enquiry has been sent, you will receive a reply soon'))
            except BadHeaderError:
                messages.error(request, _('your enquiry has not been sent. please try again later.'))
                return redirect ("contact:home")
            return redirect ("frontend:home")
    meta = Meta(
        title=_('Contact Page'),
        description='{}, tel:{}, email:{}'.format(
            global_preferences['contact__address'],
            global_preferences['contact__telephone'],
            global_preferences['contact__email'],
        ),
    )
    form = ContactForm()

    context ={
        'form': form,
        'meta': meta,
        'site_key': settings.RECAPTCHA_PUBLIC_KEY if settings.RECAPTCHA_PUBLIC_KEY else None
    }

    template = "contact.html"

    return render(request, template, context)
