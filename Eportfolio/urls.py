from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("studentform/", views.demographicForm, name="demographicForm"),

    path("studentprofile/<str:studentID>",
         views.studentProfile, name="studentProfile"),

    #     path("studentprofile/<str:studentID>/<str:subjectCode>",
    #          views.studentSubject, name="studentSubject"),



    path("admin/", RedirectView.as_view(url='/admin'), name="admin"),


    # ajax

    path("gendersubject/<int:subject_id>/<int:user_id>", views.get_gender_percentage_per_subject, name="genderpersub"),
    path("scholarssubject/<int:subject_id>/<int:user_id>", views.get_scholar_percentage_per_subject, name="scholarpersub"),
    
    path('test/<int:subject_id>/<int:student_id>/<int:isbar>/',
         views.get_activities_average, name='get_activitis'),

     path('totalScore/<int:subject_id>/<int:student_id>/<int:isbar>/',
         views.totalSubjectRubrick, name='get_total'),


    path("getsubjects/<str:studentNumber>",
         views.getUserSubject, name="getUserSubject"),
    path("gettask/<str:studentNumber>", views.getUserTask, name="getUserTask"),
    path("getallsubs/<str:studentNumber>",
         views.getAllSubject, name="getAllSubs"),
    path("getallprofsubs/", views.getAllProfSubject, name="getAllProfSubs"),
    path("getrubrick/<int:subjectid>",
         views.getUserRubrick, name="getUserRubrick"),
    path("getcptypes/", views.getAllCpType, name="getcpTypes"),
    path("getspecificsub/", views.getSpecificSub, name="getSpecificSub"),
    #     getSpecificSub





]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
