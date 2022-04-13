
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.test import test
from apps.backend.views import register

handler404 = 'apps.backend.views.my_custom_page_not_found_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('tests/', test, name='tests'),
    path('contact/', include('apps.contact.urls')),
    path('', include('apps.frontend.urls')),

]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [path('rosetta/', include('rosetta.urls'))]

if 'dynamic_preferences' in settings.INSTALLED_APPS:
    urlpatterns += [path('preferences/', include('dynamic_preferences.urls'))]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
