from django.db import models

# Create your models here.

class Note(models.Model):
    index = models.IntegerField()
    name = models.TextField(max_length=200)
    desc = models.TextField(default='',max_length=1000)
    tags = models.ManyToManyField('Tag')
  

class Image(models.Model):
    image = models.ImageField()
    note = models.ForeignKey(Note, on_delete=models.CASCADE)


class Tag(models.Model):
    title = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"
        ordering = ['title']
    
    
    def get_absolute_url(self):
     return "/tags/%s/" % self.slug

