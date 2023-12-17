from django.urls import path
from . import views

urlpatterns=[
    path('user_interface/',views.user_interface,name='user_interface'),
]