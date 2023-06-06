from django.contrib import admin

# Register your models here.
from .models import *


class rubrickFilter(admin.ModelAdmin):
    list_display = ['id', 'gpObjt', 'taskTypeID', 'percentage']
    list_editable = ['gpObjt', 'taskTypeID', 'percentage']
    search_fields = ['id', 'gpObjt', 'taskTypeID', 'percentage']


class studentProfileFilter(admin.ModelAdmin):
    list_display = ['id', 'userID', 'studentNumber', 'lastName', 'firstName', 'courseID', 'isScholar',
                    'yearID', 'genderID', 'contactNumber', 'emailAddress', 'guardianName', 'guardianNumber']
    list_editable = ['userID', 'studentNumber', 'lastName', 'firstName', 'courseID',
                     'yearID', 'genderID', 'contactNumber', 'emailAddress', 'guardianName', 'guardianNumber', 'isScholar']
    search_fields = ['studentNumber']


class subjectFilter(admin.ModelAdmin):
    list_display = ['id', 'subjectCode', 'subjectName', 'facultyName']
    list_editable = ['subjectCode', 'subjectName', 'facultyName']
    search_fields = ['subjectCode']


class tasksFilter(admin.ModelAdmin):
    list_display = ['id', 'studentProfileID', 'gptype', 'taskType',
                    'taskSubject', 'title', 'overallscore', 'score', 'date', 'image']
    list_editable = ['studentProfileID', 'gptype', 'taskType', 'taskSubject',
                     'title', 'overallscore', 'score', 'date', 'image']
    search_fields = ['title']


class studentSubjectFilter(admin.ModelAdmin):
    list_display = ['id', 'studentProfileID', 'subjectID', 'ishide']
    list_editable = ['studentProfileID', 'subjectID', 'ishide']
    search_fields = ['id']


class taskTypeFilter(admin.ModelAdmin):
    list_display = ['id', 'taskType']
    list_editable = ['taskType']


class gpTypeFilter(admin.ModelAdmin):
    list_display = ['id', 'gptypeName']
    list_editable = ['gptypeName']


class cpTypeFilter(admin.ModelAdmin):
    list_display = ['id', 'cptypeName']
    list_editable = ['cptypeName']


class gradeperiodFilter(admin.ModelAdmin):
    list_display = ['id', 'subject', 'gptype',
                    'numberOfAbsences', 'exam', 'projectTotal']
    list_editable = ['subject', 'gptype',
                     'numberOfAbsences', 'exam', 'projectTotal']


class cpFilter(admin.ModelAdmin):
    list_display = ['id', 'title', 'cptype', 'totalScore', 'gpObject']
    list_editable = ['title', 'cptype', 'totalScore', 'gpObject']


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
admin.site.register(GPType, gpTypeFilter)
admin.site.register(CPType, cpTypeFilter)
admin.site.register(GradePeriods, gradeperiodFilter)
admin.site.register(ClassPerformance, cpFilter)
admin.site.register(SubjectRubrick)
