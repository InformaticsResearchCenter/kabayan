from django.shortcuts import render, redirect
import urllib.request, urllib.parse
import json
from django.http import HttpResponse
import os
from dotenv import load_dotenv
from django.db import connections
from django.db import transaction
from .models import PenjadwalanProdi, PenjadwalanBAAK
from django.http import JsonResponse
from functools import wraps
 
try:
    dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
    load_dotenv(dotenv_path)
except:
    pass

## Query Function ##
def query_get_all(db_name, query):
    cursor = connections[db_name].cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    transaction.commit(using=db_name)
    return rows

def query_get(db_name, query):
    cursor = connections[db_name].cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    transaction.commit(using=db_name)
    return row


## View Function ##
def login(request):
    if request.session.has_key('id_user'):
        return redirect('dashboard-polpos')
    else:
        return render(request, 'auth-polpos/login.html', {})

def login_verification(request):
    if request.method =="GET":
        google_code = request.GET['code']
        client_id = os.getenv('CLIENT_ID')
        redirect_uri = os.getenv('REDIRECT_URI')
        grant_type='authorization_code'
        client_secret=os.getenv('CLIENT_SECRET')
        
        post_data = [('code',google_code),('client_id',client_id),('redirect_uri',redirect_uri),('grant_type',grant_type),('client_secret',client_secret)]
        
        result = urllib.request.urlopen('https://accounts.google.com/o/oauth2/token', urllib.parse.urlencode(post_data).encode("utf-8"))
        content = result.read()
        dct = json.loads(content)
        access_token = dct['access_token']
        headers = { 'Authorization':'OAuth %s'% access_token }
        req = urllib.request.Request('https://www.googleapis.com/oauth2/v3/userinfo ',  headers=headers)
        
        result2 = urllib.request.urlopen(req)
        content2 = result2.read()
        dct2 = json.loads(content2)
        
        # data_dict = dict()
        # data_dict['email'] = dct2['email']
        # data_dict['email_verified']=dct2['email_verified'] #True
        
        # email = "akademik@poltekpos.ac.id"
        email = "d4ti@poltekpos.ac.id"
        # email = "bak@polpos.ac.id"
        
        query = """
            SELECT case
            when user_email IS NULL or user_email = '' then Email
            when Email IS NULL or Email = '' then user_email 
            end AS Email, Login, LevelID, ProdiID        
            FROM simak_mst_karyawan smk
            LEFT JOIN simak_besan_users sbu
            ON sbu.user_name=smk.Login
            where sbu.user_email="{}" or smk.Email="{}";
        """.format(email, email)
        row = query_get('simpati', query)
        
        
        if row and dct2['email_verified'] == True:
            request.session['id_user'] = row[1]
            request.session['role_user'] = str(row[2]).replace(".","").replace("100","").replace("101","")
            request.session['prodi_user'] = row[3]
            return redirect("dashboard-polpos")
            # return HttpResponse("{}, {}, {}".format(row[0], row[1], row[2]))
        else:
            return HttpResponse("Belum terdaftar")
    
        
        # if dct2['email'] == "" and dct2['email_verified'] == True:
        #     request.session['id_user'] = ""
        #     return redirect("profile")
        # else:
        #     return render(request, 'auth-polpos/login.html', {})

def dashboard(request):
    if request.session.has_key('id_user') and request.session.has_key('role_user'):
        id_user = request.session['id_user']
        role_user = request.session['role_user']
        if role_user == "245":
            return render(request, 'baak-polpos/dashboard.html', {})        
        elif role_user == "241":
            return render(request, 'prodi-polpos/dashboard.html', {})
        else:
            return render(request, 'master-polpos/dashboard.html', {})
    else:
        return redirect('login-polpos')
    
def logout(request):
    try:
        del request.session['id_user']
        del request.session['role_user']
        del request.session['prodi_user']
    except:
        pass
    return redirect('login-polpos')

def check_role(request, role, url, context):
    if request.session.has_key('id_user') and request.session.has_key('role_user'):
        role_user = request.session['role_user']
        if role_user == role:
            return render(request, url, context)
        else:
            return HttpResponse('<script>history.back();</script>')
    else:
        return redirect('login-polpos')

