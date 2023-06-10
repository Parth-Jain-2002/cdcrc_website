from django.db import models
from datetime import date
from django.contrib.auth.models import User
from utils.validators import validate_file_extension, validate_file_size
import random
from martor.models import MartorField

class ContactUsResponse(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    organization = models.CharField(max_length=256, null=True, blank=True)
    email = models.EmailField(null=False, blank=False)
    phone = models.CharField(max_length=13, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    body = models.TextField(blank=True, null=True)
    brief = models.TextField( blank=True, null=True)
    url=models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

class Events(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    body = models.TextField(blank=True, null=True)
    brief=models.TextField( null=True, blank=True)
    venue=models.CharField(max_length=100,blank = True,null=True)
    date = models.DateField(default=date.today)
    url=models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title 


class ResourceCategory(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class Resource(models.Model):
    title = models.CharField(max_length=256, null=False, blank=False)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    categories = models.ManyToManyField(ResourceCategory, related_name='resources', help_text="Use Ctrl key and select as many categories you wish to choose. 😎")
    url = models.URLField(null=True, blank=True)
    brief = models.CharField(max_length=2000, help_text='Try to keep it less than 300 chars')
    detail = MartorField()
    datetime = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class ResourceImage(models.Model):
    image = models.ImageField(upload_to='resources/images/% Y/% m/% d/')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='images', validators=[validate_file_extension, validate_file_size])

    def __str__(self):
        return str(self.image)

class Department(models.Model):
    name = models.CharField(max_length=256, unique=True, null=False, blank=False)

    def __str__(self):
        return self.name

class ProfessionalDevelopmentActivity(models.Model):
    title = models.CharField(max_length=256, null=False, blank=False)
    brief = models.TextField(null=False, blank=False)
    detail = models.TextField(null=True, blank=True)
    photo = models.ImageField()
    date = models.DateField()

    def __str__(self):
        return self.title

class ProfessionalDevelopmentBook(models.Model):
    photo = models.ImageField()
    title = models.CharField(max_length=256)
    writer = models.CharField(max_length=100)
    url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title

class ProfessionalDevelopmentVideo(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, default='')
    youtube_embed_url = models.CharField(max_length=200, null=False, blank=False, default='')

    def __str__(self):
        return self.title

class CorporateRelationsActivity(models.Model):
    title = models.CharField(max_length=256, null=False, blank=False)
    brief = models.TextField(null=False, blank=False)
    detail = models.TextField(null=True, blank=True)
    photo = models.ImageField()
    date = models.DateField()

    def __str__(self):
        return self.title

class ProfessionalDevelopmentInitiatives(models.Model):
    title = models.CharField(max_length=256, null=False, blank=False)
    brief = models.TextField(null=False, blank=False)
    detail = models.TextField(null=True, blank=True)
    photo = models.ImageField()
    date = models.DateField()

    def __str__(self):
        return self.title


authorDesignationChoices = ("Director", "Chairperson", "Vice Chairperson")
class Messages(models.Model):
    title = models.CharField(max_length=256, null=False, blank=False)
    # Either Director, Chairperson or Vice Chairperson
    authorDesignation = models.CharField(max_length=256, null=False, blank=False, choices=[(x, x) for x in authorDesignationChoices])
    brief = models.TextField(null=False, blank=False, help_text='Try to keep it less than 300 chars')
    detail = models.TextField(null=True, blank=True)
    photo = models.ImageField()

    def __str__(self):
        return self.title