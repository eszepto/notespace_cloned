from django.db import models

# Create your models here.

class Note(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.TextField(max_length=200)
    desc = models.TextField(default='',max_length=1000)
    upload_time = models.DateTimeField('upload_time', null=True)
    def __str__(self):
        return self.name

def note_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<>/<filename>
    return '{0}/{1}'.format(instance.note.id, filename)
class Image(models.Model):
    index = models.IntegerField()
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=note_directory_path)
    


class Tag(models.Model):
    title = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"
        ordering = ['title']
    
    
    def get_absolute_url(self):
     return "/tags/%s/" % self.slug

