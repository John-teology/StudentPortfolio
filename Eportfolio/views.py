from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import *
import re

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


@csrf_exempt
def studentProfile(request, studentID):
    studentprof = Studentprofile.objects.get(studentNumber=studentID)
    studentSibjects = StudentSubject.objects.filter(studentProfileID=studentprof)
    availableSubs = Subject.objects.all()
    ids = [i.subjectID for i in studentSibjects]
    subjects = Subject.objects.filter(pk__in=ids)

    
    if request.method == "POST":
        subID = request.POST['addSub']

        sub = StudentSubject(studentProfileID=studentprof, subjectID=subID)
        sub.save()
        # studentNumber = studentprof.studentNumber
        return JsonResponse([{'data': 1}], safe=False)

    return render(request, "studentProfile.html", {
        'studentprof': studentprof,
        'subjects': subjects,
        'availSubs': availableSubs
    })


@login_required
def studentSubject(request, studentID, subjectCode):
    profile = Studentprofile.objects.get(studentNumber=studentID)
    subject = Subject.objects.get(
        studentProfileID=profile, subjectCode=subjectCode)
    studentTask = Task.objects.filter(taskSubject=subject)
    tasktype = TaskType.objects.all()
    rubrik = Rubrick.objects.filter(subjectID=subject).filter(~Q(percentage=0))

    if request.method == "POST":
        type = request.POST['type']
        title = request.POST['title']
        myScore = request.POST['myScore']
        totalScore = request.POST['totalScore']
        date = request.POST['date']
        image = request.FILES['image']

        tType = TaskType.objects.get(taskType=type)
        uploadedTask = Task(task_Type=tType, taskSubject=subject, title=title,
                            overallscore=totalScore, score=myScore, image=image, date=date)
        uploadedTask.save()
        return HttpResponseRedirect(reverse("studentSubject", args=(str(profile.studentNumber), str(subject.subjectCode))))
    return render(request, 'studentSubject.html', {
        'subject': subject,
        'sNumber': studentID,
        'task': studentTask,
        'types': tasktype,
        'rubricks': rubrik
    })


def about(request):
    return render(request, 'landing/about.html')


def overview(request):
    return render(request, 'landing/overview.html')


def contact(request):
    return render(request, 'landing/contact.html')
