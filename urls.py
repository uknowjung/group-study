"""
URL configuration for base project.

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
from django.urls import path
from django.contrib.auth import views as auth_views

from groupstudy import views

urlpatterns = [
    path("", views.index, name="index"),
    path('plan/<int:plan_id>/', views.plan_detail, name="plan_detail"),
    path('post/<int:post_id>/', views.post_detail, name="post_detail"),
    path('post/modify/<int:post_id>/', views.post_modify, name="post_modify"),
    path('post/delete/<int:post_id>/', views.post_delete, name='post_delete'),
    path('comment/create/<int:post_id>/', views.comment_create, name='comment_create'),
    path('comment/modify/<int:comment_id>/', views.comment_modify, name='comment_modify'),
    path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('progress-update/<str:username>/', views.progress_update, name='progress_update'),
    path('personal-page/<str:username>/', views.show_personal_page, name='personal_page'),
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]
