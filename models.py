from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.subject)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.post) + " (" + self.create_date.strftime("%Y/%m/%d %H시 %M분 %S초") + ")"


class Plan(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateField()

    def __str__(self):
        return str(self.subject)


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    complete_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user.last_name) + str(self.user.first_name) + " (" + self.complete_date.strftime("%Y/%m/%d") + " 완료)"
