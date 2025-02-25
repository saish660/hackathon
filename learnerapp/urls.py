from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lesson/<str:lesson_name>/<int:lesson_id>/', views.get_lesson, name='lesson'),
    path('profile/', views.profile, name='profile'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('quiz/<str:lesson_name>/<int:lesson_id>/', views.get_quiz, name='quiz'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('submit_quiz/<int:score>', views.submit_quiz, name='submit_quiz'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('submit_survey/', views.survey, name='survey'),
]