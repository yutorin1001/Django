from django.db import models

# Create your models here.
class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def ___str___(self):
        return self.title