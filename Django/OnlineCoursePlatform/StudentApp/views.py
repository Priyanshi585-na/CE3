from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from TeacherApp.models import Course
import requests
from .models import Enrolled_Course


REGISTER_API_URL = 'http://127.0.0.1:5000/registerapi'
LOGIN_API_URL = 'http://127.0.0.1:5000/loginapi'
AVAILABLE_COURSES_API_URL = 'http://127.0.0.1:5000/availablecoursesapi'
COURSES_API_URL = 'http://127.0.0.1:5000/coursesapi'
FEEDBACK_API_URL = 'http://127.0.0.1:5000/feedbackapi'



courses_all = requests.get(COURSES_API_URL).json()
course_one = courses_all.get('courses')



def get_user_role_context(request):
    context = {}
    jwt_token = request.session.get('jwt_token')
    username = request.session.get('username')
    if jwt_token:
        headers = {'Authorization':f"Bearer {jwt_token}","Content-Type": "application/json"}
        users_details_response = requests.get(REGISTER_API_URL,headers=headers)
        users_details_response.raise_for_status()
        if users_details_response.status_code == 200:
          users_details = users_details_response.json().get('users')
          for users in users_details:
              if users['username'] == username and users['role']=='Teacher':
                    context['show_teacher_center']=True    
              elif request.user.is_superuser:
                    context['show_admin_center'] = True
                    context['show_teacher_center'] = True
    return context

@login_required
def pay_view(request,course_id):
    context = get_user_role_context(request)
    context['course_id']=course_id
    return render(request,'pay.html', context)

@login_required
def cancel_view(request):
    context = get_user_role_context(request)
    return render(request,'cancel.html', context)

def web_development_view(request):
    context = get_user_role_context(request)
    web_courses = [course for course in course_one if course.get('category')=="Web Development"]
    published_courses = []
    for course_dict in web_courses:
            course_from_db = Course.objects.get(id=course_dict['id'])
            updated_course_dict = course_dict.copy()
            updated_course_dict['image'] = course_from_db.course_image
            updated_course_dict['is_draft'] = course_from_db.is_draft 
            updated_course_dict['video'] = course_from_db.course_videos
            updated_course_dict['enrolled']=course_from_db.enrolled
            
            if updated_course_dict['is_draft'] == False:
                published_courses.append(updated_course_dict)
           
    enroll = Enrolled_Course.objects.filter(user=request.user).values_list('name',flat=True)
    context['enroll']=enroll
    context['web_dev_courses'] = published_courses
    return render(request, 'webdevelopmentcourse.html',context)

def ai(request):
    context = get_user_role_context(request)
    ai_courses = [course for course in course_one if course.get('category')=="AI Engineering"]
    
    published_courses = []
    
    for course_dict in ai_courses:
            course_from_db = Course.objects.get(id=course_dict['id'])
            updated_course_dict = course_dict.copy()
            updated_course_dict['image'] = course_from_db.course_image
            updated_course_dict['is_draft'] = course_from_db.is_draft 
            updated_course_dict['video'] = course_from_db.course_videos
            updated_course_dict['enrolled']=course_from_db.enrolled
            
            if updated_course_dict['is_draft'] == False:
                published_courses.append(updated_course_dict)
           
    enroll = Enrolled_Course.objects.filter(user=request.user).values_list('name',flat=True)
    context['enroll']=enroll
    context['ai_courses'] = published_courses
    return render(request,'aicourse.html', context)

def data_science(request):
    context = get_user_role_context(request)
    data_science_courses = [course for course in course_one if course.get('category')=="Data Science"]
    
    published_courses = []
    
    for course_dict in data_science_courses:
            course_from_db = Course.objects.get(id=course_dict['id'])
            updated_course_dict = course_dict.copy()
            updated_course_dict['image'] = course_from_db.course_image
            updated_course_dict['is_draft'] = course_from_db.is_draft 
            updated_course_dict['video'] = course_from_db.course_videos
            updated_course_dict['enrolled']=course_from_db.enrolled
            
            if updated_course_dict['is_draft'] == False:
                published_courses.append(updated_course_dict)
           
    enroll = Enrolled_Course.objects.filter(user=request.user).values_list('name',flat=True)
    context['enroll']=enroll
    context['data_science_courses'] = published_courses
    return render(request, 'datasciencecourse.html', context)

