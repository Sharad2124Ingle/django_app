from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login_page'),
    path('add_record/', views.add_record, name='add_record'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('log_out/', views.logout_user, name='logout_user'),
]