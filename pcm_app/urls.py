from django.urls import path
from . import views

app_name = 'pcm_app'

urlpatterns = [
    path('', views.beranda, name='beranda'),
    path('profil/', views.profil, name='profil'),
    path('pimpinan/', views.pimpinan, name='pimpinan'),
    path('ranting/', views.ranting, name='ranting'),
    path('amal-usaha/', views.amal_usaha, name='amal_usaha'),
    path('berita/', views.berita_list, name='berita_list'),
    path('berita/<slug:slug>/', views.berita_detail, name='berita_detail'),
    path('agenda/', views.agenda, name='agenda'),
    path('unduhan/', views.unduhan, name='unduhan'),
    path('kontak/', views.kontak, name='kontak'),
]
