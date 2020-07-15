from django.urls import path
from . import views
from django.views.generic.base import RedirectView
from dotenv import load_dotenv
import os

try:
    dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
    load_dotenv(dotenv_path)
except:
    pass

client_id = os.getenv('CLIENT_ID')

urlpatterns = [
    #MAIN
    path('login/', views.login, name='login-polpos'),
    path('login-verification/', views.login_verification, name='login-verification-polpos'),
    path('login-gmail/', RedirectView.as_view(permanent=False,url="https://accounts.google.com/o/oauth2/auth?redirect_uri=http://localhost:8000/polpos/login-verification&response_type=code&client_id="+client_id+"&scope=https://www.googleapis.com/auth/userinfo.email"), name='login-gmail-polpos'),
    path('dashboard/', views.dashboard, name='dashboard-polpos'),
    path('logout', views.logout, name='logout-polpos'),
    
    #BAAK
    path('baak-penjadwalan/', views.baak_penjadwalan, name='baak-penjadwalan'),
    path('baak-penjadwalan/tambah', views.tambah_baak_penjadwalan, name='tambah-baak-penjadwalan'),
    
    #PRODI
    path('prodi-penjadwalan/', views.prodi_penjadwalan, name='prodi-penjadwalan'),
    path('prodi-penjadwalan/tambah', views.tambah_prodi_penjadwalan, name='tambah-prodi-penjadwalan'),
    
    #RANDOM
    # path('get-list-dosen/', views.get_list_dosen, name='get-list-dosen'),
    path('approval-bkd/', views.approval_bkd, name='approval-bkd-polpos'),
    
]