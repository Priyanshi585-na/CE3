from django.urls import path
from . import views


urlpatterns = [
    path('my_courses/', views.my_courses, name='my_courses'),
    path('edit_course/<str:id>/', views.edit_course, name='edit_course'),
    path('delete_course/<str:course_id>/', views.delete_course_view, name='delete_course'),
    path('record-course-content/', views.record_course_content_view, name='record_course_content'),
    path('create-engaging-course/', views.create_engaging_course_view, name='create_engaging_course'),
    path('register_course/',views.register_course,name='register_course'),
    path('admin',views.admin_view,name='admin'),
    path('delete_user/<str:user_id>/',views.delete_user,name='delete_user'),
    path('edit_course_admin/<str:course_id>/',views.edit_course_admin,name='edit_course_admin'),
    path('delete_course_admin/<str:course_id>/',views.delete_course_admin,name='delete_course_admin'),
    
]













