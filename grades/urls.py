from django.urls import path
from . import views

urlpatterns = [
    path('', views.grade_list, name='grade_list'),
    path('add/', views.add_grade, name='add_grade'),
    path('<int:pk>/edit/', views.edit_grade, name='edit_grade'),
    path('<int:pk>/delete/', views.delete_grade, name='delete_grade'),
    path('student/<int:student_pk>/', views.student_grades, name='student_grades'),
]
