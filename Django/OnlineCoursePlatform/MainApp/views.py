from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests
from TeacherApp.models import Course
from StudentApp.models import Enrolled_Course
import uuid

REGISTER_API_URL = 'http://127.0.0.1:5000/registerapi'
LOGIN_API_URL = 'http://127.0.0.1:5000/loginapi'
AVAILABLE_COURSES_API_URL = 'http://127.0.0.1:5000/availablecoursesapi'
COURSES_API_URL = 'http://127.0.0.1:5000/coursesapi'
FEEDBACK_API_URL = 'http://127.0.0.1:5000/feedbackapi'


available_courses = requests.get(AVAILABLE_COURSES_API_URL).json()    
courses = available_courses.get('courses')                            
course_names = [course.get("name") for course in courses]             

courses_all = requests.get(COURSES_API_URL).json()
course_one = courses_all.get('courses')

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        preferred_field = request.POST.getlist('preferred_field')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        gender = request.POST.get('gender')
        role = request.POST.get('role')
        linkedin = request.POST.get('linkedin')
        experience = request.POST.get('experience')
        profile_image = request.FILES.get('profile')
        uuid_id = str(uuid.uuid4()) 

        data = {
            'id': uuid_id, 
            'name': name,
            'username': username,
            'email': email,
            'mobile': mobile,
            'preferred_field': preferred_field,
            'password': password,
            'confirm_password': cpassword,
            'gender': gender,
            'role': role,
            'linkedin': linkedin,
            'experience': experience
        }

        response = requests.post(REGISTER_API_URL, json=data)
        if response.status_code == 201:
            try:
                profile = UserProfile.objects.create(id=uuid.UUID(uuid_id), profile_image=profile_image)
                profile.save()

                user = User.objects.create(username=username, email=email)
                user.set_password(password)
                user.save()
                messages.success(request, 'Registration successful')
                return redirect('login')
            except Exception as e:
                messages.error(request, f"Error creating user or profile: {e}")
                return render(request, 'register.html', {'course_names': course_names})

        else:
            error_data = response.json()
            messages.error(request, error_data.get('message', f'Registration failed on the server (status code: {response.status_code}).'))

    return render(request, 'register.html', {'course_names': course_names})      
                


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        login_data = {
            "username": username,
            "password": password
        }

        login_response = requests.post(LOGIN_API_URL, json=login_data)
        if login_response.status_code == 200:
            jwt_token = login_response.json().get('access_token')
            request.session['jwt_token'] = jwt_token
            request.session['username'] = username
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                messages.success(request, 'Login successful!')
                return redirect('home') 
            else:
                messages.error(request,'Login Failed! Please try again')
        else:
            error_data = login_response.json()
            messages.error(request, error_data.get('message', f'Login failed: {login_response.status_code}'))
    return render(request, 'login.html')


def contact_view(request):
    if request.method =='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        data={
            'name':name,
            'email':email,
            'message':message
        }
        response=requests.post(FEEDBACK_API_URL,json=data)
        response.raise_for_status()
        if response.status_code==201:
                messages.success(request,'Feedback given successfully')
                return redirect('review')
        else:           
              error_data=response.json()
              messages.error(request, error_data.get('message', f'Feedback failed: {response.status_code}'))
    return render(request,'contact.html')

def review(request):
    return render(request,'review.html')

def web_development(request):
    web_courses = [course for course in course_one if course.get('category')=="Web Development"]
    
    published_courses = []
    
    for course_dict in web_courses:
            course_from_db = Course.objects.get(id=course_dict['id'])
            updated_course_dict = course_dict.copy()
            updated_course_dict['image'] = course_from_db.course_image
            updated_course_dict['is_draft'] = course_from_db.is_draft 
            updated_course_dict['video'] = course_from_db.course_videos
            
            if updated_course_dict['is_draft'] == False:
                published_courses.append(updated_course_dict)
                
    return render(request, 'web_development.html',{'web_courses':published_courses})


