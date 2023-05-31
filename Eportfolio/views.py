from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import *
import re
import json

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        if request.user.email[-10:] != 'tup.edu.ph':
            Invalid_User = User.objects.get(pk =request.user.id)
            Invalid_User.delete()
            return HttpResponseRedirect(reverse('index'))
        if request.user.isProf == True:
            return redirect('indexProf')
        userid = User.objects.get(pk=request.user.id)
        if (Studentprofile.objects.filter(userID=userid).count() > 0):
            studentN = Studentprofile.objects.get(userID=userid)
            return HttpResponseRedirect(reverse('studentProfile', args=(studentN.studentNumber,)))
        if request.user == "Admin":
            return HttpResponseRedirect(reverse('admin'))

        # return HttpResponseRedirect(reverse('profileForm'))

    return render(request, "landing/landing.html")


@login_required
def demographicForm(request):
    if request.user.isProf == True:
        return redirect('indexProf')
    userid = User.objects.get(pk=request.user.id)
    if (Studentprofile.objects.filter(userID=userid).count() > 0):
        studentN = Studentprofile.objects.get(userID=userid)
        return HttpResponseRedirect(reverse('studentProfile', args=(studentN.studentNumber,)))

    if request.method == "POST":
        studentNumber = request.POST['studentNumber']
        first = request.user.first_name
        last = request.user.last_name
        course = request.POST['course']
        yearlevel = request.POST['yearlevel']
        gender = request.POST['gender']
        phoneNumber = request.POST['phoneNumber']
        email = request.user.email
        guardianNumber = request.POST['guardianNumber']
        guardianName = request.POST['guardianName']

        studentNumberFormat = r'^TUPM-\d{2}-\d{4}$'

        match_result = re.match(studentNumberFormat, studentNumber)

        if not match_result:
            return render(request, "studentForm.html", {
                'courses': Course.objects.all(),
                'yearLevels': YearLevel.objects.all(),
                'gender': Gender.objects.all(),
                'studentNumber': studentNumber,
                'first': first,
                'last': last,
                'phoneNumber': phoneNumber,
                'email': email,
                'guardianNumber': guardianNumber,
                'course': course,
                'guardianName': guardianName,
                'error': 'Invalid Student Number'

            })

        if (Studentprofile.objects.filter(studentNumber=studentNumber).count() > 0):
            return render(request, "studentForm.html", {
                'courses': Course.objects.all(),
                'yearLevels': YearLevel.objects.all(),
                'gender': Gender.objects.all(),
                'studentNumber': studentNumber,
                'first': first,
                'last': last,
                'phoneNumber': phoneNumber,
                'email': email,
                'guardianNumber': guardianNumber,
                'course': course,
                'guardianName': guardianName,
                'error': 'Already Added TUP Number'

            })

        courseInstance = Course.objects.get(pk=course)
        yearInstance = YearLevel.objects.get(pk=yearlevel)
        genderInstance = Gender.objects.get(pk=gender)

        studentProfile = Studentprofile(userID=request.user, studentNumber=studentNumber, lastName=last, firstName=first, courseID=courseInstance, yearID=yearInstance,
                                        genderID=genderInstance, contactNumber=phoneNumber, emailAddress=email, guardianNumber=guardianNumber, guardianName=guardianName)

        studentProfile.save()
        return HttpResponseRedirect(reverse("studentProfile", args=(str(studentNumber),)))

    return render(request, "studentForm.html", {
        'courses': Course.objects.all(),
        'yearLevels': YearLevel.objects.all(),
        'gender': Gender.objects.all(),
    })


