from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone

class ProfilOrganisasi(models.Model):
    nama = models.CharField(max_length=255)
    nama_singkat = models.CharField(max_length=50)
    tagline = models.CharField(max_length=255)
    tentang = models.TextField()
    sejarah = models.TextField()
    visi = models.TextField()
    misi = models.TextField(help_text="Tuliskan satu misi per baris")
    alamat_sekretariat = models.TextField()
    telepon = models.CharField(max_length=20)
    email = models.EmailField()
    jumlah_anggota_kta = models.PositiveIntegerField(default=0)
    hero_image = models.ImageField(upload_to='profil/')

    class Meta:
        verbose_name_plural = "Profil Organisasi"

    def clean(self):
        if not self.pk and ProfilOrganisasi.objects.exists():
            raise ValidationError("Profil organisasi hanya boleh diisi satu baris data.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama


class Pimpinan(models.Model):
    nama = models.CharField(max_length=255)
    jabatan = models.CharField(max_length=100)
    periode = models.CharField(max_length=20)
    foto = models.ImageField(upload_to='pimpinan/')
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['urutan']
        verbose_name_plural = "Pimpinan"

    def __str__(self):
        return f"{self.nama} - {self.jabatan}"


class Ranting(models.Model):
    nama_ranting = models.CharField(max_length=255)
    ketua = models.CharField(max_length=255)
    alamat = models.TextField()
    telepon = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Ranting"

    def __str__(self):
        return self.nama_ranting


class AmalUsaha(models.Model):
    BIDANG_CHOICES = [
        ('pendidikan', 'Pendidikan'),
        ('kesehatan', 'Kesehatan'),
        ('sosial', 'Sosial'),
        ('ekonomi', 'Ekonomi'),
    ]
    nama = models.CharField(max_length=255)
    bidang = models.CharField(max_length=20, choices=BIDANG_CHOICES)
    deskripsi = models.TextField()
    alamat = models.TextField()
    gambar = models.ImageField(upload_to='amal_usaha/')

    class Meta:
        verbose_name_plural = "Amal Usaha"

    def __str__(self):
        return f"{self.nama} ({self.get_bidang_display()})"


class PublishedBeritaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            status='terbit',
            tanggal_terbit__lte=timezone.now()
        )


class Berita(models.Model):
    STATUS_CHOICES = [
        ('draf', 'Draf'),
        ('terbit', 'Terbit'),
    ]
    judul = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    ringkasan = models.TextField()
    isi = models.TextField()
    gambar_sampul = models.ImageField(upload_to='berita/')
    tanggal_terbit = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draf')

    objects = models.Manager()
    published = PublishedBeritaManager()

    class Meta:
        ordering = ['-tanggal_terbit']
        verbose_name_plural = "Berita"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.judul)
            slug = base_slug
            count = 1
            while Berita.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul


class Agenda(models.Model):
    nama_kegiatan = models.CharField(max_length=255)
    waktu_mulai = models.DateTimeField()
    tempat = models.CharField(max_length=255)
    keterangan = models.TextField(blank=True)

    class Meta:
        ordering = ['-waktu_mulai']
        verbose_name_plural = "Agenda"

    def __str__(self):
        return self.nama_kegiatan


class Dokumen(models.Model):
    judul = models.CharField(max_length=255)
    keterangan = models.TextField(blank=True)
    berkas = models.FileField(upload_to='dokumen/')
    tanggal_unggah = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Dokumen"

    def __str__(self):
        return self.judul


class PesanMasuk(models.Model):
    nama = models.CharField(max_length=255)
    email = models.EmailField()
    subjek = models.CharField(max_length=255)
    pesan = models.TextField()
    waktu_kirim = models.DateTimeField(auto_now_add=True)
    sudah_dibaca = models.BooleanField(default=False)

    class Meta:
        ordering = ['-waktu_kirim']
        verbose_name_plural = "Pesan Masuk"

    def __str__(self):
        return f"Pesan dari {self.nama} - {self.subjek}"


class TautanTerkait(models.Model):
    nama = models.CharField(max_length=255)
    url = models.URLField()
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['urutan']
        verbose_name_plural = "Tautan Terkait"

    def __str__(self):
        return self.nama