def ai_view(request):
    ai_courses = [course for course in course_one if course.get('category')=="AI Engineering"]
    
    published_courses = []
    
    for course_dict in ai_courses:
            course_from_db = Course.objects.get(id=course_dict['id'])
            updated_course_dict = course_dict.copy()
            updated_course_dict['image'] = course_from_db.course_image
            updated_course_dict['is_draft'] = course_from_db.is_draft 
            updated_course_dict['video'] = course_from_db.course_videos
            
            if updated_course_dict['is_draft'] == False:
                published_courses.append(updated_course_dict)
    
    return render(request,'ai.html',{"ai_courses":published_courses})


def data_science_view(request):
     data_science_courses = [course for course in course_one if course.get('category')=="Data Science"]
     
     published_courses = []
    
     for course_dict in data_science_courses:
            course_from_db = Course.objects.get(id=course_dict['id'])
            updated_course_dict = course_dict.copy()
            updated_course_dict['image'] = course_from_db.course_image
            updated_course_dict['is_draft'] = course_from_db.is_draft 
            updated_course_dict['video'] = course_from_db.course_videos
            
            if updated_course_dict['is_draft'] == False:
                published_courses.append(updated_course_dict)
     return render(request, 'datascience.html', {'data_science_courses':published_courses})


def cpp_view(request):
     cpp_courses = [course for course in course_one if course.get('category')=="C++"]
     
     published_courses = []
    
     for course_dict in cpp_courses:
            course_from_db = Course.objects.get(id=course_dict['id'])
            updated_course_dict = course_dict.copy()
            updated_course_dict['image'] = course_from_db.course_image
            updated_course_dict['is_draft'] = course_from_db.is_draft 
            updated_course_dict['video'] = course_from_db.course_videos
            
            if updated_course_dict['is_draft'] == False:
                published_courses.append(updated_course_dict)
     return render(request, 'cpp.html', {'cpp_courses':published_courses})


def excel_view(request):
     sql_courses = [course for course in course_one if course.get('category')=="SQL"]
     
     published_courses = []
    
     for course_dict in sql_courses:
            course_from_db = Course.objects.get(id=course_dict['id'])
            updated_course_dict = course_dict.copy()
            updated_course_dict['image'] = course_from_db.course_image
            updated_course_dict['is_draft'] = course_from_db.is_draft 
            updated_course_dict['video'] = course_from_db.course_videos
            
            if updated_course_dict['is_draft'] == False:
                published_courses.append(updated_course_dict)
                
     return render(request, 'excel.html', {'sql_courses':published_courses})


def python_view(request):
    python_courses = [course for course in course_one if course.get('category')=="Python"]
    
    published_courses = []
    
    for course_dict in python_courses:
            course_from_db = Course.objects.get(id=course_dict['id'])
            updated_course_dict = course_dict.copy()
            updated_course_dict['image'] = course_from_db.course_image
            updated_course_dict['is_draft'] = course_from_db.is_draft 
            updated_course_dict['video'] = course_from_db.course_videos
            
            if updated_course_dict['is_draft'] == False:
                published_courses.append(updated_course_dict)
    return render(request, 'python.html',{'python_courses':published_courses})

def java_view(request):
     java_courses = [course for course in course_one if course.get('category')=="Java"]
     
     published_courses = []
    
     for course_dict in java_courses:
            course_from_db = Course.objects.get(id=course_dict['id'])
            updated_course_dict = course_dict.copy()
            updated_course_dict['image'] = course_from_db.course_image
            updated_course_dict['is_draft'] = course_from_db.is_draft 
            updated_course_dict['video'] = course_from_db.course_videos
            
            if updated_course_dict['is_draft'] == False:
                published_courses.append(updated_course_dict)
     return render(request, 'java.html', {'java_courses':published_courses})


