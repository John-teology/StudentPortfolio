from django.contrib import admin

# Register your models here.
from .models import *

class rubrickFilter(admin.ModelAdmin):
    list_display = ['id','subjectID','taskTypeID','percentage']
    list_editable = ['subjectID','taskTypeID','percentage']
    search_fields = ['id','subjectID','taskTypeID','percentage']

class studentProfileFilter(admin.ModelAdmin):
    list_display = ['id','userID','studentNumber','lastName','firstName','courseID','yearID','genderID','contactNumber','emailAddress','guardianName','guardianNumber']
    list_editable = ['userID','studentNumber','lastName','firstName','courseID','yearID','genderID','contactNumber','emailAddress','guardianName','guardianNumber']
    search_fields = ['studentNumber']

class subjectFilter(admin.ModelAdmin):
    list_display = ['id','subjectCode','subjectName', 'facultyName','units']
    list_editable = ['subjectCode','subjectName', 'facultyName','units']
    search_fields = ['subjectCode']

class tasksFilter(admin.ModelAdmin):
    list_display=['id','studentProfileID','task_Type','subjectStudent','taskSubject','title','overallscore','score','date','image']
    list_editable=['studentProfileID','task_Type','taskSubject','subjectStudent','title','overallscore','score','date','image']
    search_fields = ['title']

class studentSubjectFilter(admin.ModelAdmin):
    list_display = ['id','studentProfileID','subjectID' ,'ishide']
    list_editable = ['studentProfileID','subjectID' ,'ishide']
    search_fields = ['id']





admin.site.register(User)
admin.site.register(Course)
admin.site.register(YearLevel)
admin.site.register(Gender)
admin.site.register(Studentprofile,studentProfileFilter)
admin.site.register(Subject,subjectFilter)
admin.site.register(Task,tasksFilter)
admin.site.register(StudentSubject,studentSubjectFilter)
admin.site.register(TaskType)
admin.site.register(Rubrick,rubrickFilter)



