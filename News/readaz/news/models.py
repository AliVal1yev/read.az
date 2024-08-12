from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta



class Category(models.Model):
    title = models.CharField(max_length=32)
    
    def __str__(self) -> str:
        return f'{self.title}'

class New(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now , null= True, blank= True)
    updated_at = models.DateTimeField(auto_now=True)
    watch_count = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='media/%Y/%m/%d', blank=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    
    def __str__(self) -> str:
        return f' {self.pk}. {self.title}'
    
    def check_and_expire(self):
        if self.created_at < timezone.now() - timedelta(days=30):
            self.available = False
            self.save(update_fields=['available'])
    
    
    
class UserInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(New, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    disliked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'post')
