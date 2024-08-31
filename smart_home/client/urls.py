"""
URL configuration for smart_home project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from client import views
from django.urls import include, path

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('accounts/login/signup', views.signup, name='signup'),   
    path('login/', views.login_view, name='login'),
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),    
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('connect', views.connect, name='connect'),
    path('add', views.append_control, name='add'),
    path('send/<int:pk>/', views.send_signal, name='send'),
    path('posts/<int:pk>/edit/', views.edit_control, name='edit_post'),
    path('posts/<int:pk>/delete/', views.delete_control, name='delete_post'),
        path('tasks', views.task_list, name='task_list'),
     path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/new/', views.task_create, name='task_create'),
    path('task/<int:pk>/complete/', views.task_complete, name='task_complete'),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)