from django.db import models
from django.db.models import Q
from sorl.thumbnail import ImageField, get_thumbnail
import sorl.thumbnail
import datetime

from notes.field import RatingField

# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"
        ordering = ['title']
    
    
    def get_absolute_url(self):
     return "/tags/%s/" % self.slug
    def __str__(self):
        return self.title


class Note(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=200)
    owner = models.CharField(max_length=30)
    desc = models.CharField(default='',max_length=1000)
    upload_time = models.DateTimeField('upload_time', null=True, default=datetime.datetime.now)
    tags =  models.ManyToManyField(Tag,related_name='notes')
    def __str__(self):
        return self.name
    def get_thumb(self):
        try:
            i = Image.objects.filter(note=self)[0].get_thumb()
            print(i)
            return i # remember that sorl objects have url/width/height attributes
        except:
            return "/media/loading.jpg"
    def search(self):
        pass


def note_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<>/<filename>
    return '{0}/{1}'.format(instance.note.id, filename)
class Image(models.Model):
    index = models.IntegerField()
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="images")
    image = ImageField(upload_to=note_directory_path)
    def get_thumb(self):
        im = get_thumbnail(self.image, '500x500', crop='center', quality=99)
        return im.url # remember that sorl objects have url/width/height attributes

class Review(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="reviews")
    author = models.CharField(max_length=30)
    datetime = models.DateTimeField("reviewed_time", null=True, default=datetime.datetime.now)
    score = models.FloatField()
    text = models.TextField(max_length=1000)

    




