from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("studentform/",views.demographicForm, name="demographicForm"),
    path("studentprofile/<str:studentID>",views.studentProfile,name="studentProfile"),
    path("studentprofile/<str:studentID>/<str:subjectCode>",views.studentSubject,name="studentSubject"),
    path("siteadmin",views.adminSite,name="adminsite"),
    path("admin/", RedirectView.as_view(url='/admin'),name="admin"),
    path("about/", views.about, name= "aboutpage"),
    path("overview/", views.overview, name= "overviewpage"),
    path("contact/", views.contact, name= "contactpage"),   
    path("dashboard/", views.dashboard, name= "dashboard"),
    # path("landing/", views.landing, name= "landingpage"),
    # path("login/", views.login, name="loginpage"),   

    
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)