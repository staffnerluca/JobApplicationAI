from django.shortcuts import render, redirect
import os
from django.http import FileResponse, HttpResponse
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm


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


def login(request):
    return HttpResponse("Hello World")


def download(request):
    file_name = "dieKatastrophe.pdf"
    file_path = os.path.join(settings.BASE_DIR, "ApplicationAI/output", file_name)
    file = open(file_path, 'rb')
    response = FileResponse(file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=JobApplication'
    return response
