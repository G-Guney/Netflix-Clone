from django.shortcuts import render, redirect
from .models import * 
from user.models import *

# Create your views here.

def index(request):
    return render(request, 'index.html')

def movies(request, profilId, slug):
    profil = Profile.objects.get(id = profilId, slug = slug)
    profiller = Profile.objects.filter(user = request.user)
    populer = Movie.objects.filter(kategori__isim = 'Popüler')
    gundem = Movie.objects.filter(kategori__isim = 'Gündemdekiler')
    context = {
        'populer' : populer,
        'gundem' : gundem,
        'profil' : profil,
        'profiller' : profiller,
    }
    return render(request, 'browse-index.html', context)

def view_404(request, exception):
    return redirect('/')

def view_500(request):
    return render(request, 'hata.html')