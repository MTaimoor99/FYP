from django.urls import path
from . import views

urlpatterns=[
    path('user_interface/',views.user_interface,name='user_interface'),
    path('register',views.register,name='register'),
    path('',views.login_user,name='login'),
    path('history',views.user_history,name='history'),
    path('about_us',views.about_us,name='about_us'),
    path('contact_us',views.contact_us,name='contact_us')
]