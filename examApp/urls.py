from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('exams/', views.exams, name='exams'),
    path('podcast/', views.podcast, name='podcast'),
    path('review/', views.review, name='review'),
    path('leaderboards/', views.leaderboards, name='leaderboards'),
    path('sections/<str:exam_uuid>/', views.sections, name='sections'),
    path('items/<str:section_uuid>/', views.items, name='items'),
    path('quiz/<str:section_uuid>/', views.quizzes, name='quizzes'),
]