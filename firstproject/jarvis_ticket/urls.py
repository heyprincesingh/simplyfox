from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('createtoken', views.create_token, name='createToken')
]