from django import forms
from .models import PesanMasuk

class PesanMasukForm(forms.ModelForm):
    class Meta:
        model = PesanMasuk
        fields = ['nama', 'email', 'subjek', 'pesan']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Anda'}),
            'subjek': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subjek Pesan'}),
            'pesan': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tuliskan pesan Anda'}),
        }
