from django.urls import path
from . import views
urlpatterns = [
    path('', views.Login, name='login'),
    path('input', views.Input, name='input'),
    path('confirm', views.Confirm, name='confirm'),
    path('register', views.Register, name='register'),
    path('detail', views.Detail, name='detail'),
    path('jaspay', views.Jaspay, name='jaspay'),
    path('logout', views.Logout, name='logout'),
]
