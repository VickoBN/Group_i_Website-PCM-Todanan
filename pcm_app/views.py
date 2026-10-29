from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import Http404
from django.utils import timezone
from .models import ProfilOrganisasi, Pimpinan, Ranting, AmalUsaha, Berita, Agenda, Dokumen
from .forms import PesanMasukForm

def beranda(request):
    context = {
        'profil': ProfilOrganisasi.objects.first(),
        'jumlah_ranting': Ranting.objects.count(),
        'jumlah_aum': AmalUsaha.objects.count(),
        'berita_terbaru': Berita.published.all()[:3],
        'agenda_terbaru': Agenda.objects.filter(waktu_mulai__gte=timezone.now())[:3],
    }
    return render(request, 'pcm_app/beranda.html', context)

def profil(request):
    profil_obj = ProfilOrganisasi.objects.first()
    misi_list = profil_obj.misi.splitlines() if profil_obj and profil_obj.misi else []
    return render(request, 'pcm_app/profil.html', {'profil': profil_obj, 'misi_list': misi_list})

def pimpinan(request):
    daftar_pimpinan = Pimpinan.objects.all().order_by('urutan')
    return render(request, 'pcm_app/pimpinan.html', {'daftar_pimpinan': daftar_pimpinan})

def ranting(request):
    daftar_ranting = Ranting.objects.all()
    return render(request, 'pcm_app/ranting.html', {'daftar_ranting': daftar_ranting})

def amal_usaha(request):
    aum_list = AmalUsaha.objects.all()
    aum_by_bidang = {
        'Pendidikan': aum_list.filter(bidang='pendidikan'),
        'Kesehatan': aum_list.filter(bidang='kesehatan'),
        'Sosial': aum_list.filter(bidang='sosial'),
        'Ekonomi': aum_list.filter(bidang='ekonomi'),
    }
    return render(request, 'pcm_app/amal_usaha.html', {'aum_by_bidang': aum_by_bidang})

def berita_list(request):
    berita_qs = Berita.published.all()
    paginator = Paginator(berita_qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pcm_app/berita_list.html', {'page_obj': page_obj})

def berita_detail(request, slug):
    berita = get_object_or_404(Berita, slug=slug)
    if berita.status != 'terbit' or berita.tanggal_terbit > timezone.now():
        raise Http404("Berita tidak ditemukan.")
    berita_lain = Berita.published.exclude(id=berita.id)[:3]
    return render(request, 'pcm_app/berita_detail.html', {'berita': berita, 'berita_lain': berita_lain})

def agenda(request):
    now = timezone.now()
    agenda_mendaang = Agenda.objects.filter(waktu_mulai__gte=now).order_by('waktu_mulai')
    agenda_lampau = Agenda.objects.filter(waktu_mulai__lt=now).order_by('-waktu_mulai')
    return render(request, 'pcm_app/agenda.html', {
        'agenda_mendatang': agenda_mendaang,
        'agenda_lampau': agenda_lampau
    })

def unduhan(request):
    daftar_dokumen = Dokumen.objects.all().order_by('-tanggal_unggah')
    return render(request, 'pcm_app/unduhan.html', {'daftar_dokumen': daftar_dokumen})

def kontak(request):
    if request.method == 'POST':
        form = PesanMasukForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pesan Anda berhasil terkirim!")
            return redirect('pcm_app:kontak')
    else:
        form = PesanMasukForm()
    return render(request, 'pcm_app/kontak.html', {'form': form})
