from django.urls import path
from . import views

urlpatterns = [
    path('', views.wheel_timer, name='wheel_timer'),
]