from django.urls import path
from . import views
from django.views.generic.base import RedirectView
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)

client_id = os.getenv('CLIENT_ID')

urlpatterns = [
    path('login/', views.login, name='login-polpos'),
    path('login-verification/', views.login_verification, name='login-verification-polpos'),
    path('login-gmail/', RedirectView.as_view(permanent=False,url="https://accounts.google.com/o/oauth2/auth?redirect_uri=http://localhost:8000/polpos/login-verification&response_type=code&client_id="+client_id+"&scope=https://www.googleapis.com/auth/plus.login"), name='login-gmail-polpos'),
    path('dashboard/', views.dashboard, name='dashboard-polpos')
    
]