from PIL import Image

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.http import JsonResponse
from django.template.loader import get_template
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


def _clear_str_space(input): # for deleting excess space in String
    return " ".join(input.split())  # "aaaa    bbbb" to "aaaa bbbb"


def has_login(request):
    status = request.session.get('status')
    if status == "loggedin":
        return JsonResponse({"has_login":True})
    else:
        return JsonResponse({"has_login":False})

def crop_center(image_path):
    im = Image.open(image_path)
    
    width, height = im.size   # Get dimensions
    d = width
    if width > height :
        d = height
    left = (width - d)/2
    top = (height - d)/2
    right = (width + d)/2
    bottom = (height + d)/2
    
    im = im.crop((left, top, right, bottom))    
    im.save(image_path,"jpeg", quality=65)