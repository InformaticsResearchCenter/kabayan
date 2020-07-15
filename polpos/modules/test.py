import sqlite3
import os
import pymysql
from dotenv import load_dotenv
 
try:
    dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
    load_dotenv(dotenv_path)
except:
    pass

def connDBSQLite():
    try:
        db_path = os.path.join(os.path.dirname(__file__), '../../db.sqlite3')
        conn = sqlite3.connect(db_path)   
        # query = "SELECT kode_prodi, matkul, total_jam, kelas, nama_dosen, tipe_hari, tipe_ruangan FROM polpos_penjadwalanprodi"
        # cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        # for x in cursor:
        #     print(x)
        
        print("Berhasil SQLite")
    except Exception as e:
        print(e)

def connDBSiap():
    try:
        conn = pymysql.connect(
        db=os.getenv('NAME_DB1'), 
        user=os.getenv('USER_DB1'), 
        passwd=os.getenv('PASS_DB1'), 
        host=os.getenv('HOST_DB1'), 
        port=int(os.getenv('PORT_DB1')))
        conn.close()
        print("Berhasil MySQL")
    except Exception as e:
        print(e)
        
# connDBSQLite()
# connDBSiap()

import subprocess


process = subprocess.Popen(["python", os.path.join(os.path.dirname(__file__), "penjadwalan.py"), "20192;divakrishna55@gmail.com"])
process.wait()
process.kill()

# process.kill()
# print(os.path.join(os.path.dirname(__file__), '../../.env'))
# print(os.path.dirname(__file__))

# import os
# import signal
# pro = subprocess.Popen(["python", os.path.join(os.path.dirname(__file__), "penjadwalan.py"),"20192"], 
#                        stdout=subprocess.PIPE, 
#                        shell=True, 
#                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP) 

# os.killpg(os.getpgid(pro.pid), signal.SIGTERM)