from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login, name='login-stimlog'),
    path('dashboard/', views.dashboard, name='dashboard-stimlog')
]