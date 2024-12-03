from django.urls import path

from . import views

app_name = 'tetris'

urlpatterns = [
    path("", views.index, name='index'),
    path("action", views.action, name='action'),
]