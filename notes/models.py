import datetime

from django.db import models
from django.db.models import Q
from sorl.thumbnail import ImageField


# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True) # the full title for url and spaced with dash like "physic-in-everyday-life"
    
    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/tags/%s/" % self.slug
    


class Note(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=200)
    owner = models.CharField(max_length=30)
    desc = models.CharField(default='',max_length=1000) # description
    upload_time = models.DateTimeField('upload_time', null=True, default=datetime.datetime.now)
    tags =  models.ManyToManyField(Tag,related_name='notes')
    def __str__(self):
        return self.name
    def thumbnail_url(self):
        try:
            i = self.thumbnail.get().image.url # get thumbnail url of note
            return i 
        except:
            return "/media/error_not_found.jpg"

    def get_mean_score(self): #for getting review mean score of note
        all_reviews = self.reviews
        score = 0
        n = len(all_reviews)
        for review in all_reviews:  
            score += review.score
        mean = score/n     #
        mean = round(mean, 2) # round to 2 digit
        mean = float("{:.2f}".format(mean))  #fix floating point problem to get exactly 2 digit value
        return mean



def thumbnail_uploadto_path(instance, filename):
    return '{0}/thumbnail.{1}'.format(instance.note.id, filename.split('.')[-1]) 
class Thumbnail(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="thumbnail")
    image = models.ImageField(upload_to=thumbnail_uploadto_path)

def image_uploadto_path(instance, filename): #for getting path for each image file
    # files will be uploaded to <MEDIA_ROOT>/<note_id>/<filename>
    return '{0}/{1}'.format(instance.note.id, filename) 
class Image(models.Model):
    index = models.IntegerField()
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=image_uploadto_path)


class Review(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="reviews")
    author = models.CharField(max_length=30)
    datetime = models.DateTimeField("reviewed_time", null=True, default=datetime.datetime.now)
    score = models.FloatField(default=0)
    text = models.TextField(max_length=1000)

    

    




