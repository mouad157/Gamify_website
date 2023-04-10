from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name = 'signup'),
    path('signin', views.signin, name = 'signin'),
    path('signout', views.signout, name = 'signout'),
    path('task/<int:id>/', views.task, name = 'task'),
    path('review_task/<int:id>/', views.review_task, name = 'review_task'),
    path('review_image/<int:id>/<int:taskid>/', views.review_image, name = 'review_image'),
    path('add_task', views.add_task, name = 'add_task'),
    path('download_task/<int:id>/', views.download_task, name = 'download_task'),
    
]