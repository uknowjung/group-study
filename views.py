from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect, resolve_url

from .forms import UserForm, PostForm, CommentForm
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


@login_required(login_url='login')
def plan_detail(request, plan_id):
    if request.method == 'POST':
        if request.user.username == 'admin':
            return redirect('index')
        progress_update(request, request.user.username)
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        plan = get_object_or_404(Plan, pk=plan_id)
        form = PostForm()
    context = {
        'plan': plan,
        'form': form,
    }
    return render(request, 'plan_detail.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'post_detail.html', context)


@login_required(login_url='login')
def post_modify(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        messages.error(request, "수정 권한이 없습니다")
        return redirect('post_detail', post_id=post.id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    context = {
        "form": form,
        "post": post,
    }
    return render(request, 'post_form.html', context)


@login_required(login_url='login')
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('post_detail', post_id=post.id)
    post.delete()
    return redirect('personal_page', username=request.user.username)


@login_required(login_url='login')
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('post_detail', post_id=post.id), comment.id))
    else:
        return HttpResponseNotAllowed('포스팅만 가능합니다!')
    context = {'post': post, 'form': form}
    return render(request, 'post_detail.html', context)


@login_required(login_url='login')
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('post_detail', post_id=comment.post.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('post_detail', post_id=comment.post.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'comment': comment, 'form': form}
    return render(request, 'comment_form.html', context)


@login_required(login_url='login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        comment.delete()
    return redirect('post_detail', post_id=comment.post.id)


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
    _ = username
    progress_list = Progress.objects.order_by("complete_date").filter(user=request.user.id)
    progress = progress_list.filter(complete_date=datetime.now())
    if not progress:
        progress = Progress(user=request.user)
        progress.save()


def show_personal_page(request, username):
    target_user = get_user_model().objects.get(username=username)
    my_progress_list = Progress.objects.order_by("complete_date").filter(user=target_user)
    my_post_list = Post.objects.filter(author=target_user).order_by("-create_date")
    context = {
        "my_progress_list": my_progress_list,
        "target_user": target_user,
        "my_post_list": my_post_list,
    }
    return render(request, 'personal_page.html', context)
