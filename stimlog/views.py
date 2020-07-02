from django.shortcuts import render

def login(request):
    return render(request, 'auth-stimlog/login.html', {})

def dashboard(request):
    return render(request, 'master-stimlog/dashboard.html', {})
