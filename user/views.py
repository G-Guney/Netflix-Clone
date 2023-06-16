from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import *
# Create your views here.

def userRegister(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        resim = request.FILES['resim']
        telefon = request.POST['telefon']
        sifre = request.POST['sifre']
        sifre2 = request.POST['sifre2']

        if sifre == sifre2:
            if User.objects.filter(username = username).exists():
                messages.error(request, 'Kullanıcı adı daha önce alınmış!')
            elif User.objects.filter(email = email).exists():
                messages.error(request, 'Email kullanımda')
            elif len(sifre) < 6:
                messages.error(request, 'Şifre en az 6 karakter olmalı!')
            elif username.lower() in sifre.lower():
                messages.error(request, 'Kullanıcı adı ile şifre benzer olmamalıdır!')
            else:
                user = User.objects.create_user(
                    username = username,
                    email = email,
                    password = sifre,
                )
                Hesap.objects.create(
                    user = user,
                    resim = resim,
                    telefon = telefon,
                )
                user.save()
                messages.success(request, 'Kayıt işlemi tamamlandı.')
                return redirect('index')
        else:
            messages.error(request, 'Şifreler uyuşmuyor!')
    return render(request, 'register.html')

def userLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        sifre = request.POST['sifre']

        user = authenticate(request, username = username, password = sifre)

        if user is not None:
            login(request, user)
            messages.success(request, 'Giriş işlemi tamamlandı.')
            return redirect('profiles')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı!')
            return render('login')
    return render(request, 'login.html')

@login_required(login_url='login')
def profiles(request):
    profiller = Profile.objects.filter(user = request.user)
    context = {
        'profiller' : profiller
    }
    return render(request, 'browse.html', context)

# bu sayfaya ulaşabilmesi için kullanıcın girişli olmasını sağlayan özellik
@login_required(login_url='login')
def create_profile(request):
    form = ProfileForm
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            if Profile.objects.filter(user = request.user).count() < 4:
                newProfile = form.save(commit=False)
                newProfile.user = request.user
                newProfile.save()
                messages.success(request, 'Profil oluşturuldu')
                return redirect('profiles')
            else:
                messages.warning(request, 'En fazla 4 adet profil oluşturabilirsiniz')
                return redirect('profiles')
    context = {
        'form': form
    }
    return render(request, 'create-profile.html', context)

def hesap(request):
    profil = request.user.hesap
    context = {
        'profil' : profil
    }
    return render(request, 'hesap.html', context)

def changePassword(request):
    if request.method == 'POST':
        eski = request.POST['eski']
        yeni = request.POST['yeni']
        yeni2 = request.POST['yeni2']

        user = authenticate(request, username = request.user, password = eski)

        if user is not None:
            if yeni == yeni2:
                user.set_password(yeni)
                user.save()
                messages.success(request, 'Şifreniz değiştirildi')
                return redirect('login')
            else:
                messages.warning(request, 'Şifreler uyuşmuyor')
        else:
            messages.error(request, 'mevcut Şifreniz hatalı')
    return render(request, 'change-password.html')