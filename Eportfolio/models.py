from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.urls import reverse

# Create your models here.


class User(AbstractUser):
    isProf = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email if self.email else 'Admin'}"


class Course(models.Model):
    course = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.course}"


class TaskType(models.Model):
    taskType = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.taskType}"


class YearLevel(models.Model):
    yearLevel = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.yearLevel}"


class Gender(models.Model):
    gender = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.gender}"


class GPType(models.Model):
    gptypeName = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.gptypeName}"


class CPType(models.Model):
    cptypeName = models.CharField(max_length=100)

    def serialize(self):
        return {
            'id': self.id,
            'type': self.cptypeName
        }


class Studentprofile(models.Model):
    userID = models.ForeignKey(
        User, on_delete=CASCADE, related_name='studentProfile')
    studentNumber = models.CharField(max_length=25, blank=True)
    lastName = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    courseID = models.ForeignKey(
        Course, on_delete=CASCADE, related_name='studentCourse')
    yearID = models.ForeignKey(
        YearLevel, on_delete=CASCADE,  related_name='studentYearLevel')
    genderID = models.ForeignKey(
        Gender, on_delete=CASCADE,  related_name='studentGender')
    contactNumber = models.IntegerField()
    emailAddress = models.CharField(max_length=100)
    guardianName = models.CharField(max_length=70, default="null")
    guardianNumber = models.IntegerField()
    isScholar = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.studentNumber} : {self.lastName}, {self.firstName}"


class Subject(models.Model):
    subjectCode = models.CharField(max_length=100)
    subjectName = models.CharField(max_length=100)
    facultyName = models.ForeignKey(
        User, on_delete=CASCADE, related_name='profSubject')

    def __str__(self):
        return f"{self.subjectCode}: {self.subjectName}"

    def serialize(self, user=False):
        if user:
            is_subject_added = StudentSubject.objects.filter(
                studentProfileID=user, subjectID=self).exists()
            action_button = f'<button type="button" class="btn btn-info addSubButton" value="{self.id}"'

            if is_subject_added:
                action_button += ' disabled>Already Added</button>'
                action_button += f'<button type="button" class="btn btn-danger submodalDelete" value="{self.id}" data-toggle="modal" data-target="#subConfirmDeleteModal" style="margin-left: 5px;"> <i class="fa fa-trash"></i> </button>'
            else:
                action_button += '>Add Subject</button>'

            return {
                "id": self.id,
                "subjectCode": self.subjectCode,
                "subjectName": self.subjectName,
                "facultyName": self.facultyName.first_name,
                "action": action_button
            }
        else:
            return {
                "id": self.id,
                "subjectCode": self.subjectCode,
                "subjectName": self.subjectName,
                "facultyName": self.facultyName.first_name,
                "action": f'<button type="button" class="btn btn-danger modaldelete" value="{self.id}" name="taskDelete"data-toggle="modal" data-target="#confirmDeleteModal" > <i class="fa fa-trash"></i> </button> <button type="button" class="btn btn-info editSub" data-toggle="modal" data-target="#editSubjetModal" id = {self.pk} subjectcode= "{self.subjectCode}" subjectname = "{self.subjectName}" > <i class="fa fa-edit"></i> </button>'
            }


class StudentSubject(models.Model):
    studentProfileID = models.ForeignKey(
        Studentprofile, on_delete=CASCADE, related_name="studentSubject", null=True)
    subjectID = models.ForeignKey(
        Subject, on_delete=CASCADE, related_name='StudentSubject', null=True)
    ishide = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.studentProfileID.studentNumber}: {self.subjectID.subjectName}"

    def serialize(self):
        return {
            "StudentName": self.studentProfileID.firstName,
            "StudentSurname": self.studentProfileID.lastName,
            "StudentNumber": f'<a href="{reverse("studentProfile", args=[self.studentProfileID.studentNumber])}"  target="_blank">{self.studentProfileID.studentNumber}</a>',
            "YearLevel": self.studentProfileID.yearID.yearLevel,
            "Course": self.studentProfileID.courseID.course,
        }


class Task(models.Model):
    studentProfileID = models.ForeignKey(
        Studentprofile, on_delete=CASCADE, related_name="studentTask", null=True)
    studentsubject = models.ForeignKey(
        StudentSubject, on_delete=CASCADE, related_name="studentSub", null=True)
    taskSubject = models.ForeignKey(
        Subject, on_delete=CASCADE, related_name="subjectTask", null=True)
    gptype = models.ForeignKey(
        GPType, on_delete=CASCADE, related_name='taskGPType' , null=True)
    taskType = models.ForeignKey(
        TaskType,  on_delete=CASCADE,db_constraint=False, related_name='UsertaskType', null=True)
    title = models.CharField(max_length=100)
    overallscore = models.IntegerField()
    score = models.IntegerField()
    date = models.DateField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return f"{self.title}"

    def serialize(self):
        return {
            "title": self.title,
            "score": self.score,
            "cptype": self.taskType.taskType,
            "gptype": self.gptype.gptypeName,
            "overallscore": self.overallscore,
            "date": self.date,
            "subject": self.taskSubject.subjectCode + ": " + self.taskSubject.subjectName,
            "image": self.image.url if self.image else None,
            "action": f'<button type="button" class="btn btn-danger modaldelete" value="{self.id}" data-toggle="modal" data-target="#confirmDeleteModal"  > <i class="fa fa-trash"></i> </button> <button type="button" class="btn btn-info EditTask" data-toggle="modal" data-target="#actionModify" title="{self.title}" score="{self.score}" overall="{self.overallscore}" date="{self.date}"  id = {self.pk} > <i class="fa fa-edit"></i> </button>'
        }


class GradePeriods(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=CASCADE, related_name='GPSubject')
    gptype = models.ForeignKey(
        GPType, on_delete=CASCADE, related_name="GPType")
    numberOfAbsences = models.IntegerField(default=0)
    projectTotal = models.IntegerField(null=True)
    exam = models.IntegerField()

    def __str__(self):
        return f'{self.gptype.gptypeName}:{self.subject.subjectCode}'
    


class ClassPerformance(models.Model):
    title = models.CharField(max_length=100)
    cptype = models.ForeignKey(
        CPType, on_delete=CASCADE, related_name='CPtype')
    totalScore = models.IntegerField()
    gpObject = models.ForeignKey(
        GradePeriods, on_delete=CASCADE, related_name='CPgradepoint')


class Rubrick(models.Model):
    gpObjt = models.ForeignKey(
        GradePeriods, on_delete=CASCADE, related_name='gpRubrick', null=True)
    taskTypeID = models.ForeignKey(
        TaskType, on_delete=CASCADE, related_name='typeRubicks')
    percentage = models.IntegerField(null=True)



    def serialize(self, isprof=0):
        if isprof:
            return {
                "id": self.id,
                "taskID": self.taskTypeID_id,
                "taskName": self.taskTypeID.taskType.lower()+"Edit",
                "percentage": self.percentage
            }
        return {
            "id": self.id,
            "taskID": self.taskTypeID_id,
            "taskName": self.taskTypeID.taskType,
        }


class SubjectRubrick(models.Model):
    subjectObj = models.ForeignKey(
        Subject, on_delete=CASCADE, related_name='subjectRub')
    gpObjt = models.ForeignKey(
        GPType, on_delete=CASCADE, related_name='subGpRubrick', null=True)
    percentage = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.subjectObj.subjectCode}:{self.subjectObj.subjectName}({self.gpObjt.gptypeName}) = {self.percentage}"