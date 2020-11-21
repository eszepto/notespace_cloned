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

from notes.models  import Note, Image, Tag, Review
from notes.views.help import _clear_str_space

def home_page(request):  # path - <domain>/
    notes = Note.objects.order_by('-upload_time')           # get all notes in db orderby latest upload time
    return render(request,'home_page.html',{'notes':notes}) # return return from home_page.html with notes

def about(request): # path - <domain>/about/
    return render(request, 'about.html')  # return render from about.html

def help_page(request): # path - <domain>/help/
    return render(request, 'help_main.html') # return render from help_main.html

def help_detail(request, help_topic): # 
    try:  # try to search for topic file
        get_template("help/%s.html"%(help_topic))              # try to get topic template file
        return render(request, "help/%s.html"%(help_topic) )   # return that topic template file
    except:
        return HttpResponseNotFound("<h1>404 Page not found</h1>")  # else return 404 page



def detial(request,note_index): # path - <domain>/<note_index>/
    _note = get_object_or_404(Note, pk=note_index)   # get note from database by note_index , if not found return 404
    _images = Image.objects.filter(note=_note)        # get images of note from database 
    img_urls = [i.image.url for i in _images]      # get list of urls of those images
    return render(request,'detail.html',{'images_url':img_urls,'note':_note})  # return datail.html

def tag_query(request, tag_title): # path - <domain>/tag/<tag_name> 
    _tag = get_object_or_404(Tag , title=tag_title)        # get tag from database by tag_title , if not found return 404
    return render(request, 'tag_result.html',{'tag':_tag}) # return tag_result.html



def upload_page(request): # path - <domain>/upload/
    if request.user.is_authenticated:
        return render(request,'upload_page.html')  # return upload page
    else:
        return HttpResponseRedirect('/login')

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

def register_page(request): # path - <domain>/register    
    return render(request, "register_page.html")

def login_page(request): # path - <domain>/login
    if not(request.user.is_authenticated):  # if user hasn't login
        return render(request, "login_page.html")
    else: # if user already login
        return HttpResponseRedirect('/')
