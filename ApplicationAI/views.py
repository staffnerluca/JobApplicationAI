from django.shortcuts import render, redirect
import os
import json
from django.http import FileResponse, HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
import openai
import subprocess
from django.views.decorators.csrf import csrf_exempt


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
    createCV(request)
    fileName = "EngelUndTeufel.pdf"
    dName = "CV.pdf"
    filePath = os.path.join(settings.BASE_DIR, "ApplicationAI/output", fileName)
    file = open(filePath, 'rb')
    response = FileResponse(file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename='+dName
    return response


def createPromptCV(data):
    prompt = "Write a short and beautiful CV in LaTex. "
    prompt += "The name of the applicant is "+data.GET["name"]+"; "
    prompt += "He/she is applying to a position as "+data.GET["position"]+" "
    prompt += "at the company "+data.GET["companyName"]+"; "
    prompt += "that works in the "+data.GET["sector"]+" sector; "
    prompt += "He/she is currently working at "+data.GET["companyNow"]+" "
    prompt += "as a "+data.GET["position"]+"; "
    prompt += "Education: "+data.GET["education"]+"; "
    prompt += "Skills: "+data.GET["skills"]+"; "
    prompt += "Work Experience: "+data.GET["experience"]+"; "
    prompt += "Achievements: "+data.GET["achievements"]+"; "
    prompt += "Side Projects: "+data.GET["sideProjects"]+"; "
    return prompt


def creastePromptCL(request):
    pass


def createPromptML(request):
    pass


def getOutputFromChatGPT(prompt, numTokens):
    response = ""
    return response


def compileToPDF():
    try:
        if not os.path.exists("ApplicationAI/output"):
            os.makedirs("ApplicationAI/output")
        pro = subprocess.Popen(["pdflatex", "-output-directory", "ApplicationAI/output", "ApplicationAI/output/EngelUndTeufel.tex"])
        pro.communicate()
        return True
    except subprocess.CalledProcessError as e:
        print("Error: "+e)
        return False


def createNameForPDF():
    pass


def createCV(request, ty):
    match ty:
        case "CV":
            prompt = createPromptCV(request)
        case "CL":
            prompt = createPromptCL(request)
        case "ML":
            prompt = createPromptML(request)
    print(prompt)
    getOutputFromChatGPT(prompt, 1000)
    compileToPDF()


def getData(request):
    createCV(request)
    return(HttpResponse("Hello from get Data"))


def submitPressed():
    pass
