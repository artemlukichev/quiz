from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_task, name='add_task'),
    path('search/', views.search_task, name='search_task'),
    path('tasks/', views.task_list, name='task_list'),
    path('answer/<int:task_id>/', views.answer_task, name='answer_task'),
    path('recent/', views.recent_results, name='recent_results'),
    path('search_subject/', views.search_by_subject, name='search_by_subject'),
]