@csrf_exempt
def studentProfile(request, studentID):
    studentprof = Studentprofile.objects.get(studentNumber=studentID)
    gender = Gender.objects.get(pk=1)
    yearlist = YearLevel.objects.all()
    courselist = Course.objects.all()


    studentSubjects = StudentSubject.objects.filter(
        studentProfileID=studentprof, ishide=False)
    subjectIDs = [
        studentSubject.subjectID_id for studentSubject in studentSubjects]
    subjects = Subject.objects.filter(id__in=subjectIDs)

    studentTasks = Task.objects.filter(
        studentProfileID=studentprof)

    availableSubs = Subject.objects.all()

    studentTasks = Task.objects.filter(
        studentProfileID=studentprof)

    data = dataForGraph(subjects, studentTasks)
    dataD = dataForGraph(subjects, studentTasks, isrubick=1)

    if request.method == "POST":

        # user subject ids
        subID = request.POST.get('addSub', 0)
        deleteSubId = request.POST.get('deleteSubId', 0)

        # edit profile below
        isEdit = request.POST.get('editProfile', 0)
        guardName = request.POST.get('guardianName', 0)
        guardNumber = request.POST.get('guardianNumber', 0)
        courseName = request.POST.get('courseID', 0)
        yearName = request.POST.get('yearID', 0)
        contactD = request.POST.get('contactNumber', 0)

        # add task
        typeID = request.POST.get('taskType', '')
        subjectID = request.POST.get('taskSubject', '')
        title = request.POST.get('taskTitle', '')
        myScore = request.POST.get('taskScore', 0)
        totalScore = request.POST.get('taskTotal', 0)
        date = request.POST.get('taskDate', 0)
        image = request.FILES.get('taskAttachments', "")
        taskToBeDelete = request.POST.get('taskDeleteID', False)

        # edit task
        isEditType = request.POST.get('taskIdEdit', 0)  # this is the ID
        typeIDEdit = request.POST.get('taskTypeEdit', '')
        subjectIDEdit = request.POST.get('taskSubjectEdit', '')
        titleEdit = request.POST.get('taskTitleEdit', '')
        myScoreEdit = request.POST.get('taskScoreEdit', 0)
        totalScoreEdit = request.POST.get('taskTotalEdit', 0)
        dateEdit = request.POST.get('taskDateEdit', 0)
        imageEdit = request.FILES.get('taskAttachmentsEdit', "")

        if taskToBeDelete:
            deleteTask = Task.objects.get(pk=taskToBeDelete)
            deleteTask.delete()
            subjects = Subject.objects.filter(id__in=subjectIDs)

            studentTasks = Task.objects.filter(
                studentProfileID=studentprof)
            data = dataForGraph(subjects, studentTasks)
            dataD = dataForGraph(subjects, studentTasks, isrubick=1)

            return JsonResponse({'data': data, 'dounut': dataD}, safe=False)

        if typeID:
            tType = TaskType.objects.get(pk=typeID)
            subject = Subject.objects.get(pk=subjectID)
            studentSub = StudentSubject.objects.get(
                studentProfileID=studentprof, subjectID=subject)
            uploadedTask = Task(studentProfileID=studentprof, task_Type=tType, taskSubject=subject, title=title,
                                overallscore=totalScore, score=myScore, image=image, date=date, subjectStudent=studentSub)
            uploadedTask.save()
            subjects = Subject.objects.filter(id__in=subjectIDs)

            studentTasks = Task.objects.filter(
                studentProfileID=studentprof)
            data = dataForGraph(subjects, studentTasks)
            dataD = dataForGraph(subjects, studentTasks, isrubick=1)

            return JsonResponse({"title": uploadedTask.title, "myscore": uploadedTask.score, "overallscore": uploadedTask.overallscore, "date": uploadedTask.date, 'type': tType.taskType, 'subject': subject.subjectName, 'attaachment':  uploadedTask.image.url if uploadedTask.image else None, "data": data, 'dounut': dataD}, safe=False)

        if isEditType:
            try:
                modifiedTask = Task.objects.get(pk=isEditType)
                print(modifiedTask.title)
                tTypeNew = TaskType.objects.get(pk=typeIDEdit)
                subjectNew = Subject.objects.get(pk=subjectIDEdit)
                studentSub = StudentSubject.objects.get(
                    studentProfileID=studentprof, subjectID=subjectNew)
                modifiedTask.title = titleEdit
                modifiedTask.score = myScoreEdit
                modifiedTask.overallscore = totalScoreEdit
                modifiedTask.task_Type = tTypeNew
                modifiedTask.taskSubject = subjectNew
                modifiedTask.date = dateEdit
                modifiedTask.subjectStudent = studentSub
                modifiedTask.image = imageEdit
                modifiedTask.save()

                subjects = Subject.objects.filter(id__in=subjectIDs)
                studentTasks = Task.objects.filter(
                    studentProfileID=studentprof)
                data = dataForGraph(subjects, studentTasks)
                dataD = dataForGraph(subjects, studentTasks, isrubick=1)

                return JsonResponse({'data': 1, 'graphdata': data, 'dounut': dataD}, safe=False)
            except:
                return JsonResponse({'data': 0}, safe=False)

        if isEdit:
            yearObj = YearLevel.objects.get(yearLevel=yearName)
            courseObj = Course.objects.get(course=courseName)
            studentprof.guardianName = guardName
            studentprof.guardianNumber = guardNumber
            studentprof.courseID = courseObj
            studentprof.yearID = yearObj
            studentprof.contactNumber = contactD

            studentprof.save()

        if subID:
            addedSubject = Subject.objects.get(pk=subID)
            subjectCode = addedSubject.subjectCode
            subjectName = addedSubject.subjectName
            facultyName = addedSubject.facultyName
            studentprof = studentprof
            # Get the student profile instance
            # Check if there is an existing subject in StudentSubject with the same subjectCode and subjectName but different facultyName
            existing_subject = StudentSubject.objects.filter(
                (Q(subjectID__subjectCode=subjectCode) |
                 Q(subjectID__subjectName=subjectName)) &
                ~Q(subjectID__facultyName__username=facultyName) &
                Q(studentProfileID=studentprof)
            ).first()

            if existing_subject:
                return JsonResponse({'isAlreadyAdded': 1}, safe=False)
            else:
                # Subject does not exist in StudentSubject with the same subjectCode, subjectName, and different facultyName
                # Create and save the new StudentSubject instance
                sub = StudentSubject(
                    studentProfileID=studentprof, subjectID=addedSubject)
                sub.save()

            studentSubjects = StudentSubject.objects.filter(
                studentProfileID=studentprof, ishide=False)
            subjectIDs = [
                studentSubject.subjectID_id for studentSubject in studentSubjects]
            subjects = Subject.objects.filter(id__in=subjectIDs)
            studentTasks = Task.objects.filter(
                studentProfileID=studentprof)
            data = dataForGraph(subjects, studentTasks)
            dataD = dataForGraph(subjects, studentTasks, isrubick=1)
            return JsonResponse({'data': data, 'subjectCode': addedSubject.subjectCode, 'subjectName': addedSubject.subjectName, 'dounut': dataD}, safe=False)

        if deleteSubId:
            deletedSub = Subject.objects.get(pk=deleteSubId)
            toBeDeleteSubject = StudentSubject.objects.get(
                studentProfileID=studentprof, subjectID=deleteSubId)
            toBeDeleteSubject.delete()

            studentSubjects = StudentSubject.objects.filter(
                studentProfileID=studentprof, ishide=False)
            subjectIDs = [
                studentSubject.subjectID_id for studentSubject in studentSubjects]
            subjects = Subject.objects.filter(id__in=subjectIDs)
            studentTasks = Task.objects.filter(
                studentProfileID=studentprof)
            data = dataForGraph(subjects, studentTasks)
            dataD = dataForGraph(subjects, studentTasks, isrubick=1)
            return JsonResponse({'data': data, 'subjectCode': deletedSub.subjectCode, 'subjectName': deletedSub.subjectName, 'dounut': dataD}, safe=False)

    return render(request, "studentProfile.html", {
        'studentprof': studentprof,
        'subjects': subjects,
        'availSubs': availableSubs,
        'test':  data,
        'yearList':  yearlist,
        'courseList':  courselist,
        'male': gender,
        'tasks': studentTasks,
        'dounut': dataD
    })


