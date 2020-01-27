from django.contrib import admin
from .models import Note, Image, Tag
# Register your models here.

class ImageInline(admin.StackedInline):
    model = Image
    extra = 1

class NoteAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    fieldsets = [
        
        ("", {'fields': ['name','desc','upload_time']})
        
    ]

admin.site.register(Note, NoteAdmin)