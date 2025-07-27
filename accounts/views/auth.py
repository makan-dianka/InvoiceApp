from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm #UserCreationForm
from  accounts.forms.userform import CreateUserForm
from django.contrib import messages
from django.conf import settings
from utils.payment import sendmail, log




def register_view(request):
    if request.user.is_authenticated:
        return redirect("factures:dashboard")

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            log('debug_log', 'info', f'new user is created : {request.user}')
            # sendmail
            # maildata = {
            # 'usermail': settings.EMAIL_RECIPIENT,
            # 'mailsubject' : f"[OkFacture] Un nouveau utilisateur vient de s'inscrire",
            # 'html_file': 'register.html',
            # 'txt_file': 'register.txt',
            # }
            # sendmail(request, **maildata)

            return redirect('accounts:company_creation')  # à adapter plus tard
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