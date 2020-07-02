from django.shortcuts import render

def login(request):
    return render(request, 'auth-ypbpi/login.html', {})

def dashboard(request):
    return render(request, 'master-ypbpi/dashboard.html', {})