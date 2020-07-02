from django.shortcuts import render
import urllib.request, urllib.parse
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

def login(request):
    return render(request, 'auth-polpos/login.html', {})

@csrf_protect
def login_verification(request):
    if request.method =="GET":
        gcode = request.GET['code']
        client_id='519477122351-i4onlc5rlr6kgn1li9211cb2aoamun61.apps.googleusercontent.com'
        redirect_uri='http://localhost:8000/polpos/login-verification'
        grant_type='authorization_code'
        client_secret='bVDO32A8QazGM2GVScRpQwjb'
        post_data = [('code',gcode),('client_id',client_id),('redirect_uri',redirect_uri),('grant_type',grant_type),('client_secret',client_secret)]     # a sequence of two element tuples
        result = urllib.request.urlopen('https://accounts.google.com/o/oauth2/token', urllib.parse.urlencode(post_data).encode("utf-8"))
        content = result.read()
        dct = json.loads(content)
        access_token = dct['access_token']
        headers = { 'Authorization':'OAuth %s'% access_token }
        req = urllib.request.Request('https://www.googleapis.com/plus/v1/people/me',  headers=headers)
        result2 = urllib.request.urlopen(req)
        content = result2.read()
        dct = json.loads(content)
        person_dict = dict()
        person_dict['id'] = dct['id']
        person_dict['personname']=dct['displayName']
        
        return HttpResponse("j")
          

def dashboard(request):
    return render(request, 'master-polpos/dashboard.html', {})