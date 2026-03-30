"""elearning_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import (
    login_view, register, logout_view, dashboard, 
    create_college, create_admin, create_faculty, 
    create_branch, provision_student, student_results,
    admin_students, admin_courses
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('', login_view), # Keep root accessible as well
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create-college/', create_college, name='create_college'),
    path('create-admin/', create_admin, name='create_admin'),
    path('create-faculty/', create_faculty, name='create_faculty'),
    path('create-branch/', create_branch, name='create_branch'),
    path('provision-student/', provision_student, name='provision_student'),
    path('results/', student_results, name='student_results'),
    path('admin-students/', admin_students, name='admin_students'),
    path('admin-courses/', admin_courses, name='admin_courses'),
    path('courses/', include('courses.urls')),
    path('quiz/', include('quiz.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
