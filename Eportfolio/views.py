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
        if request.user.isProf == True:
            return redirect('indexProf')
        userid = User.objects.get(username=request.user)
        if (Studentprofile.objects.filter(userID=userid).count() > 0):
            studentN = Studentprofile.objects.get(userID=userid)
            return HttpResponseRedirect(reverse('studentProfile', args=(studentN.studentNumber,)))
        if request.user.username == "jan":
            return HttpResponseRedirect(reverse('admin'))

        # return HttpResponseRedirect(reverse('profileForm'))

    return render(request, "landing/landing.html")


@login_required
def demographicForm(request):
    if request.user.isProf == True:
        return redirect('indexProf')
    userid = User.objects.get(username=request.user)
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
                'error': 'Wrong Format'

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


def studentProfile(request, studentID):
    studentprof = Studentprofile.objects.get(studentNumber=studentID)
    gender = Gender.objects.get(pk=1)
    yearlist = YearLevel.objects.all()
    courselist = Course.objects.all()

    studentSibjects = StudentSubject.objects.filter(
        studentProfileID=studentprof)

    availableSubs = Subject.objects.all()
    ids = [i.subjectID for i in studentSibjects]
    subjects = Subject.objects.filter(pk__in=ids)
    studentTasks = Task.objects.filter(
        studentProfileID=studentprof)

    percentage = {}

    data = {}
    if studentTasks:
        for sub in subjects:
            sub = {f"{sub}": {}}
            percentage.update(sub)

        for sub in subjects:
            rubrik = Rubrick.objects.filter(
                subjectID=sub).filter(~Q(percentage=0))
            for rub in rubrik:
                scoreHolder = []
                for task in studentTasks:
                    if (rub.taskTypeID == task.task_Type and task.taskSubject == sub):
                        if f"{task.task_Type}" in percentage[f'{sub}']:
                            counter += 1
                        else:
                            percentage[f'{sub}'].update(
                                {f"{task.task_Type}": task.score})
                            counter = 1
                        scoreHolder.append(
                            int(task.score/task.overallscore * 100)/100)

                percent = 100/counter
                total = 0
                for score in scoreHolder:
                    total += percent * score
                if total and scoreHolder:
                    if f'{sub}' in data:
                        data[f'{sub}'].update({f'{rub.taskTypeID}': total})
                    else:
                        data[f'{sub}'] = {f'{rub.taskTypeID}': total}

    if request.method == "POST":
        subID = request.POST.get('addSub', 0)
        # edit profile below
        isEdit = request.POST.get('editProfile', 0)
        guardName = request.POST.get('guardianName', 0)
        guardNumber = request.POST.get('guardianNum', 0)
        courseName = request.POST.get('courseName', 0)
        yearName = request.POST.get('yearName', 0)
        contactD = request.POST.get('contactD', 0)

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
            sub = StudentSubject(studentProfileID=studentprof, subjectID=subID)
            sub.save()
        # studentNumber = studentprof.studentNumber
        return JsonResponse([{'data': 1}], safe=False)

    return render(request, "studentProfile.html", {
        'studentprof': studentprof,
        'subjects': subjects,
        'availSubs': availableSubs,
        'test':  data,
        'yearList':  yearlist,
        'courseList':  courselist,
        'male': gender
    })


@login_required
def studentSubject(request, studentID, subjectCode):
    profile = Studentprofile.objects.get(studentNumber=studentID)

    subject = Subject.objects.get(subjectCode=subjectCode)

    studentTasks = Task.objects.filter(
        studentProfileID=profile, taskSubject=subject)
    rubrik = Rubrick.objects.filter(subjectID=subject).filter(~Q(percentage=0))

    if request.method == "POST":
        isEdit = request.POST.get('editType', 0)  # this is the ID
        type = request.POST.get('taskType', '')
        title = request.POST.get('taskTitle', '')
        myScore = request.POST.get('taskScore', 0)
        totalScore = request.POST.get('taskTotal', 0)
        date = request.POST.get('taskDate', 0)
        image = request.FILES.get('taskAttachments', False)
        taskToBeDelete = request.POST.get('taskDeleteID', False)

        if taskToBeDelete:
            deleteTask = Task.objects.get(pk=taskToBeDelete)
            deleteTask.delete()



        if isEdit:
            tType = TaskType.objects.get(taskType=type)
            getTask = Task.objects.get(pk=isEdit)
            getTask.task_Type = tType
            getTask.title = title
            getTask.score = myScore
            getTask.overallscore = totalScore
            getTask.date = date
            if image:
                getTask.image = image
            getTask.save()

            return HttpResponseRedirect(reverse("studentSubject", args=(str(profile.studentNumber), str(subject.subjectCode))))

        if type:
            tType = TaskType.objects.get(taskType=type)
            uploadedTask = Task(studentProfileID=profile, task_Type=tType, taskSubject=subject, title=title,
                                overallscore=totalScore, score=myScore, image=image, date=date)
            uploadedTask.save()
            return HttpResponseRedirect(reverse("studentSubject", args=(str(profile.studentNumber), str(subject.subjectCode))))

    return render(request, 'studentSubject.html', {
        'subject': subject,
        'sNumber': studentID,
        'rubricks': rubrik,
        'tasks': studentTasks,
    })


def about(request):
    return render(request, 'landing/about.html')


def overview(request):
    return render(request, 'landing/overview.html')


def contact(request):
    return render(request, 'landing/contact.html')
