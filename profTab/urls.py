from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("",views.index, name="indexProf"),
    path("addSub/",views.subject,name="addsubject"),
    path("getSub/<int:subId>",views.getMySubjects,name="getsubject"),
    path('getstudents/<int:profid>/<int:subject_id>',views.getAllMyStudents,name='mystudents'),
    path('editsubject/<int:subID>',views.editSubject,name='editsub'),
    path('submiteditsubject/<int:sub_id>',views.edit_subject_form,name='editsubform')

    
    
]