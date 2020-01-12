from django.db import models

# Create your models here.

class Note(models.Model):
    index = models.IntegerField()
    name = models.TextField(max_length=200)
    desc = models.TextField(default='',max_length=1000)

class Image(models.Model):
    image = models.ImageField()
    note = models.ForeignKey(Note, on_delete=models.CASCADE)


