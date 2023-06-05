from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db import IntegrityError
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
    userFaculty = User.objects.get(pk=request.user.id)
    availableSubs = Subject.objects.filter(facultyName=userFaculty)
    return render(request, "professor/prof.html", {
        'subjects': subjects,
        'tasksT': taskT,
        'gpTypes': gpTypes,
        'mysubs':availableSubs,
    })


@csrf_exempt
def subject(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # delete sub ----------------------------

    deletemySub = request.POST.get('subDeleteID', 0)

    if deletemySub:
        subToDelete = Subject.objects.get(pk=deletemySub)
        subToDelete.delete()
        return JsonResponse({"message": "data deleted successfully."}, status=201)

    # delete sub ----------------------------

    courseCode = request.POST.get('courseCode', '')
    courseName = request.POST.get('courseName', '')
    faculty = User.objects.get(pk=request.user.id)

    studentSubject = Subject(
        subjectCode=courseCode, subjectName=courseName, facultyName=faculty)
    studentSubject.save()

    gpTypes = GPType.objects.all()
    tasktypes = TaskType.objects.all()

    for gp in gpTypes:
        subPercent = request.POST.get(f'{gp}percentage', 0)
        setSubRubrick = SubjectRubrick(
            subjectObj=studentSubject, gpObjt=gp, percentage=subPercent if subPercent != '' else 0)
        setSubRubrick.save()
        gptypeSub = studentSubject
        totalExam = request.POST.get(f'{gp}TotalExam', 0)
        totalProject = request.POST.get(f'{gp}TotalProject', 0)

        subjectGP = GradePeriods(
            subject=gptypeSub, gptype=gp, exam=totalExam if totalExam != '' else 0, projectTotal=totalProject if totalProject != '' else 0)
        subjectGP.save()

        gpCounter = request.POST.get(f'{gp}Counter', 0)

        if gpCounter:
            for i in range(int(gpCounter)):
                title = request.POST.get(f"{gp}TitleCP{i+1}", '')
                totalItems = request.POST.get(f"{gp}TotalItemCP{i+1}", '')
                cptypeID = request.POST.get(f"{gp}ID{i+1}", '')

                try:
                    cptypeObj = CPType.objects.get(pk=cptypeID)
                    print(title, totalItems, cptypeObj)
                    newClassP = ClassPerformance(
                        title=title, gpObject=subjectGP, cptype=cptypeObj, totalScore=totalItems)
                    newClassP.save()
                except:
                    return JsonResponse({"error": "Invalid Inputs."})

        for task in tasktypes:
            percentage = request.POST.get(f"{gp}{task}", 0)
            rubrick = Rubrick(gpObjt=subjectGP, taskTypeID=task,
                              percentage=percentage if percentage != '' else 0)
            rubrick.save()
    return JsonResponse({"message": "data added successfully."}, status=201)


def getMySubjects(request, subId):
    test = Subject.objects.get(pk=subId)
    # Get the target faculty user instance
    target_faculty = User.objects.get(pk=request.user.id)

    rubricks = Rubrick.objects.filter(
        subjectID__facultyName=target_faculty, subjectID=test)
    return JsonResponse([rub.serialize(isprof=1) for rub in rubricks], safe=False)


def getAllMyStudents(request, profid):
    # Retrieve the faculty object based on the faculty_id
    faculty = User.objects.get(pk=profid)

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


def editSubject(request, subID):
    # Assuming you have the required subjectCode and subjectName variables
    subject = Subject.objects.get(pk=subID)

    # Retrieve the related grade periods for the subject
    grade_periods = GradePeriods.objects.filter(subject=subject)

    # Initialize the dictionary
    dic = {
        'courseCode': subject.subjectCode,
        'courseName': subject.subjectName,
        'ID': subject.id,
        'Prelims': {},
        'Midterm': {},
        'Finals': {}
    }
    for gp in grade_periods:
        # Retrieve the rubrick for the grade period
        rubrick = Rubrick.objects.filter(gpObjt=gp)
        subRub = SubjectRubrick.objects.get(
            subjectObj=subject, gpObjt=gp.gptype)
        # Retrieve the class performances for the grade period
        class_performances = ClassPerformance.objects.filter(gpObject=gp)

        # Initialize the grade period dictionary
        gp_dict = {
            'percentageSUB': subRub.percentage,
            'gpid': gp.id,
            'totalItem': gp.exam,
            'totalProject': gp.projectTotal,
            'cpTask': [],
            'percentage': {}
        }
        for i in rubrick:
            gp_dict['percentage'].update({i.taskTypeID.taskType: i.percentage})

        # Iterate over the class performances and populate the cpTask dictionary
        for i, cp in enumerate(class_performances):
            cp_task_dict = {
                'title': cp.title,
                'cptype': cp.cptype.cptypeName,
                'noItems': cp.totalScore,
                'cptypeID': cp.cptype.id,
                'id': cp.id,
            }
            gp_dict['cpTask'].append(cp_task_dict)

        # Add the grade period dictionary to the respective section in the main dictionary
        if gp.gptype.gptypeName == 'Prelims':
            dic['Prelims'] = gp_dict
        elif gp.gptype.gptypeName == 'Midterm':
            dic['Midterm'] = gp_dict
        elif gp.gptype.gptypeName == 'Finals':
            dic['Finals'] = gp_dict

    return JsonResponse(dic, safe=False)


@csrf_exempt
def edit_subject_form(request, sub_id):
    # Retrieve the existing subject and related objects from the database based on the subject ID
    try:
        subject = Subject.objects.get(pk=sub_id)
    except Subject.DoesNotExist:
        return JsonResponse({"error": "Subject not found."}, status=404)

    # Update the subject data
    subject.subjectCode = request.POST.get(
        'courseCodeEdit', subject.subjectCode)
    subject.subjectName = request.POST.get(
        'courseNameEdit', subject.subjectName)
    subject.save()

    # Update the grade periods and related objects
    gpTypes = GPType.objects.all()
    tasktypes = TaskType.objects.all()

    for gp in gpTypes:

        percentageEdit = request.POST.get(f'{gp}percentageEdit',0)
        updateSubRub = SubjectRubrick.objects.get(
            subjectObj=subject, gpObjt=gp)
        updateSubRub.percentage = percentageEdit if percentageEdit != '' else 0
        updateSubRub.save()

        # Update the GradePeriods object
        try:
            subjectGP = GradePeriods.objects.get(subject=subject, gptype=gp)
        except GradePeriods.DoesNotExist:
            continue

        subjectGP.exam = request.POST.get(f'{gp}TotalExamEdit', subjectGP.exam)
        subjectGP.projectTotal = request.POST.get(
            f'{gp}TotalProjectEdit', subjectGP.projectTotal)

        subjectGP.save()

        gpCounter = request.POST.get(f'{gp}CounterEdit', 0)

        if gpCounter:
            # Update the ClassPerformance objects
            ClassPerformance.objects.filter(gpObject=subjectGP).delete()

            for i in range(int(gpCounter)):
                title = request.POST.get(f"{gp}TitleCP{i+1}Edit", '')
                totalItems = request.POST.get(f"{gp}TotalItemCP{i+1}Edit", '')
                cptypeID = request.POST.get(f"{gp}ID{i+1}Edit", '')

                if not cptypeID:  # Skip the iteration if cptypeID is empty
                    continue

                cptypeObj = CPType.objects.get(pk=cptypeID)
                newClassP = ClassPerformance(
                        title=title, gpObject=subjectGP, cptype=cptypeObj, totalScore=totalItems)
                newClassP.save()
               

                    
        # Update the Rubrick objects
        for task in tasktypes:
            try:
                rubrick = Rubrick.objects.get(
                    gpObjt=subjectGP, taskTypeID=task)
            except Rubrick.DoesNotExist:
                continue

            rubrick.percentage = request.POST.get(
                f"{gp}{task}Edit", 0) if request.POST.get(
                f"{gp}{task}Edit", 0) != '' else 0 
            rubrick.save()

    return JsonResponse({"message": "Data updated successfully."}, status=200)
