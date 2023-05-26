from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect 
from django.urls import reverse 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from datetime import date


# Create your views here.
from Eportfolio.models import *


@login_required
def index(request):
    if(request.user.date_joined.date() == date.today()):
        user = User.objects.get(email = request.user.email)
        user.isProf =  True
        user.save()
    else:
        if(request.user.isProf == False):
            return redirect('index')
    subjects = Subject.objects.all()
    taskT = TaskType.objects.all()
    
    return render(request, "professor/prof.html",{
        'subjects' : subjects,
        'tasksT' : taskT
    })
    
    
@csrf_exempt
def subject(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)


    # data = json.loads(request.body)
    subjectCode = request.POST.get('subjectCode',"")
    subName = request.POST.get('subjectName',"")
    fName = request.POST.get('facultyName',"")
    units = request.POST.get('units',0)
    
    
    # rubricks
    quiz = request.POST.get('quiz',0)
    performanceTask = request.POST.get('performancetask',0)
    prelims = request.POST.get('prelims',0)
    midterms = request.POST.get('midterm',0)
    finals = request.POST.get('finals',0)
    project = request.POST.get('project',0)
    
    studentSubject = Subject(subjectCode = subjectCode,subjectName = subName, facultyName= fName,units=units)
    studentSubject.save()
    
    
        
    addRubricks("Quiz",studentSubject,quiz) 
    addRubricks("PerformanceTask",studentSubject,performanceTask) 
    addRubricks("Prelims",studentSubject,prelims) 
    addRubricks("Midterm",studentSubject,midterms) 
    addRubricks("Finals",studentSubject,finals) 
    addRubricks("Project",studentSubject,project) 


    # setRubricks = Rubrick(SubjectID = studentSubject,)
    
    return JsonResponse({"message": "data added successfully."}, status=201)    


def addRubricks(a,b,c):
        t_id = TaskType.objects.get(taskType = a)
        setRubricks = Rubrick(subjectID = b,taskTypeID = t_id,percentage = c )
        setRubricks.save()   
    


def prof_auth(request):

    return render(request,'professor/login_prof.html')


    
    