# below are for ajax ----------------------------

def getUserSubject(request, studentNumber):
    user = Studentprofile.objects.get(studentNumber=studentNumber)
    studentSubjects = StudentSubject.objects.filter(
        studentProfileID=user, ishide=False)
    subjectIDs = [
        studentSubject.subjectID_id for studentSubject in studentSubjects]
    subjects = Subject.objects.filter(id__in=subjectIDs)
    return JsonResponse([subject.serialize(user) for subject in subjects], safe=False)


def getUserRubrick(request, subjectid):
    rubricks = Rubrick.objects.filter(
        subjectID=subjectid).filter(~Q(percentage=0))
    return JsonResponse([rub.serialize() for rub in rubricks], safe=False)


@csrf_exempt
def getUserTask(request, studentNumber):
    user = Studentprofile.objects.get(studentNumber=studentNumber)
    studentTasks = Task.objects.filter(
        studentProfileID=user)
    task_data = [task.serialize() for task in studentTasks]
    return JsonResponse(task_data, safe=False)


@csrf_exempt
def getAllSubject(request, studentNumber):
    user = Studentprofile.objects.get(studentNumber=studentNumber)
    availableSubs = Subject.objects.all()
    return JsonResponse([subject.serialize(user) for subject in availableSubs], safe=False)


