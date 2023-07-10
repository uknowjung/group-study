from datetime import datetime

from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, get_object_or_404, redirect

from .forms import UserForm
from .models import *


# Create your views here.


def index(request):
    plan_list = Plan.objects.order_by("create_date").filter(create_date=datetime.now())
    progress_list = Progress.objects.all()
    my_progress_list = Progress.objects.order_by("complete_date").filter(user=request.user.id)
    progress = my_progress_list.filter(complete_date=datetime.now())
    len_progress_list = len(progress_list)
    user_list = get_user_model().objects.all()
    len_user_list = len(user_list) - 1  # 관리자 계정 제외
    context = {
        "plan_list": plan_list,
        "progress": progress,
        "len_progress_list": len_progress_list,
        "len_user_list": len_user_list,
        "user_list": user_list,
    }
    return render(request, "index.html", context)


def plan_detail(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id)
    context = {'plan': plan}
    return render(request, 'plan_detail.html', context)


def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = Comment(post=post, content=request.POST.get('content'))
    comment.save()
    return redirect('post_detail', post_id=post.id)


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})


def progress_update(request, username):
    if username == "admin":
        return redirect('index')
    progress_list = Progress.objects.order_by("complete_date").filter(user=request.user.id)
    progress = progress_list.filter(complete_date=datetime.now())
    if not progress:
        progress = Progress(user=request.user)
        progress.save()
    return redirect('index')


def show_personal_page(request, username):
    target_user = get_user_model().objects.get(username=username)
    my_progress_list = Progress.objects.order_by("complete_date").filter(user=target_user)
    context = {
        "my_progress_list": my_progress_list,
        "target_user": target_user,
    }
    return render(request, 'personal_page.html', context)
