from .views import *
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('movies/<profilId>/<slug>', movies, name='movies'),
]