def cpp(request):
    context = get_user_role_context(request)
    cpp_courses = [course for course in course_one if course.get('category')=="C++"]
    
    published_courses = []
    
    for course_dict in cpp_courses:
            course_from_db = Course.objects.get(id=course_dict['id'])
            updated_course_dict = course_dict.copy()
            updated_course_dict['image'] = course_from_db.course_image
            updated_course_dict['is_draft'] = course_from_db.is_draft 
            updated_course_dict['video'] = course_from_db.course_videos
            updated_course_dict['enrolled']=course_from_db.enrolled
            
            if updated_course_dict['is_draft'] == False:
                published_courses.append(updated_course_dict)
           
    enroll = Enrolled_Course.objects.filter(user=request.user).values_list('name',flat=True)
    context['enroll']=enroll
    context['cpp_courses'] = published_courses
    return render(request, 'cppcourse.html', context)


def excel(request):
    context = get_user_role_context(request)
    sql_courses = [course for course in course_one if course.get('category')=="SQL"]
    
    published_courses = []
    
    for course_dict in sql_courses:
            course_from_db = Course.objects.get(id=course_dict['id'])
            updated_course_dict = course_dict.copy()
            updated_course_dict['image'] = course_from_db.course_image
            updated_course_dict['is_draft'] = course_from_db.is_draft 
            updated_course_dict['video'] = course_from_db.course_videos
            updated_course_dict['enrolled']=course_from_db.enrolled
            
            if updated_course_dict['is_draft'] == False:
                published_courses.append(updated_course_dict)
           
    enroll = Enrolled_Course.objects.filter(user=request.user).values_list('name',flat=True)
    context['enroll']=enroll
    context['sql_courses'] = published_courses
    return render(request, 'sqlcourse.html', context) 


def python(request):
    context = get_user_role_context(request)
    python_courses = [course for course in course_one if course.get('category')=="Python"]
    
    published_courses = []
    
    for course_dict in python_courses:
            course_from_db = Course.objects.get(id=course_dict['id'])
            updated_course_dict = course_dict.copy()
            updated_course_dict['image'] = course_from_db.course_image
            updated_course_dict['is_draft'] = course_from_db.is_draft 
            updated_course_dict['video'] = course_from_db.course_videos
            updated_course_dict['enrolled']=course_from_db.enrolled
            
            if updated_course_dict['is_draft'] == False:
                published_courses.append(updated_course_dict)
           
    enroll = Enrolled_Course.objects.filter(user=request.user).values_list('name',flat=True)
    context['enroll']=enroll
    context['python_courses'] = published_courses
    return render(request,'pythoncourse.html', context)

def java(request):
    context = get_user_role_context(request)
    java_courses = [course for course in course_one if course.get('category')=="Java"]
    
    published_courses = []
    
    for course_dict in java_courses:
            course_from_db = Course.objects.get(id=course_dict['id'])
            updated_course_dict = course_dict.copy()
            updated_course_dict['image'] = course_from_db.course_image
            updated_course_dict['is_draft'] = course_from_db.is_draft 
            updated_course_dict['video'] = course_from_db.course_videos
            updated_course_dict['enrolled']=course_from_db.enrolled
            
            if updated_course_dict['is_draft'] == False:
                published_courses.append(updated_course_dict)
           
    enroll = Enrolled_Course.objects.filter(user=request.user).values_list('name',flat=True)
    context['enroll']=enroll
    context['java_courses'] = published_courses
    return render(request, 'javacourse.html', context)

def game(request):
    context = get_user_role_context(request)
    game_development_courses =[course for course in course_one if course.get('category')=="Game Development"]
    
    published_courses = []
    
    for course_dict in game_development_courses:
            course_from_db = Course.objects.get(id=course_dict['id'])
            updated_course_dict = course_dict.copy()
            updated_course_dict['image'] = course_from_db.course_image
            updated_course_dict['is_draft'] = course_from_db.is_draft 
            updated_course_dict['video'] = course_from_db.course_videos
            updated_course_dict['enrolled']=course_from_db.enrolled
            
            if updated_course_dict['is_draft'] == False:
                published_courses.append(updated_course_dict)
           
    enroll = Enrolled_Course.objects.filter(user=request.user).values_list('name',flat=True)
    context['enroll']=enroll
    context['game_development_courses'] = published_courses
    return render(request, 'gamedevcourse.html', context)

def my_learning_view(request):
    context = get_user_role_context(request)
    enrollments = Enrolled_Course.objects.filter(user=request.user)
    context['enrollments']=enrollments
    return render(request,'my_learning.html',context) 

def enroll(request,course_id):
     url = f"{COURSES_API_URL}/{course_id}"
     course_response = requests.get(url).json()
     this_course = course_response.get('course')
     course = Course.objects.get(id = course_id)
     
     
     enrollments = Enrolled_Course.objects.create(
         name = this_course['name'],
         description = this_course['description'],
         created_by = this_course['created_by'],
         user = request.user.username,
         image= course.course_image
     )
     enrollments.save()
     
     course.enrolled=True
     course.save()
     return redirect('home')