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

from notes.models import Note, Image, Thumbnail, Tag, Review
from notes.views.help import _clear_str_space, crop_center

def upload_api(request): # path - <domain>/api/upload/
    IMAGEFILE_EXTENSIONS = ["img", "png", "jpg" ,"jpeg", "tiff", "gif", "bmp"]   # white list for imagefile extension with lower-case 
    if request.POST and request.user.is_authenticated:  # if request method is POST
        newnote = Note()   # create new note
        newnote.name  =  _clear_str_space(request.POST['name'])      # set note name with excess space cleared POST[name]
        newnote.owner =  _clear_str_space(request.POST['guestname']) # set note owner with excess space cleared POST[guestname]
        newnote.desc  =  _clear_str_space(request.POST['desc'])      # set note description with excess space cleared POST[desc]
        newnote.save() # save note to database

        newthumb = Thumbnail()
        newthumb.note = newnote
        print(type(request.FILES.getlist('imagefiles')[0].file))
        newthumb.image = request.FILES.getlist('imagefiles')[0]
        newthumb.save()

        i = 0 # files index 
        for file in request.FILES.getlist('imagefiles'):   # for each file in request
            
            if(  len(file.name.split(".")) > 1   # if the file name has at least 1 "." for splitting   like "sample.file.jpeg" 
            and file.name.split(".")[-1].lower() in IMAGEFILE_EXTENSIONS): #  and the last word in lower-case when splitted is in white list imagefile extension 
                
                newimg = Image()    # create new image
                newimg.image = file # set image to current file 
                newimg.index = i    # set image index to current file index
                newimg.note = newnote # set note to that note
                newimg.save()       # save image to database
                i += 1 # file index plus 1
        if(i==0): # if all files is invalid so this note has no any image
            return HttpResponse("File Type Error")  # and return "file type error"
        
        crop_center(newthumb.image.url[1:]) # crop image media/<note>/thumbnail.jpg to center
        return HttpResponseRedirect("/")  # return to to homepage
        
    return HttpResponseRedirect("/")  # if request method isnot POST -> return to homepage


def add_review_api(request): # path - <domain>/api/addreview/    
    """use for adding comment"""
    if request.POST and request.user.is_authenticated:
        note_id = request.POST['note_id']    # set note_id value from  POST method request parameter 'note_id'
        _note = Note.objects.get(id=note_id)     # use note_id to query note from database then save to  n

        author = request.POST['author']     # set author value from  POST method request parameter 'note_id'
        text = request.POST['text']         # set text value from POST method request parameter 'text'
        
        if request.POST['score'] in ["1","2","3","4","5"]:
            score = float(request.POST['score'])  
        else: 
            return JsonResponse({'status':'fail'})  

        review = Review()   # create new Review
        review.note = _note     # set note of Review from n
        review.author = author # set author of Review from author
        review.text = text  # set text of Review from text
        review.score = score # set score of Review from score

        review.save()  # save Review to database
        return HttpResponseRedirect(f"/notes/{note_id}/")   # return to current page



@csrf_exempt
def register_api(request): # path - <domain>/api/register
    """api for registering user"""
    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).count() is 0:   # if username not in database
            User.objects.create_user(username, email, password)  
            return JsonResponse({"status":"success"})
        else:
            return JsonResponse({"status":"fail"})

@csrf_exempt
def login_api(request): # path - <domain>/api/login
    """api for logging in """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password) # auth username and password 
    if user is not None:
        login(request, user) 
        request.session["status"] = "loggedin"
        return JsonResponse({"status":"success",
                            "username":username})
    else:
        return JsonResponse({"status":"fail"})

def logout_api(request): # path - <domain>/logout
    """api for logging out"""
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # redirect to previous page
