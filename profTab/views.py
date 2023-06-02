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
    if (request.user.date_joined.date() == date.today()):
        user = User.objects.get(email=request.user.email)
        user.isProf = True
        user.save()
    else:
        if (request.user.isProf == False):
            return redirect('index')
    subjects = Subject.objects.all()
    taskT = TaskType.objects.all()
    gpTypes = GPType.objects.all()

    return render(request, "professor/prof.html", {
        'subjects': subjects,
        'tasksT': taskT,
        'gpTypes' : gpTypes
    })


@csrf_exempt
def subject(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # data = json.loads(request.body)
    subjectCode = request.POST.get('subjectCode', "")
    subName = request.POST.get('subjectName', "")
    fName = request.POST.get('facultyName', "")
    units = request.POST.get('units', 0)

    # edit
    editID = request.POST.get('editID', 0)
    subjectCodeEdit = request.POST.get('subjectCodeEdit', "")
    subNameEdit = request.POST.get('subjectNameEdit', "")
    unitsEdit = request.POST.get('unitsEdit', 0)

    quizEdit = request.POST.get('quizEdit', 0)
    performanceTaskEdit = request.POST.get('performancetaskEdit', 0)
    prelimsEdit = request.POST.get('prelimsEdit', 0)
    midtermsEdit = request.POST.get('midtermEdit', 0)
    finalsEdit = request.POST.get('finalsEdit', 0)
    projectEdit = request.POST.get('projectEdit', 0)

    deletemySub = request.POST.get('subDeleteID', 0)
    if deletemySub:
        subToDelete = Subject.objects.get(pk=deletemySub)
        subToDelete.delete()

    if editID:
        # facultyUser = User.objects.get(pk=request.user.id)
        mySubject = Subject.objects.get(pk=editID)
        mySubject.subjectCode = subjectCodeEdit
        mySubject.subjectName = subNameEdit
        mySubject.units = unitsEdit

        mySubject.save()

        addRubricks("Quiz", mySubject, 0 if quizEdit ==
                    '' else quizEdit, isEdit=1)
        addRubricks("PerformanceTask", mySubject, 0 if performanceTaskEdit ==
                    '' else performanceTaskEdit, isEdit=1)
        addRubricks("Prelims", mySubject, 0 if prelimsEdit ==
                    '' else prelimsEdit, isEdit=1)
        addRubricks("Midterm", mySubject, 0 if midtermsEdit ==
                    '' else midtermsEdit, isEdit=1)
        addRubricks("Finals", mySubject, 0 if finalsEdit ==
                    '' else finalsEdit, isEdit=1)
        addRubricks("Project", mySubject, 0 if projectEdit ==
                    '' else projectEdit, isEdit=1)

    # rubricks
    quiz = request.POST.get('quiz', 0)
    performanceTask = request.POST.get('performancetask', 0)
    prelims = request.POST.get('prelims', 0)
    midterms = request.POST.get('midterm', 0)
    finals = request.POST.get('finals', 0)
    project = request.POST.get('project', 0)

    if subjectCode:
        facultyUser = User.objects.get(pk=request.user.id)
        studentSubject = Subject(
            subjectCode=subjectCode, subjectName=subName, facultyName=facultyUser, units=units)
        studentSubject.save()

        addRubricks("Quiz", studentSubject, quiz)
        addRubricks("PerformanceTask", studentSubject, performanceTask)
        addRubricks("Prelims", studentSubject, prelims)
        addRubricks("Midterm", studentSubject, midterms)
        addRubricks("Finals", studentSubject, finals)
        addRubricks("Project", studentSubject, project)

    # setRubricks = Rubrick(SubjectID = studentSubject,)

    return JsonResponse({"message": "data added successfully."}, status=201)


def addRubricks(a, b, c, isEdit=0):
    if isEdit:
        t_id = TaskType.objects.get(taskType=a)
        subject = Subject.objects.get(pk=b.id)
        new_rub = Rubrick.objects.get(subjectID=subject, taskTypeID=t_id)
        new_rub.percentage = c
        new_rub.save()
    else:
        t_id = TaskType.objects.get(taskType=a)
        setRubricks = Rubrick(subjectID=b, taskTypeID=t_id, percentage=c)
        setRubricks.save()


def getMySubjects(request, subId):
    test = Subject.objects.get(pk=subId)
    # Get the target faculty user instance
    target_faculty = User.objects.get(pk=request.user.id)

    rubricks = Rubrick.objects.filter(
        subjectID__facultyName=target_faculty, subjectID=test)
    return JsonResponse([rub.serialize(isprof=1) for rub in rubricks], safe=False)


def getAllMyStudents(request,profid):
    # Retrieve the faculty object based on the faculty_id
    faculty = User.objects.get(id=profid)

    # Get all the student subjects associated with the faculty
    student_subjects = StudentSubject.objects.filter(
        subjectID__facultyName=faculty)

    serialized_data = []
    for rub in student_subjects:
        serialized_obj = rub.serialize()
        print(serialized_obj)
        if serialized_obj not in serialized_data:
            serialized_data.append(serialized_obj)
            
    return JsonResponse(serialized_data, safe=False)