def game_view(request):
     game_development_courses =[course for course in course_one if course.get('category')=="Game Development"]
     
     published_courses = []
    
     for course_dict in game_development_courses:
            course_from_db = Course.objects.get(id=course_dict['id'])
            updated_course_dict = course_dict.copy()
            updated_course_dict['image'] = course_from_db.course_image
            updated_course_dict['is_draft'] = course_from_db.is_draft 
            updated_course_dict['video'] = course_from_db.course_videos
            
            if updated_course_dict['is_draft'] == False:
                published_courses.append(updated_course_dict)
     return render(request, 'game_development.html', {'game_development_courses':published_courses })

def index_view(request):
    return render(request,'index.html')

def aboutus_view(request):
    return render(request,'aboutus.html')

def teach_view(request):
    return render(request,'teach.html')


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
def home(request):
    context = get_user_role_context(request)
    published_courses = []
    try:  
     for course_dict in course_one:
            course_from_db = Course.objects.get(id=course_dict['id'])
            updated_course_dict = course_dict.copy()
            updated_course_dict['image'] = course_from_db.course_image
            updated_course_dict['is_draft'] = course_from_db.is_draft 
            updated_course_dict['video'] = course_from_db.course_videos
            updated_course_dict['enrolled']=course_from_db.enrolled
            
            if updated_course_dict['is_draft'] == False:
                published_courses.append(updated_course_dict)
    except:
         pass          
    enroll = Enrolled_Course.objects.filter(user=request.user).values_list('name',flat=True)
    context['all_courses'] = published_courses
    context['enroll']=enroll
    return render(request, 'home.html', context)


    
@login_required
def logout_view(request):
    logout(request)
    return redirect('index')
   
   
@login_required
def user_profile_view(request):
    context = get_user_role_context(request)
    user_id = None
    all_users_response = requests.get(REGISTER_API_URL).json()
    all_users = all_users_response.get('users')
    for users in all_users:
            if users['username'] == request.user.username:  
             context['user_details']=users   
             print(context)
    return render(request, 'view_profile.html',context)



@login_required
def edit_profile_view(request, user_id):
    context = get_user_role_context(request)
    users_response_url = f"{REGISTER_API_URL}/{user_id}"

    try:
        user_response = requests.get(users_response_url)
        user_response.raise_for_status()
        this_user = user_response.json().get('user', {})
    except requests.exceptions.RequestException as e:
        this_user = {}
        
        messages.error(request, f"Error fetching user data: {str(e)}")

    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        user = None
        messages.error(request, "Profile not found!")

    this_user['image'] = user.profile_image if user and user.profile_image else None
    context['user'] = this_user
    context['user_profile']=user

    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        role = request.POST.get('role')
        experience = request.POST.get('experience') if role == 'Teacher' else None
        linkedin = request.POST.get('linkedin') if role == 'Teacher' else None
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')

        data = {
            'name': name,
            'experience': experience,
            'linkedin': linkedin,
            'mobile': mobile,
            'gender': gender
        }

        if image and user:
            user.profile_image = image
            user.save()
        try:
            response = requests.put(users_response_url, json=data)
            response.raise_for_status()
            messages.success(request, "Updated successfully!")
            return redirect('view_profile')
        except requests.exceptions.RequestException as e:
            error_message = f"Error: {str(e)}"
            try:
                error_data = response.json()
                error_message = f"Error: {error_data.get('detail', str(e))}"
            except:
                pass  
            messages.error(request, error_message)
            return render(request, 'edit_profile.html', context)

    return render(request, 'edit_profile.html', context)

@login_required
def change_password_view(request,user_id):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return render(request, 'change_password.html')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match!")
            return render(request, 'change_password.html')

        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters long!")
            return render(request, 'change_password.html')
        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)

        api_data = {
            "password": new_password,
            "confirm_password":confirm_password
            }
        api_url = f"{REGISTER_API_URL}/{user_id}"
        
        try:
            response = requests.put(api_url, json=api_data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            messages.error(request, f"{str(e)}")
            return render(request, 'change_password.html')

        messages.success(request, "Password changed successfully!")
        return redirect('view_profile')

    return render(request, 'change_password.html')
        
        
        
        