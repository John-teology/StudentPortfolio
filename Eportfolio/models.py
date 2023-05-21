from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE

# Create your models here.


class User(AbstractUser):
    isProf = models.BooleanField(default=False)


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

    def __str__(self):
        return f"{self.studentNumber} : {self.lastName}, {self.firstName}"


class Subject(models.Model):
    subjectCode = models.CharField(max_length=100, unique=True)
    subjectName = models.CharField(max_length=100)
    facultyName = models.CharField(max_length=100)
    units = models.IntegerField()

    def __str__(self):
        return f"{self.subjectCode}: {self.subjectName}"

    def serialize(self):
        return {
            "id": self.id,
            "subjectCode": self.subjectCode,
            "subjectName": self.subjectName,
            "facultyName": self.facultyName,
            "units": self.units,
            "action" : f'<button type="button" class="btn btn-info addSubButton" value="{self.id}"> Add Subject </button>'

        }


class Task(models.Model):
    studentProfileID = models.ForeignKey(
        Studentprofile, on_delete=CASCADE, related_name="studentTask", null=True)
    task_Type = models.ForeignKey(
        TaskType, on_delete=CASCADE, related_name="TypeofTask", null=True)
    taskSubject = models.ForeignKey(
        Subject, on_delete=CASCADE, related_name="subjectTask")
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
            "overallscore": self.overallscore,
            "date": self.date,
            "taskType": self.task_Type.taskType,
            "subject": self.taskSubject.subjectCode + ": " + self.taskSubject.subjectName,
            "image": self.image.url if self.image else None,
            "action": f'<button type="button" class="btn btn-danger deleteTask" value="{self.id}" name="taskDelete" > <i class="fa fa-trash"></i> </button> <button type="button" class="btn btn-info EditTask" data-toggle="modal" data-target="#actionModify" title="{self.title}" score="{self.score}" overall="{self.overallscore}" date="{self.date}" subject={self.taskSubject_id} subType={self.task_Type_id} id = {self.pk} > <i class="fa fa-edit"></i> </button>'
        }


class Rubrick(models.Model):
    subjectID = models.ForeignKey(
        Subject, on_delete=CASCADE, related_name='subjectRubicks')
    taskTypeID = models.ForeignKey(
        TaskType, on_delete=CASCADE, related_name='takstypeRubicks')
    percentage = models.IntegerField(null=True)

    def serialize(self):
        return {
            "id": self.id,
            "taskID": self.taskTypeID_id,
            "taskName": self.taskTypeID.taskType,
        }


class StudentSubject(models.Model):
    studentProfileID = models.ForeignKey(
        Studentprofile, on_delete=CASCADE, related_name="studentSubject", null=True)
    subjectID = models.ForeignKey(
        Subject, on_delete=CASCADE, related_name='StudentSubject', null=True)
    ishide = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.studentProfileID.studentNumber}: {self.subjectID.subjectName}"
