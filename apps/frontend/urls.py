from django.urls import path
from apps.backend.views import activate
from . import views

app_name = "frontend"

urlpatterns = [
    path('', views.home, name='home'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
]
