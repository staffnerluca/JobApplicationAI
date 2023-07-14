from django.shortcuts import render
import os
from django.http import FileResponse
from django.conf import settings


def index(request):
    return render(request, "index.html")


def download(request):
    file_name = "dieKatastrophe.pdf"
    file_path = os.path.join(settings.BASE_DIR, "ApplicationAI/output", file_name)
    file = open(file_path, 'rb')
    response = FileResponse(file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=JobApplication'
    return response
