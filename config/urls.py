from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/favicon/favicon.ico', permanent=False)),
    path('', include('apps.home.urls')),
]
