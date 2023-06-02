from django.contrib import admin

# Register your models here.
from .models import *


class rubrickFilter(admin.ModelAdmin):
    list_display = ['id', 'subjectID', 'taskTypeID', 'percentage']
    list_editable = ['subjectID', 'taskTypeID', 'percentage']
    search_fields = ['id', 'subjectID', 'taskTypeID', 'percentage']


class studentProfileFilter(admin.ModelAdmin):
    list_display = ['id', 'userID', 'studentNumber', 'lastName', 'firstName', 'courseID',
                    'yearID', 'genderID', 'contactNumber', 'emailAddress', 'guardianName', 'guardianNumber']
    list_editable = ['userID', 'studentNumber', 'lastName', 'firstName', 'courseID',
                     'yearID', 'genderID', 'contactNumber', 'emailAddress', 'guardianName', 'guardianNumber']
    search_fields = ['studentNumber']


class subjectFilter(admin.ModelAdmin):
    list_display = ['id', 'subjectCode', 'subjectName', 'facultyName']
    list_editable = ['subjectCode', 'subjectName', 'facultyName']
    search_fields = ['subjectCode']


class tasksFilter(admin.ModelAdmin):
    list_display = ['id', 'studentProfileID', 'task_Type', 'subjectStudent',
                    'taskSubject', 'title', 'overallscore', 'score', 'date', 'image']
    list_editable = ['studentProfileID', 'task_Type', 'taskSubject',
                     'subjectStudent', 'title', 'overallscore', 'score', 'date', 'image']
    search_fields = ['title']


class studentSubjectFilter(admin.ModelAdmin):
    list_display = ['id', 'studentProfileID', 'subjectID', 'ishide']
    list_editable = ['studentProfileID', 'subjectID', 'ishide']
    search_fields = ['id']


class taskTypeFilter(admin.ModelAdmin):
    list_display = ['id', 'taskType']
    list_editable = ['taskType']

class gpTypeFilter(admin.ModelAdmin):
    list_display = ['id','gptypeName']
    list_editable = ['gptypeName']

class cpTypeFilter(admin.ModelAdmin):
    list_display = ['id','cptypeName']
    list_editable = ['cptypeName']


class gradeperiodFilter(admin.ModelAdmin):
    list_display = ['id','subject','gptype','student','numberOfAbsences','exam','image']
    list_editable = ['subject','gptype','student','numberOfAbsences','exam','image']


class cpFilter(admin.ModelAdmin):
    list_display = ['id','title','cptype','totalScore','score','gpObject','image']
    list_editable = ['title','cptype','totalScore','score','gpObject','image']


admin.site.register(User)
admin.site.register(Course)
admin.site.register(YearLevel)
admin.site.register(Gender)
admin.site.register(Studentprofile, studentProfileFilter)
admin.site.register(Subject, subjectFilter)
admin.site.register(Task, tasksFilter)
admin.site.register(StudentSubject, studentSubjectFilter)
admin.site.register(TaskType, taskTypeFilter)
admin.site.register(Rubrick, rubrickFilter)
admin.site.register(GPType,gpTypeFilter)
admin.site.register(CPType,cpTypeFilter)
admin.site.register(GradePeriods,gradeperiodFilter)
admin.site.register(ClassPerformance,cpFilter)
