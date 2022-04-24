from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from moviepy.editor import VideoFileClip
import datetime
from django.contrib.auth.models import User


# Create your models here.

class Course(models.Model):
    title=models.CharField(max_length=120,blank=False,null=False)
    slug=models.SlugField(unique=True)
    desc=models.CharField(max_length=200)
    price = models.IntegerField(blank=False,null=False)
    discount = models.IntegerField(blank=False,null=False , default = 0)
    thumbnail = models.ImageField(upload_to = "thumb",blank=False,null=False)
    date=models.DateTimeField(auto_now_add=True)
    length=models.PositiveIntegerField(blank=False,null=False)
    Active=models.BooleanField(default=False)

    def __str__(self):
        return self.title
    @property
    def discounts(self):
        price=self.price
        discount=self.discount
        amount=int(price-(price*discount*.01))
        return amount
  


class CourseAttribute(models.Model):
    title=models.CharField(max_length=120,blank=False,null=False)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        abstract=True


class Tag(CourseAttribute):
    pass        


class Prerequisite(CourseAttribute):
    pass   

class  Learning(CourseAttribute):
    pass   


class Module(models.Model):
    title=models.CharField(max_length=120,blank=False,null=False,unique=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.title

class Video(models.Model):
    serial=models.PositiveIntegerField(blank=False,null=False,unique=False)
    module=models.ForeignKey(Module,on_delete=models.CASCADE,blank=False,null=False)
    title=models.CharField(max_length=120,blank=False,null=False)
    desc=models.CharField(max_length=200,blank=False,null=False)
    video=models.FileField(upload_to='videos',blank=False,null=False,validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    notes=models.FileField(upload_to='notes',null=True,blank=True)
    is_preview=models.BooleanField(default=False)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    @property
    def vlength(self):
        templink=self.video.url
        reallink=f'http://127.0.0.1:8000{templink}'
        clip = VideoFileClip(reallink)
        duration = clip.duration
        video_time = str(datetime.timedelta(seconds = int(duration)))
        return video_time
        
#it will be helpfull for mycourse.
class UserCourse(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        user=f'{self.user.username} -{self.course.title}'
        return user

class Payment(models.Model):
    payment_id=models.CharField(max_length=100)
    order_id=models.CharField(max_length=120)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    user_course=models.ForeignKey(UserCourse, on_delete=models.CASCADE, null = True , blank = True , ) #It will be usefull for feteching course easily.
    date=models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=False)


       
class Copun(models.Model):
    code=models.CharField(max_length=120)
    discount=models.CharField(max_length=130)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)



