from .models import ProfilOrganisasi, TautanTerkait

def global_pcm_context(request):
    return {
        'profil_global': ProfilOrganisasi.objects.first(),
        'tautan_global': TautanTerkait.objects.all(),
    }