@login_required
@csrf_exempt
def getAllProfSubject(request):
    userFaculty = User.objects.get(pk=request.user.id)
    availableSubs = Subject.objects.filter(facultyName=userFaculty)
    return JsonResponse([subject.serialize() for subject in availableSubs], safe=False)


def dataForGraph(subjects, studentTasks, isrubick=0):
    percentage = {}
    rubricksTotal = {}
    data = {}
    for sub in subjects:
        subd = {f"{sub.subjectCode}": {}}
        percentage.update(subd)
        rubricksTotal.update({f"{sub.subjectName}": 0})

    for sub in subjects:
        rubrik = Rubrick.objects.filter(
            subjectID=sub).filter(~Q(percentage=0))
        for rub in rubrik:
            scoreHolder = []
            counter = 1
            for task in studentTasks:
                if (rub.taskTypeID == task.task_Type and task.taskSubject == sub):
                    if f"{task.task_Type}" in percentage[f'{sub.subjectCode}']:
                        counter += 1
                    else:
                        percentage[f'{sub.subjectCode}'].update(
                            {f"{task.task_Type}": task.score})
                        counter = 1
                    scoreHolder.append(
                        int(task.score/task.overallscore * 100)/100)

            percent = 100/counter
            total = 0
            for score in scoreHolder:
                total += percent * score if score else 0
            # if isrubick:
            if f'{sub.subjectName}' in rubricksTotal:
                rubricksTotal[f'{sub.subjectName}'] += total * \
                    (float(rub.percentage/100))
            else:
                rubricksTotal[f'{sub.subjectName}'] = total * \
                    (float(rub.percentage/100))
            # else:
            if f'{sub.subjectCode}' in data:
                data[f'{sub.subjectCode}'].update(
                    {f'{rub.taskTypeID}': total if total else 0})
            else:
                data[f'{sub.subjectCode}'] = {
                    f'{rub.taskTypeID}': total if total else 0}

    return rubricksTotal if isrubick else data


def about(request):
    return render(request, 'landing/about.html')


def overview(request):
    return render(request, 'landing/overview.html')


def contact(request):
    return render(request, 'landing/contact.html')