def check_role_post(role):
    def decorator(function):
        @wraps(function)
        def wrap(request, *args, **kwargs):
            if request.session.has_key('id_user') and request.session.has_key('role_user'):
                role_user = request.session['role_user']
                if role_user == role:
                    return function(request, *args, **kwargs)
                else:
                    return HttpResponse('<script>history.back();</script>')
            else:
                return redirect('login-polpos')
        return wrap
    return decorator

# def check_role_post(func):
#     if request.session.has_key('id_user') and request.session.has_key('role_user'):
#         role_user = request.session['role_user']
#         if role_user == role:
#             func()
#         else:
#             return HttpResponse('<script>history.back();</script>')
#     else:
#         return redirect('login-polpos')

def baak_penjadwalan(request):
    tahuns = PenjadwalanBAAK.objects.all()
    if request.method == "POST":
        tahun_id = request.POST['tahun_id']
        jadwals = PenjadwalanProdi.objects.filter(tahun_id_id=tahun_id)
        context = {
            'tahuns': tahuns,
            'jadwals': jadwals,
            'selected': PenjadwalanBAAK.objects.filter(tahun_id=tahun_id)
        }
        print(context)
    else:
        context = {
            'tahuns': tahuns,
            'jadwals': '',        
            'selected':''
        }
        print(context)
    return check_role(request, "245", 'baak-polpos/penjadwalan.html', context)

@check_role_post("245")
def tambah_baak_penjadwalan(request):
    if request.method == "POST":
        pb = PenjadwalanBAAK()
        pb.tahun_id = '20201'
        pb.status = 'Asiap'
        pb.save()
        return redirect('baak-penjadwalan')

def prodi_penjadwalan(request):
    jadwals = PenjadwalanProdi.objects.filter(kode_prodi="14")
    context = {
        'jadwals': jadwals
    }
    return check_role(request, "241", 'prodi-polpos/penjadwalan.html', context)

def tambah_prodi_penjadwalan(request):
    if request.method == "POST":
        obj = PenjadwalanProdi.objects.create(
            matkul=request.POST['matakuliah'],
            kode_prodi="14",
            total_jam=request.POST['total_jam'],
            kelas=request.POST['kelas'],
            nama_dosen=request.POST['dosen'],
            tipe_hari=';'.join(filter(None,request.POST.getlist('tipe_hari'))),
            tipe_ruangan=request.POST['tipe_ruangan']
            )
        obj.save()
        return redirect('tambah-prodi-penjadwalan')
    else:
        prodi = "14"
        query_matkul = """
                SELECT Nama FROM simpati.simak_mst_matakuliah WHERE ProdiID="{}" and KurikulumID = (SELECT KurikulumID FROM simak_mst_matakuliah WHERE ProdiID="{}" group by MKID DESC limit 1)
                """.format(prodi, prodi)
        rows_matkul = query_get_all('simpati', query_matkul)
        
        query_dosen = """
                SELECT Nama FROM simpati.simak_mst_dosen WHERE Homebase="{}";
                """.format(prodi)
        rows_dosen = query_get_all('simpati', query_dosen)
        
        rows_kelas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', "J"]
        context = {
            'matkuls': rows_matkul,
            'dosens' : rows_dosen,
            'kelass'  : rows_kelas,
        }
        return check_role(request, "241", 'prodi-polpos/tambah.html', context)

# def get_list_dosen(request):
#     if request.method == "GET" and request.is_ajax():
#         prodi = request.GET.get("prodi")
        
#         try:
#             query = """
#                 SELECT Nama FROM simpati.simak_mst_matakuliah WHERE ProdiID="{}" and KurikulumID = (SELECT KurikulumID FROM simak_mst_matakuliah WHERE ProdiID="{}" group by MKID DESC limit 1)
#                 """.format(prodi, prodi)
#             rows = query_get_all('simpati', query)
#         except:
#             return JsonResponse({"success":False}, status=400)
#         return JsonResponse({"data":rows}, status=200)
#     return JsonResponse({"success":False}, status=400)

def approval_bkd(request):
    return render(request, 'approval-polpos/bkd.html', {})