from django.db import models
from django.contrib.auth.models import User

class CourseType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name

class Profile(models.Model):
    user = models.ForeignKey(User)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    user_desciption = models.TextField()

    def __unicode__(self):
        return self.user.username

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_type = models.ForeignKey(CourseType)
    course_desciption = models.TextField()
    owner = models.ForeignKey(Profile)
    price = models.IntegerField()

    def __unicode__(self):
        return self.course_name

# Create your models here.
