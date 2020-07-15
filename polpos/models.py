from django.conf import settings
from django.db import models
from django.utils import timezone

class PenjadwalanBAAK(models.Model):
    tahun_id = models.CharField(max_length=7, primary_key=True)
    status = models.CharField(max_length=15)    
    tanggal_dibuat = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.tahun_id

class PenjadwalanProdi(models.Model):    
    kode_matkul = models.CharField(max_length=10)
    matkul = models.CharField(max_length=255)
    kode_prodi = models.CharField(max_length=5)
    total_jam = models.CharField(max_length=5)
    kelas = models.CharField(max_length=5)
    kode_dosen = models.CharField(max_length=10)
    nama_dosen = models.CharField(max_length=255)
    tipe_hari = models.CharField(max_length=255, blank=True, null=True)
    tipe_ruangan = models.CharField(max_length=5)    
    tahun_id = models.ForeignKey(PenjadwalanBAAK, on_delete=models.CASCADE, null=True)
    tanggal_dibuat = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.kode_matkul+" - "+self.kode_prodi+" - "+self.kelas

