from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='related_post', blank=True) 
    def ___str___(self):
        return self.title

    class Meta:
       ordering = ["-created_at"]
       verbose_name_plural = "投稿"



class Connection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return self.user.username 


class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 返信したユーザー
    content = models.TextField()  # 返信内容
    created_at = models.DateTimeField(auto_now_add=True)  # 返信日時
    def __str__(self):
        return f"Reply by {self.user.username} on {self.post.id}"

    class Meta:
       ordering = ["-created_at"]
       verbose_name_plural = "投稿"
