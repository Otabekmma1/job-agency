from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('jobs/', all_jobs, name='jobs'),
    path('contact/', contact, name='contact'),
    path('job-detail/<int:id>/', job_detail, name='job-detail'),
    path('category/<int:category_id>/', jobs_by_category, name='by_category'),

    path('add-job/', add_job, name='add'),
    path('update-job/<int:id>/', update_job, name='update_job'),
    path('delete-job/<int:id>/', delete_job, name='delete_job'),

    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/' , user_logout, name='logout'),

    path('profile/', userprofile, name='profile'),
    path('update-profile/', update_profile, name='update_profile'),
    path('delete-profile/', delete_profile, name='delete_profile')

]