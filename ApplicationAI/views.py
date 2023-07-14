from django.shortcuts import render, redirect
import os
from django.http import FileResponse, HttpResponse
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, "index.html")


def app(request):
    return render(request, "app.html")


def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("app")
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('app')
        else:
            #TODO need to include error message
            error_message = "Invalid username or password"
            return render(request, 'index.html', {'error_message': error_message})
    else:
        return render(request, 'index.html')


def download(request):
    file_name = "dieKatastrophe.pdf"
    file_path = os.path.join(settings.BASE_DIR, "ApplicationAI/output", file_name)
    file = open(file_path, 'rb')
    response = FileResponse(file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=JobApplication'
    return response
