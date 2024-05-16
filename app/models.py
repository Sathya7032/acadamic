from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django_ckeditor_5.fields import CKEditor5Field

class User(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def profile(self):
        profile = Profile.objects.get(user=self)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=1000)
    bio = models.CharField(max_length=10000)
    role = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="user_images", default="default.jpg")


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)



class Todo(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
 
class Blogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    content = CKEditor5Field('Text', config_name='extends')
    date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_blogs', blank=True)
    
    def __str__(self):
        return self.title[:30]
    
    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.title}'

class TutorialName(models.Model):
    tutorialName = models.CharField(max_length=1000)
    tutorialContent = models.TextField()
    tutorialImage = models.ImageField(upload_to='Tutorials')
    def __str__(self):
        return self.tutorialName

class TutorialPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_title = models.CharField(max_length=100)
    post_content = CKEditor5Field('Text', config_name='extends')
    post_file = models.CharField(max_length=1000)
    tutorialName = models.ForeignKey(TutorialName, on_delete=models.CASCADE)   
    post_video = models.URLField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.post_title

class Comment_tutorials(models.Model):
    post = models.ForeignKey(TutorialPost, on_delete=models.CASCADE, related_name='comments_tutorials')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.post_title}'


class Meme(models.Model):
    description = models.CharField(max_length=1100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    images = models.FileField(upload_to='memes', default=1)
    likes = models.ManyToManyField(User, related_name='liked_memes', blank=True)

    def __str__(self):
        return self.description[:30]

    def total_likes(self):
        return self.likes.count()

class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    subject = models.CharField(max_length=20)
    message = models.TextField()
    
    def __str__(self):
        return self.name

class Language(models.Model):
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.language
    
class Topics(models.Model):
    topic = models.CharField(max_length=100)
    language = models.ForeignKey(Language,on_delete=models.CASCADE)

    def __str__(self):
        return self.topic

class CodeSnippet(models.Model):
    code_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    code = models.TextField()
    content = models.TextField()
    topic = models.ForeignKey(Topics,on_delete= models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.title
    

class Problem_solve(models.Model):
    content = CKEditor5Field('Text', config_name='extends') 
    user = models.ForeignKey(User,on_delete=models.CASCADE) 