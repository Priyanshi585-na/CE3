from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Course
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
import requests
import uuid


REGISTER_API_URL = 'http://127.0.0.1:5000/registerapi'
LOGIN_API_URL = 'http://127.0.0.1:5000/loginapi'
AVAILABLE_COURSES_API_URL = 'http://127.0.0.1:5000/availablecoursesapi'
COURSES_API_URL = 'http://127.0.0.1:5000/coursesapi'
FEEDBACK_API_URL = 'http://127.0.0.1:5000/feedbackapi'


courses_all = requests.get(COURSES_API_URL).json()
course_one = courses_all.get('courses')

all_feedback=requests.get(FEEDBACK_API_URL).json()
feedback=all_feedback.get('feedback')

all_user=requests.get(REGISTER_API_URL).json()
users=all_user.get('users')

available_courses = requests.get(AVAILABLE_COURSES_API_URL).json()    
courses = available_courses.get('courses')                            
course_names = [course.get("name") for course in courses]



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



def register_course(request):
    context = get_user_role_context(request)
    categories = course_names  
    context['categories'] = categories
    username = request.session.get('username')

    if request.method == 'POST':
        name = request.POST.get('name')
        course_image = request.FILES.get('image')
        description = request.POST.get('description')
        category = request.POST.get('category')
        difficulty = request.POST.get('difficulty')
        price = request.POST.get('price')
        duration = request.POST.get('duration')
        course_video = request.FILES.get('video')
        uuid_value = str(uuid.uuid4())  

        data = {
            'id': uuid_value, 
            'name': name,
            'description': description,
            'category': category,
            'difficulty': difficulty,
            'price': price,
            'duration': duration,
            'created_by': username,
        }

        course = Course.objects.create(
            id=uuid.UUID(uuid_value), 
            course_image=course_image,
            course_videos=course_video,
            is_draft=True if 'save_to_drafts' in request.POST else False,  
        )
        course.save()

        try:
            response = requests.post(COURSES_API_URL, json=data)  # Sending to Flask
            response.raise_for_status()
            if response.status_code == 201:
                messages.success(request, 'Course created successfully!')
                return redirect('my_courses')
            else:
                error_data = response.json()
                error_message = error_data.get('message', f'Failed to create course. Status code: {response.status_code}')
                messages.error(request, error_message)
                return render(request, 'register_course.html', context)
        except requests.exceptions.RequestException as e:
            messages.error(request, f'Error: {e}')
            return render(request, 'register_course.html', context)

    return render(request, 'register_course.html', context)


def my_courses(request):
    context = {}
    username = request.session.get('username')
    all_courses_response = requests.get(COURSES_API_URL).json()
    all_courses = all_courses_response.get('courses')
    my_courses = [course for course in all_courses if course['created_by'] == username]

    published_courses = []
    drafted_courses = []

    for course_dict in my_courses:
        try:
            course_from_db = Course.objects.get(id=course_dict['id'])
            updated_course_dict = course_dict.copy()
            updated_course_dict['image'] = course_from_db.course_image
            updated_course_dict['is_draft'] = course_from_db.is_draft 
            updated_course_dict['video'] = course_from_db.course_videos

            if updated_course_dict['is_draft'] == True:
                drafted_courses.append(updated_course_dict)
            else:
                published_courses.append(updated_course_dict)

        except Course.DoesNotExist:
            published_courses.append(course_dict)  

    context['courses'] = published_courses 
    context['drafted_courses'] = drafted_courses 
    return render(request, 'my_courses.html', context)


def edit_course(request, id):
    context = {}
    context = get_user_role_context(request)
    username = request.session.get('username')
    course = get_object_or_404(Course, id=id)
    categories = [course for course in course_names]
    context['categories'] = categories
    all_courses_response_url = f"{COURSES_API_URL}/{id}"
    all_courses_response = requests.get(all_courses_response_url)
    all_courses_response.raise_for_status()
    this_course = all_courses_response.json().get('course')  
    this_course['image'] = course.course_image if course.course_image else None
    this_course['video'] = course.course_videos if course.course_videos else None 


    context['course'] = this_course

    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        category_name = request.POST.get('category')
        difficulty = request.POST.get('difficulty')
        price = request.POST.get('price')
        duration = request.POST.get('duration')
        video = request.FILES.get('video')
        is_draft = 'save_to_drafts' in request.POST

        api_url = f"{COURSES_API_URL}/{id}"
        data = {
            'name': name,
            'description': description,
            'category': category_name,
            'difficulty': difficulty,
            'price': price,
            'duration': duration,
            'created_by': username,
        }

        course.is_draft = is_draft
        if image:
            course.course_image = image
        if video:
            course.course_videos = video
        course.save()  

        try:
            response = requests.put(api_url, json=data)
            response.raise_for_status()
            messages.success(request, f"Course '{name}' updated successfully!")
            return redirect('my_courses')

        except requests.exceptions.RequestException as e:
            try:
                error_data = response.json()
                error_message = f"API Error: {error_data.get('detail', str(e))}"
            except:
                error_message = f"API Error: {e}"
            messages.error(request, error_message)
            return render(request, 'edit_course.html', context)

    else:
        return render(request, 'edit_course.html', context)


