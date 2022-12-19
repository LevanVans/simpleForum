from django.db import models
from django.contrib.auth.models import User


# Model for each post on Forum

class Post(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
    body = models.TextField(max_length=200)
    tags = models.ManyToManyField('Tag', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated','-created']

                
        



# Model for post's  Topics

class Topic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name



# Model for post's comments

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    post = models.ForeignKey('Post', on_delete=models.CASCADE  )
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "User:" + self.user.username

    class Meta:
        ordering = ['-updated','-created']

# Tags for posts

class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name