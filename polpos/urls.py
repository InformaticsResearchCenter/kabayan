from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('login/', views.login, name='login-polpos'),
    path('login-verification/', views.login_verification, name='login-verification-polpos'),
    path('login-gmail/', RedirectView.as_view(permanent=False,url="https://accounts.google.com/o/oauth2/auth?redirect_uri=http://localhost:8000/polpos/login-verification&response_type=code&client_id=519477122351-i4onlc5rlr6kgn1li9211cb2aoamun61.apps.googleusercontent.com&scope=https://www.googleapis.com/auth/plus.login"), name='login-gmail-polpos'),
    path('dashboard/', views.dashboard, name='dashboard-polpos')
    
]