from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm #UserCreationForm
from  ..forms.userform import CreateUserForm
from django.contrib import messages
# from models import EmailBackend




def register_view(request):
    if request.user.is_authenticated:
        return redirect("factures:dashboard")

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('factures:dashboard')  # à adapter plus tard
    else:
        form = CreateUserForm()
    return render(request, 'accounts/register.html', {'form': form})



def login_view(request):
    if request.user.is_authenticated:
        return redirect("factures:dashboard")

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('factures:dashboard') # -> redirection du dashboard de  user
        else:
            messages.info(request, 'Votre nom ou mot de passe est incorrect')
    return render(request, 'accounts/login.html')



def logout_view(request):
    logout(request)
    return redirect('accounts:login')