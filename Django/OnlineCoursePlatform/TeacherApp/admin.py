from django.contrib import admin
from .models import Course  

class CourseAdmin(admin.ModelAdmin):
    list_display = ('id','is_draft', 'course_image', 'course_videos') 
admin.site.register(Course,CourseAdmin)    