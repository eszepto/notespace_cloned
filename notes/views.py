from django.shortcuts import render
from django.http import HttpResponse
from .models import Image,Note
# Create your views here.
def home_page(request):
    notes = Note.objects.order_by('-upload_time')
    return render(request,'home_page.html',{'notes':notes})
def upload_page(request):
    return render(request,'upload_page.html')
    
def detial(request,note_index):
    return render(request,'detail.html')