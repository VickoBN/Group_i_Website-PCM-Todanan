from django.contrib import admin
from .models import (
    ProfilOrganisasi, Pimpinan, Ranting, AmalUsaha,
    Berita, Agenda, Dokumen, PesanMasuk, TautanTerkait
)

@admin.register(ProfilOrganisasi)
class ProfilOrganisasiAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nama_singkat', 'telepon', 'email')

@admin.register(Pimpinan)
class PimpinanAdmin(admin.ModelAdmin):
    list_display = ('nama', 'jabatan', 'periode', 'urutan')
    list_editable = ('urutan',)

@admin.register(Ranting)
class RantingAdmin(admin.ModelAdmin):
    list_display = ('nama_ranting', 'ketua', 'telepon')
    search_fields = ('nama_ranting', 'ketua')

@admin.register(AmalUsaha)
class AmalUsahaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'bidang', 'alamat')
    list_filter = ('bidang',)
    search_fields = ('nama',)

@admin.register(Berita)
class BeritaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'status', 'tanggal_terbit')
    list_filter = ('status', 'tanggal_terbit')
    search_fields = ('judul', 'isi')
    prepopulated_fields = {'slug': ('judul',)}

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('nama_kegiatan', 'waktu_mulai', 'tempat')
    list_filter = ('waktu_mulai',)
    search_fields = ('nama_kegiatan', 'tempat')

@admin.register(Dokumen)
class DokumenAdmin(admin.ModelAdmin):
    list_display = ('judul', 'tanggal_unggah')
    search_fields = ('judul',)

@admin.register(PesanMasuk)
class PesanMasukAdmin(admin.ModelAdmin):
    list_display = ('nama', 'email', 'subjek', 'waktu_kirim', 'sudah_dibaca')
    list_filter = ('sudah_dibaca', 'waktu_kirim')
    readonly_fields = ('nama', 'email', 'subjek', 'pesan', 'waktu_kirim')

@admin.register(TautanTerkait)
class TautanTerkaitAdmin(admin.ModelAdmin):
    list_display = ('nama', 'url', 'urutan')
    list_editable = ('urutan',)
