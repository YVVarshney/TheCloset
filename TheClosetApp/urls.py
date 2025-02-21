"""
URL configuration for TheClosetServer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from TheClosetApp import views
from django.urls import path, include


urlpatterns = [
    path('quiz/', views.quiz, name='quiz'),
    path('question/<int:questionId>/', views.quiz, name='quiz'),
    path('measurementQuiz/',views.measurementQuiz, name='measurementQuiz'),
    path('results/<str:bodyType>/', views.results, name='results'),
    path('submit/', views.submit_response, name='submit_response'),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
    path('feedback/', views.feedback, name='feedback'),
    path("", views.home, name='home'),    
    path("admin/", admin.site.urls),
]