from . import views
from django.urls import path

urlpatterns = [
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('feedback/',views.contact_view,name='feedback'),
    path('review/',views.review,name='review'),
     path('AiEngineering/',views.ai_view, name='ai'),
    path('java/',views.java_view, name='java'),
    path('cpp/',views.cpp_view, name='cpp'),
    path('GameDevelopment/',views.game_view, name='game_development'),
    path('WebDevelopment/',views.web_development, name='web_development'),
    path('python/',views.python_view, name='python'),
    path('data_science/',views.data_science_view, name='data_science'),
    path('excel/',views.excel_view, name='excel'),
    path('',views.index_view, name='index'),
    path('aboutus/',views.aboutus_view, name='about'),
    path('contactus/',views.contact_view, name='contact'),
    path('teach/',views.teach_view,name='teach'),
    path('home/',views.home,name='home'),
    path('logout/',views.logout_view,name='logout'),
    path('edit_profile/<str:user_id>/',views.edit_profile_view,name='edit_profile'),
    path('view_profile/',views.user_profile_view,name='view_profile'),
    path('change_password/<str:user_id>/',views.change_password_view,name='change_password')

]