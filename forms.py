from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from groupstudy.models import Post, Comment


class UserForm(UserCreationForm):
    last_name = forms.CharField(max_length=5)
    first_name = forms.CharField(max_length=5)
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "last_name", "first_name", "email")


class PostForm(forms.ModelForm):
    class Meta:
        model = Post  # 사용할 모델
        fields = ['subject', 'content']  # PostFrom에서 사용할 Post 모델의 속성
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
        labels = {
            'subject': '제목',
            'content': '내용',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # 사용할 모델
        fields = ['content']  # CommentForm에서 사용할 Comment 모델의 속성
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
        labels = {
            'content': '내용',
        }
