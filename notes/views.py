from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home_page(request):
    return render(request,'home_page.html')
def upload_page(request):
    return render(request,'upload_page.html')