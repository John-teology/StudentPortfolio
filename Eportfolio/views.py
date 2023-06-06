from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import *
import re
import json
from django.db.models import Avg, F, FloatField


# Create your views here.
import json

import json

from django.http import JsonResponse


def index(request):
    if request.user.is_authenticated:
        # if request.user.email[-10:] != 'tup.edu.ph':
        #     Invalid_User = User.objects.get(pk =request.user.id)
        #     Invalid_User.delete()
        # return HttpResponseRedirect(reverse('index'))
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
        isScholarval = request.POST['scholarValue']
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
                                        genderID=genderInstance, contactNumber=phoneNumber, emailAddress=email, guardianNumber=guardianNumber, guardianName=guardianName,
                                        isScholar=True if isScholarval else False)

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

    test = TaskType.objects.get(pk=5)
    print(test)

    # data = dataForGraph(subjects, studentTasks)
    # dataD = dataForGraph(subjects, studentTasks, isrubick=1)

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
        gpTypeId = request.POST.get('gpType', '')
        taskTypeid = request.POST.get('cptypeid', '')
        subjectID = request.POST.get('taskSubject', '')
        title = request.POST.get('taskTitle', '')
        myScore = request.POST.get('taskScore', 0)
        totalScore = request.POST.get('taskTotal', 0)
        date = request.POST.get('taskDate', 0)
        image = request.FILES.get('taskAttachments', "")
        taskToBeDelete = request.POST.get('taskDeleteID', False)
        print(gpTypeId, subjectID, title, myScore, totalScore)

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

            # studentTasks = Task.objects.filter(
            #     studentProfileID=studentprof)
            # data = dataForGraph(subjects, studentTasks)
            # dataD = dataForGraph(subjects, studentTasks, isrubick=1)

            return JsonResponse({'succes': 1, }, safe=False)

        if subjectID:
            gpType = GPType.objects.get(pk=gpTypeId)
            tasktypeObj = TaskType.objects.get(id=taskTypeid)
            subject = Subject.objects.get(pk=subjectID)
            studentSub = StudentSubject.objects.get(
                studentProfileID=studentprof, subjectID=subject)

            existing_task = Task.objects.filter(
                taskSubject=subject,
                gptype=gpType,
                taskType=tasktypeObj,
                title=title,
            ).first()

            if existing_task:
                # Task with the same details already exists
                return JsonResponse({'message': 'Task already added'})
            uploadedTask = Task(studentProfileID=studentprof, gptype=gpType,
                                taskType=tasktypeObj, taskSubject=subject, title=title,
                                overallscore=totalScore, score=myScore, image=image, date=date, studentsubject=studentSub)
            uploadedTask.save()
            # subjects = Subject.objects.filter(id__in=subjectIDs)

            # studentTasks = Task.objects.filter(
            #     studentProfileID=studentprof)
            # data = dataForGraph(subjects, studentTasks)
            # dataD = dataForGraph(subjects, studentTasks, isrubick=1)

            return JsonResponse({"title": uploadedTask.title, "myscore": uploadedTask.score, "overallscore": uploadedTask.overallscore, "date": uploadedTask.date,  'subject': subject.subjectName, 'attaachment':  uploadedTask.image.url if uploadedTask.image else None, 'studentid': studentprof.id, 'value': [sub.serialize() for sub in subjects]}, safe=False)

        if isEditType:
            try:
                modifiedTask = Task.objects.get(pk=isEditType)

                modifiedTask.score = myScoreEdit
                modifiedTask.date = dateEdit
                modifiedTask.image = imageEdit
                modifiedTask.save()

                # subjects = Subject.objects.filter(id__in=subjectIDs)
                # studentTasks = Task.objects.filter(
                #     studentProfileID=studentprof)
                # data = dataForGraph(subjects, studentTasks)
                # dataD = dataForGraph(subjects, studentTasks, isrubick=1)

                return JsonResponse({'data': 1, 'studentid': studentprof.id, 'value': [sub.serialize() for sub in subjects]}, safe=False)
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

            # studentSubjects = StudentSubject.objects.filter(
            #     studentProfileID=studentprof, ishide=False)
            # subjectIDs = [
            #     studentSubject.subjectID_id for studentSubject in studentSubjects]
            # subjects = Subject.objects.filter(id__in=subjectIDs)
            # studentTasks = Task.objects.filter(
            #     studentProfileID=studentprof)
            # data = dataForGraph(subjects, studentTasks)
            # dataD = dataForGraph(subjects, studentTasks, isrubick=1)
            return JsonResponse({'subjectCode': addedSubject.subjectCode, 'subjectName': addedSubject.subjectName, }, safe=False)

        if deleteSubId:
            deletedSub = Subject.objects.get(pk=deleteSubId)
            toBeDeleteSubject = StudentSubject.objects.get(
                studentProfileID=studentprof, subjectID=deleteSubId)
            toBeDeleteSubject.delete()

            # studentSubjects = StudentSubject.objects.filter(
            #     studentProfileID=studentprof, ishide=False)
            # subjectIDs = [
            #     studentSubject.subjectID_id for studentSubject in studentSubjects]
            # subjects = Subject.objects.filter(id__in=subjectIDs)
            # studentTasks = Task.objects.filter(
            #     studentProfileID=studentprof)
            # data = dataForGraph(subjects, studentTasks)
            # dataD = dataForGraph(subjects, studentTasks, isrubick=1)
            return JsonResponse({'subjectCode': deletedSub.subjectCode, 'subjectName': deletedSub.subjectName, }, safe=False)

    return render(request, "studentProfile.html", {
        'studentprof': studentprof,
        'subjects': subjects,
        'availSubs': availableSubs,
        'yearList':  yearlist,
        'courseList':  courselist,
        'male': gender,
        'tasks': studentTasks,
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


def getAllCpType(request):
    ctypes = CPType.objects.all()
    return JsonResponse([cy.serialize() for cy in ctypes], safe=False)


def getSpecificSub(request, subID):
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

        # Retrieve the class performances for the grade period
        class_performances = ClassPerformance.objects.filter(gpObject=gp)

        # Initialize the grade period dictionary
        gp_dict = {
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


def get_activities_average(request, subject_id, student_id, isbar=1):
    # Get the subject code for the specific subject
    subject_code = Subject.objects.get(id=subject_id).subjectName
    subject_code_rubrick = Subject.objects.get(id=subject_id)

    # Get all distinct GPType names
    gptype_names = ['Prelims', 'Midterm', 'Finals']

    # Get all distinct TaskType names
    tasktype_names = TaskType.objects.values_list('taskType', flat=True)

    # Prepare the response data
    response_data = {}
    sumofdata = {
        "Prelims": 0,
        "Midterm": 0,
        "Finals": 0,
    }

    # Iterate over the GPType names
    for gptype_name in gptype_names:
        # Prepare the GPType data in the response
        response_data[gptype_name] = {}

        # Get the Rubrick objects for the current subject and GPType
        rubricks = Rubrick.objects.filter(
            gpObjt__subject_id=subject_id, gpObjt__gptype__gptypeName=gptype_name)

        # Iterate over the TaskType names
        for tasktype_name in tasktype_names:
            # Get the Rubrick object for the current task type
            rubrick = rubricks.filter(
                taskTypeID__taskType=tasktype_name).first()

            if rubrick:
                # Get the rubric percentage for the current task type
                rubrick_percentage = rubrick.percentage
            else:
                # If no rubric exists, default to 0 percentage
                rubrick_percentage = 0

            # Get the computed score per GPType and TaskType for the specific subject and student
            if tasktype_name == 'Attendance':
                # Set the attendance score to always be 100
                average_score = 100
            else:
                task_scores = Task.objects.filter(
                    taskSubject_id=subject_id,
                    studentProfileID_id=student_id,  # Filter tasks by student ID
                    gptype__gptypeName=gptype_name,
                    taskType__taskType=tasktype_name,
                ).values('score', 'overallscore')

                # Calculate the average computed score for the specific GPType and TaskType
                if task_scores.exists():
                    total_weighted_score = sum(
                        ((score['score'] / score['overallscore']) * 50) + 50
                        for score in task_scores
                    )
                    average_score = total_weighted_score / task_scores.count()
                else:
                    average_score = 0

            # Calculate the value for response_data[gptype_name][tasktype_name]

            value = average_score * (rubrick_percentage / 100)
            value_str = f'{round(value, 2)} / {rubrick_percentage} %'
            valOnly = round(value, 2)
            sumofdata[gptype_name] += valOnly

            # Add the computed score to the GPType data in the response
            response_data[gptype_name][tasktype_name] = value_str
        gpname = GPType.objects.get(gptypeName=gptype_name)
        subRub = SubjectRubrick.objects.get(
            subjectObj=subject_code_rubrick, gpObjt=gpname)
        print(subRub)
        print(sumofdata[gptype_name])

    # Create a new dictionary with subject code as key and response data as value
    if isbar:
        response_data = {subject_code: sumofdata}
    else:
        response_data = {subject_code: response_data}

    # Return the response as JSON
    return JsonResponse(response_data)


def get_gender_percentage_per_subject(request, subject_id, user_id):
    user = User.objects.get(pk=user_id)
    subject = Subject.objects.get(pk=subject_id)

    male_count = StudentSubject.objects.filter(
        subjectID=subject, subjectID__facultyName=user, studentProfileID__genderID__gender='Male').count()

    female_count = StudentSubject.objects.filter(
        subjectID=subject, subjectID__facultyName=user, studentProfileID__genderID__gender='Female').count()

    total_students = male_count + female_count

    if total_students > 0:
        male_percentage = (male_count / total_students) * 100
        female_percentage = (female_count / total_students) * 100
    else:
        male_percentage = 0
        female_percentage = 0

    gender_percentage = {
        'subject': subject.subjectName,
        'male_percentage': male_percentage,
        'female_percentage': female_percentage
    }

    return JsonResponse(gender_percentage)


def get_scholar_percentage_per_subject(request, subject_id, user_id):
    user = User.objects.get(pk=user_id)
    subject = Subject.objects.get(pk=subject_id)

    scholar_count = StudentSubject.objects.filter(
        subjectID=subject, subjectID__facultyName=user, studentProfileID__isScholar=True).count()

    non_scholar_count = StudentSubject.objects.filter(
        subjectID=subject, subjectID__facultyName=user, studentProfileID__isScholar=False).count()

    total_students = scholar_count + non_scholar_count

    if total_students > 0:
        scholar_percentage = (scholar_count / total_students) * 100
        non_scholar_percentage = (non_scholar_count / total_students) * 100
    else:
        scholar_percentage = 0
        non_scholar_percentage = 0

    scholar_percentage_data = {
        'subject': subject.subjectName,
        'scholar_percentage': scholar_percentage,
        'non_scholar_percentage': non_scholar_percentage
    }

    return JsonResponse(scholar_percentage_data)


def totalSubjectRubrick(request, subject_id, student_id):
    # Get the subject code for the specific subject
    subject_code_rubrick = Subject.objects.get(id=subject_id)

    # Get all distinct GPType names
    gptype_names = ['Prelims', 'Midterm', 'Finals']

    # Get all distinct TaskType names
    tasktype_names = TaskType.objects.values_list('taskType', flat=True)

    # Prepare the response data
    response_data = {}
    sumofdata = {
        "Prelims": 0,
        "Midterm": 0,
        "Finals": 0,
    }
    Totalvalue = 0
    # Iterate over the GPType names
    for gptype_name in gptype_names:
        # Prepare the GPType data in the response
        response_data[gptype_name] = {}

        # Get the Rubrick objects for the current subject and GPType
        rubricks = Rubrick.objects.filter(
            gpObjt__subject_id=subject_id, gpObjt__gptype__gptypeName=gptype_name)

        # Iterate over the TaskType names
        for tasktype_name in tasktype_names:
            # Get the Rubrick object for the current task type
            rubrick = rubricks.filter(
                taskTypeID__taskType=tasktype_name).first()

            if rubrick:
                # Get the rubric percentage for the current task type
                rubrick_percentage = rubrick.percentage
            else:
                # If no rubric exists, default to 0 percentage
                rubrick_percentage = 0

            # Get the computed score per GPType and TaskType for the specific subject and student
            if tasktype_name == 'Attendance':
                # Set the attendance score to always be 100
                average_score = 100
            else:
                task_scores = Task.objects.filter(
                    taskSubject_id=subject_id,
                    studentProfileID_id=student_id,  # Filter tasks by student ID
                    gptype__gptypeName=gptype_name,
                    taskType__taskType=tasktype_name,
                ).values('score', 'overallscore')

                # Calculate the average computed score for the specific GPType and TaskType
                if task_scores.exists():
                    total_weighted_score = sum(
                        ((score['score'] / score['overallscore']) * 50) + 50
                        for score in task_scores
                    )
                    average_score = total_weighted_score / task_scores.count()
                else:
                    average_score = 0

            # Calculate the value for response_data[gptype_name][tasktype_name]

            value = average_score * (rubrick_percentage / 100)
            value_str = f'{round(value, 2)} / {rubrick_percentage} %'
            valOnly = round(value, 2)
            sumofdata[gptype_name] += valOnly

            # Add the computed score to the GPType data in the response
            response_data[gptype_name][tasktype_name] = value_str
        gpname = GPType.objects.get(gptypeName=gptype_name)
        subRub = SubjectRubrick.objects.get(
            subjectObj=subject_code_rubrick, gpObjt=gpname)
        # print(subRub.percentage)
        # print(sumofdata[gptype_name])
        res = (sumofdata[gptype_name] / 100) * subRub.percentage
        Totalvalue += res

    # Create a new dictionary with subject code as key and response data as value
    response_data = {"totalScore": Totalvalue,
                     "subjectid": subject_id, "studentid": student_id}

    student_final_grade, created = StudentFinalGrade.objects.get_or_create(
        studentprofile_id=response_data["studentid"],
        subject_id=response_data["subjectid"])
    # Update the totalGrade field
    student_final_grade.totalGrade = response_data["totalScore"]
    student_final_grade.save()

    # Return the response as JSON
    return JsonResponse(response_data)
