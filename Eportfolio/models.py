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
            "subjectCode": self.subjectCode,
            "subjectName": self.subjectName,
            "facultyName": self.facultyName,
            "units": self.units,

        }


class Task(models.Model):
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


class Rubrick(models.Model):
    subjectID = models.ForeignKey(
        Subject, on_delete=CASCADE, related_name='subjectRubicks')
    taskTypeID = models.ForeignKey(
        TaskType, on_delete=CASCADE, related_name='takstypeRubicks')
    percentage = models.IntegerField(null=True)


class StudentSubject(models.Model):
    studentProfileID = models.ForeignKey(
        Studentprofile, on_delete=CASCADE, related_name="studentSubject", null=True)
    subjectID = models.IntegerField()
    ishide = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subjectID}"
