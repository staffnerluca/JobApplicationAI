from django.shortcuts import render, redirect
from django.http import QueryDict
import os
import zipfile
from django.http import FileResponse, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import authenticate, login
import openai
import subprocess
from django.views.decorators.csrf import csrf_exempt
from .models import Users
from .forms import fRegister
import tempfile
import shutil


# GLOBAL vars
openai.api_key = "YOUR API KEY HERE"


# RETURN PAGES
def index(request):
    return render(request, "index.html")


@login_required
def app(request):
    userData = Users.objects.get(id=request.user.id)
    return render(request, "app.html", {"userData": userData})


# USER
def register(request):
    form = fRegister()
    if request.method == "POST":
        form = fRegister(request.POST)
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
            # TODO need to include error message
            error_message = "Invalid username or password"
            return render(request, 'index.html', {'error_message': error_message})
    else:
        return render(request, 'index.html')


def updateUserNumber(request):
    user = Users.objects.get(id=request.user.id)
    if user.requestNumber is None:
        user.requestNumber = 0
    user.requestNumber += 1
    user.save()


def saveUserDataToDB(request):
    addData = Users.objects.get(id=request.user.id)
    addData.fullName = request.GET.get("name")
    addData.companyNow = request.GET.get("companyNow")
    addData.positionNow = request.GET.get("positionNow")
    addData.education = request.GET.get("education")
    addData.skills = request.GET.get("skills")
    addData.experience = request.GET.get("experience")
    addData.achievements = request.GET.get("achievements")
    addData.sideProjects = request.GET.get("sideProjects")
    addData.save()


# PROMPT GENERATION AND GPT
def createPrompt(data, ty):
    # TODO find better prompt, because the results are not that great some of the time
    prompt = f"Write a short and beautiful {ty} in LaTex. "
    prompt += "The name of the applicant is "+data.GET["name"]+"; "
    prompt += "He/she is applying to a position as "+data.GET["position"]+" "
    prompt += "at the company "+data.GET["companyName"]+"; "
    prompt += "that works in the "+data.GET["sector"]+" sector; "
    prompt += "He/she is currently working at "+data.GET["companyNow"]+" "
    prompt += "as a "+data.GET["positionNow"]+"; "
    prompt += "Education: "+data.GET["education"]+"; "
    prompt += "Skills: "+data.GET["skills"]+"; "
    prompt += "Work Experience: "+data.GET["experience"]+"; "
    prompt += "Achievements: "+data.GET["achievements"]+"; "
    prompt += "Side Projects: "+data.GET["sideProjects"]+"; "
    return prompt


def getOutputFromChatGPT(prompt, numTokens):
    try:
        response = openai.Completion.create(
                engine = "text-davinci-002",
                prompt = prompt,
                max_tokens = numTokens
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print("Error: "+str(e))
        return "Error"


# CREATE PDF
def compileToPDF(file, folder):
    try:
        if not os.path.exists("ApplicationAI/output/"+folder):
            os.makedirs("ApplicationAI/output/"+folder)
        file = file.replace(" ", "")
        pro = subprocess.Popen(["pdflatex", "-output-directory", "ApplicationAI/output/"+folder, "ApplicationAI/output/"+file+".tex"])
        pro.communicate()
        return True
    except subprocess.CalledProcessError as e:
        print("Error: "+str(e))
        return False


def createNameForFolder(request):
    user = request.user
    fName = str(user.fullName).replace(" ", "")
    fName += str(user.requestNumber)
    return fName


def createDoc(request, ty, foName):
    #prompt = createPrompt(request, ty)
    #out = getOutputFromChatGPT(prompt, 3900)
    compileToPDF(ty+".tex", foName)


def removeOldFiles(name):
    pass


def zipFolder(request, foName):
    path = os.path.join(settings.BASE_DIR, "ApplicationAI/output", f"{foName}")
    with zipfile.ZipFile(path+".zip", 'w') as zipf:
        for root, _, files in os.walk(path):
            for file in files:
                filePath = os.path.join(root, file)
                arcname = os.path.relpath(filePath, path)
                zipf.write(filePath, arcname)


# MAIN
def download(request):
    request = createExampleData(request)
    saveUserDataToDB(request)
    updateUserNumber(request)
    foName = createNameForFolder(request)
    tempDir = tempfile.mkdtemp
    createDoc(request, "CV", foName)
    createDoc(request, "Cover Letter", foName)
    createDoc(request, "Motivation Letter", foName)
    zipFolder(request, foName)
    shutil.rmtree(tempDir)
    path = os.path.join(settings.BASE_DIR, "ApplicationAI/output", f"{foName}.zip")
    with open(path, "rb") as zFo:
        response = HttpResponse(zFo.read(), content_type = "application/zip")
        response["Content-Disposition"] = f"attachment; filename='{foName}.zip'"
    return response


# TESTS
def createExampleData(response):
    data = QueryDict(mutable=True)
    data["name"] = "Luca Staffner"
    data["position"] = "Software Engineer"
    data["companyName"] = "Google"
    data["sector"] = "Technology"
    data["companyNow"] = "Twitter"
    data["positionNow"] = "Data Scientist"
    data["skills"] = "Python, Problem Solving, Statistics, C#"
    data["experience"] = "Intern at Microsoft"
    data["achievements"] = "Increased revenue by 5 %"
    data["education"] = "2018-2021: University of Innsbruck Computer Science"
    data["sideProjects"] = "Flappy Bird Clone"
    response.GET = data
    return response