def delete_course_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    api_url = f"{COURSES_API_URL}/{course_id}"
    headers = {}

    try:
        response = requests.delete(api_url, headers=headers)
        response.raise_for_status() 

        if response.status_code == 200 or response.status_code == 204:
            course.delete() 
            messages.success(request, f"Course deleted successfully!")
        else:
            error_data = response.json()
            error_message = f"API Error: {error_data.get('detail', 'Failed to delete course in Flask.')}"
            messages.error(request, error_message)
        
    except requests.exceptions.RequestException as e:
        messages.error(request, f"API Error: {e}")

    return redirect('my_courses')

def record_course_content_view(request):
    context = get_user_role_context(request)
    return render(request, 'record_course_content.html', context)


def create_engaging_course_view(request):
    context = get_user_role_context(request)
    return render(request, 'create_engaging_course.html', context)



def admin_view(request):
    context = get_user_role_context(request)
    context['all_courses']=course_one
    context['course_names']=courses
    context['feedback']=feedback
    context['users']=users
    context['user']=request.user
    return render(request, 'admin_dashboard.html',context)


def delete_user(request,user_id):
      api_url = f"{COURSES_API_URL}/{user_id}"
      headers = {}
  
      try:
          response = requests.delete(api_url, headers=headers)
          response.raise_for_status() 
  
          if response.status_code == 200 or response.status_code == 204:
              messages.success(request, f"Course deleted successfully!")
          else:
              error_data = response.json()
              error_message = f"API Error: {error_data.get('detail', 'Failed to delete course in Flask.')}"
              messages.error(request, error_message)
          
      except requests.exceptions.RequestException as e:
          messages.error(request, f"API Error: {e}")
  
      return redirect('admin')
  
  
  
def edit_course_admin(request, course_id):
    context = {}
    context = get_user_role_context(request)
    username = request.session.get('username')
    course = get_object_or_404(Course, id=course_id)
    categories = [course for course in course_names]
    context['categories'] = categories
    all_courses_response_url = f"{COURSES_API_URL}/{course_id}"
    all_courses_response = requests.get(all_courses_response_url)
    all_courses_response.raise_for_status()
    this_course = all_courses_response.json().get('course')  
    this_course['image'] = course.course_image if course.course_image else None
    this_course['video'] = course.course_videos if course.course_videos else None 
    context['course'] = this_course

    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        category_name = request.POST.get('category')
        difficulty = request.POST.get('difficulty')
        price = request.POST.get('price')
        duration = request.POST.get('duration')
        video = request.FILES.get('video')
        is_draft = 'save_to_drafts' in request.POST

        api_url = f"{COURSES_API_URL}/{course_id}"
        data = {
            'name': name,
            'description': description,
            'category': category_name,
            'difficulty': difficulty,
            'price': price,
            'duration': duration,
            'created_by': username,
        }

        course.is_draft = is_draft
        if image:
            course.course_image = image
        if video:
            course.course_videos = video
        course.save()  

        try:
            response = requests.put(api_url, json=data)
            response.raise_for_status()
            messages.success(request, f"Course '{name}' updated successfully!")
            return redirect('admin')

        except requests.exceptions.RequestException as e:
            try:
                error_data = response.json()
                error_message = f"API Error: {error_data.get('detail', str(e))}"
            except:
                error_message = f"API Error: {e}"
            messages.error(request, error_message)
            return render(request, 'edit_course.html', context)

    else:
        return render(request, 'edit_course.html', context)
    
@login_required    
def delete_course_admin(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    api_url = f"{COURSES_API_URL}/{course_id}"
    headers = {}

    try:
        response = requests.delete(api_url, headers=headers)
        response.raise_for_status() 

        if response.status_code == 200 or response.status_code == 204:
            course.delete() 
            messages.success(request, f"Course deleted successfully!")
        else:
            error_data = response.json()
            error_message = f"API Error: {error_data.get('detail', 'Failed to delete course.')}"
            messages.error(request, error_message)
        
    except requests.exceptions.RequestException as e:
        messages.error(request, f"API Error: {e}")
        
        
