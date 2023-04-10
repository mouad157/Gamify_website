from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
class Slave(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
class Task(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    task_title = models.TextField(max_length=30)
    task_text = models.TextField()
    priority = models.IntegerField()
    quantity_left = models.IntegerField()
    quantity_done = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
class Image(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null= True, upload_to='images/')
    origin = models.ForeignKey(Slave, blank=True, null= True, on_delete=models.CASCADE)
    reviewed = models.BooleanField(default = False)
    mark = models.IntegerField(blank=True,null =True)
class Reveiw(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    mark = models.IntegerField()
    

