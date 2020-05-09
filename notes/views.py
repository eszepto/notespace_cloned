
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

from .models import Note, Image, Tag, Review
# Create your views here.


def home_page(request):  # path - <domain>/
    notes = Note.objects.order_by('-upload_time')           # get all notes in db orderby latest upload time
    return render(request,'home_page.html',{'notes':notes}) # return return from home_page.html with notes
@csrf_exempt
def about(request): # path - <domain>/about/
    return render(request, 'about.html')  # return render from about.html

def detial(request,note_index): # path - <domain>/<note_index>/
    _note = get_object_or_404(Note, pk=note_index)   # get note from database by note_index , if not found return 404
    _images = Image.objects.filter(note=_note)        # get images of note from database 
    img_urls = [i.image.url for i in _images]      # get list of urls of those images
    return render(request,'detail.html',{'images_url':img_urls,'note':_note})  # return datail.html

def tag_query(request, tag_title): # path - <domain>/tag/<tag_name> 
    _tag = get_object_or_404(Tag , title=tag_title)        # get tag from database by tag_title , if not found return 404
    return render(request, 'tag_result.html',{'tag':_tag}) # return tag_result.html

def help_page(request): # path - <domain>/help/
    return render(request, 'help_main.html') # return render from help_main.html

def help_detail(request, help_topic): # 
    try:  # try to search for topic file
        get_template("help/%s.html"%(help_topic))              # try to get topic template file
        return render(request, "help/%s.html"%(help_topic) )   # return that topic template file
    except:
        return HttpResponseNotFound("<h1>404 Page not found</h1>")  # else return 404 page



def upload_page(request): # path - <domain>/upload/
    if request.user.is_authenticated:
        return render(request,'upload_page.html')  # return upload page
    else:
        return HttpResponseRedirect('/login')

def _clear_str_space(input): # for deleting excess space in String
    return " ".join(input.split())  # "aaaa    bbbb" to "aaaa bbbb"

def upload_api(request): # path - <domain>/api/upload/
    IMAGEFILE_EXTENSIONS = ["img", "png", "jpg" ,"jpeg", "tiff", "gif", "bmp"]   # white list for imagefile extension with lower-case 
    if request.POST and request.user.is_authenticated:  # if request method is POST
        newnote = Note()   # create new note
        newnote.name  =  _clear_str_space(request.POST['name'])      # set note name with excess space cleared POST[name]
        newnote.owner =  _clear_str_space(request.POST['guestname']) # set note owner with excess space cleared POST[guestname]
        newnote.desc  =  _clear_str_space(request.POST['desc'])      # set note description with excess space cleared POST[desc]
        newnote.save() # save note to database

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
            newnote.delete()  # delete that note from database
            return HttpResponse("File Type Error")  # and return "file type error"
        
        return HttpResponseRedirect("/")  # return to to homepage
        
    return HttpResponseRedirect("/")  # if request method isnot POST -> return to homepage



def search_page(request): # path - <domain>/search?q=<query_word>/
    query_word = request.GET.get("q",'')        # set query_word value from request parameter 'q'
    searched_notes = Note.objects.filter(Q(name__icontains=query_word) |         # get notes from database by using query with name or description or tag
                                            Q(desc__icontains=query_word) |
                                            Q(tags__title__icontains=query_word) 
                                            )   
   
    return render(request, 'search_result.html',  # return search_result.html
    {
        'search_key':query_word,
        'searched_notes':searched_notes,
        })   



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

def register_page(request): # path - <domain>/register    
    return render(request, "register_page.html")
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

def login_page(request): # path - <domain>/login
    if not(request.user.is_authenticated):  # if user hasn't login
        return render(request, "login_page.html")
    else: # if user already login
        return HttpResponseRedirect('/')
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

def has_login(request):
    status = request.session.get('status')
    if status == "loggedin":
        return JsonResponse({"has_login":True})
    else:
        return JsonResponse({"has_login":False})