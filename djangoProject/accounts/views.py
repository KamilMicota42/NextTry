from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from djangoProject.forms import RegisterUserForm
from store.models import Customer

from django.core.mail import send_mail
from django.conf import settings


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is None:
            context = {"error": "Invalid username or password"}
            return render(request, "accounts/login.html", context)
        login(request, user)
        return redirect('/')
    return render(request, "accounts/login.html", {})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/login/")
    return render(request, "accounts/logout.html", {})


def register_view(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)

            name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            customer = Customer(name=name, email=email)

            customer.user = user
            customer.save()

            subject = 'Welcome to NexTry.'
            message = 'We are so happy to have you with us.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail(subject, message, email_from, recipient_list)

            login(request, user)
            return redirect('/')
    else:
        form = RegisterUserForm()

    return render(request, 'accounts/register.html', {'form': form, })
