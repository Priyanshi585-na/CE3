from django.urls import path 
from . import views
urlpatterns = [
    path('pay/<str:course_id>',views.pay_view,name='pay'),
    path('datasciencecourse/',views.data_science,name='datasciencecourse'),
    path('webdevelopmentcourse/',views.web_development_view,name='webdevelopmentcourse'),
    path('aicourse/',views.ai,name='aicourse'),
    path('sqlcourse/',views.excel,name='sqlcourse'),
    path('gamedevelopmentcourse/',views.game,name='gamedevelopmentcourse'),
    path('pythoncourse/',views.python,name='pythoncourse'),
    path('javacourse/',views.java,name='javacourse'),
    path('cppcourse/',views.cpp,name='cppcourse'),
    path('my_learning',views.my_learning_view,name='my_learning'),
    path('enroll/<str:course_id>/',views.enroll,name='enroll')
    
    
    ]