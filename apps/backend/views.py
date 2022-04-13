from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from core.email import UserRegisterEmail, VerificationEmail
from core.tokens import account_activation_token
from django.utils.translation import ugettext as _
from dynamic_preferences.registries import global_preferences_registry
from core.decorators import check_recaptcha


global_preferences = global_preferences_registry.manager()

@check_recaptcha
def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid() and request.recaptcha_is_valid:
            user = form.save()
            context = {
                'request':request
            }
            if global_preferences['app__verification_email']:
                VerificationEmail(context, user).send()
                messages.success(request, _('verification email has been sent'))
            else:
                user.is_active = True
                user.save()
                UserRegisterEmail(context, user).send()
                login(request, user)
                messages.success(request, _('registration successful'))
            return redirect("frontend:home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    context = {
        "register_form":form,
        'site_key': settings.RECAPTCHA_PUBLIC_KEY if settings.RECAPTCHA_PUBLIC_KEY else None
    }
    return render (request, 'registration/registration_user.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, _('Thank you for your email confirmation'))
        login(request, user)
        return redirect('frontend:home')
    else:
        messages.error(request, _('Activation link is invalid!'))
        return redirect('frontend:home')



def my_custom_page_not_found_view(request, exception):
    return render (request, '404.html', {})

def custom_error_view(request, exception=None):
    return render(request, "errors/500.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "errors/403.html", {})

def custom_bad_request_view(request, exception=None):
    return render(request, "errors/400.html", {})
