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
    

admin.site.register(User)
admin.site.register(Course)
admin.site.register(YearLevel)
admin.site.register(Gender)
admin.site.register(Studentprofile,studentProfileFilter)
admin.site.register(Subject)
admin.site.register(Task)
admin.site.register(TaskType)
admin.site.register(Rubrick,rubrickFilter)



