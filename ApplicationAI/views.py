from django.shortcuts import render, redirect
from django.http import QueryDict
import os
from django.http import FileResponse, HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate, login
import openai
import subprocess
from django.views.decorators.csrf import csrf_exempt
from .models import Users
from .forms import fRegister


# GLOBAL vars
openai.api_key = "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"


# RETURN PAGES
def index(request):
    return render(request, "index.html")


def app(request):
    return render(request, "app.html")


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
            #TODO need to include error message
            error_message = "Invalid username or password"
            return render(request, 'index.html', {'error_message': error_message})
    else:
        return render(request, 'index.html')


def updateUserNumber():
    pass


def saveUserDataToDB():
    pass


# PROMPT GENERATION AND GPT
def createPromptCV(data):
    prompt = "Write a short and beautiful CV in LaTex. "
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


def createPromptCL(request):
    pass


def createPromptML(request):
    pass


def getOutputFromChatGPT(prompt, numTokens):
    try:
        response = openai.Completion.create(
                engine = "text-davinci-002",
                prompt = prompt,
                max_tokens = numTokens
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print("Error: "+e)
        return "Error"


# CREATE PDF
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


def createDoc(request, ty):
    request = createExampleData(request)
    match ty:
        case "CV":
            prompt = createPromptCV(request)
        case "CL":
            prompt = createPromptCL(request)
        case "ML":
            prompt = createPromptML(request)
    print(prompt)
    print(getOutputFromChatGPT(prompt, 10000))
    compileToPDF()


def removeOldFiles(name):
    pass


# MAIN
def download(request):
    createDoc(request, "CV")
    fileName = "EngelUndTeufel.pdf"
    dName = "CV.pdf"
    filePath = os.path.join(settings.BASE_DIR, "ApplicationAI/output", fileName)
    file = open(filePath, 'rb')
    response = FileResponse(file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename='+dName
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
