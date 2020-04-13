
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from .models import Note, Image, Tag, Review
from django.template.loader import get_template
# Create your views here.


def home_page(request):  # path - <domain>/
    notes = Note.objects.order_by('-upload_time')           # get all notes in db orderby latest upload time
    return render(request,'home_page.html',{'notes':notes}) # return return from home_page.html with notes

def about(request): # path - <domain>/about/
    return render(request, 'about.html')  # return render from about.html

def help(request): # path - <domain>/help/
    return render(request, 'help_main.html') # return render from help_main.html

def help_detail(request, help_topic): # 
    try:  # try to search for topic file
        get_template("help/%s.html"%(help_topic))              # try to get topic template file
        return render(request, "help/%s.html"%(help_topic) )   # return that topic template file
    except:
        return HttpResponseNotFound("<h1>404 Page not found</h1>")  # else return 404 page

def upload_page(request): # path - <domain>/upload/
    return render(request,'upload_page.html')  # return upload page

def ClearStrSpace(input): # for deleting excess space in String
    return " ".join(input.split())  # "aaaa    bbbb" to "aaaa bbbb"

def upload_api(request): # path - <domain>/api/upload/
    filetype_list = ["img", "png", "jpg" ,"jpeg", "tiff", "gif", "bmp"]   # white list for imagefile extension with lower-case 
    if request.POST:  # if request method is POST
        newnote = Note()   # create new note
        newnote.name  =  ClearStrSpace(request.POST['name'])      # set note name with excess space cleared POST[name]
        newnote.owner =  ClearStrSpace(request.POST['guestname']) # set note owner with excess space cleared POST[guestname]
        newnote.desc  =  ClearStrSpace(request.POST['desc'])      # set note description with excess space cleared POST[desc]
        newnote.save() # save note to database

        i = 0 # files index 
        for file in request.FILES.getlist('imagefiles'):   # for each file in request
            
            if(  len(file.name.split(".")) > 1   # if the file name has at least 1 "." for splitting   like "sample.file.jpeg" 
            and file.name.split(".")[-1].lower() in filetype_list): #  and the last word in lower-case when splitted is in white list imagefile extension 
                
                newimg = Image()    # create new image
                newimg.image = file # set image to current file 
                newimg.index = i    # set image index to current file index
                newimg.note = newnote # set note to that note
                newimg.save()       # save image to database
                i += 1 # file index plus 1

        if(i==0): # if all files is invalid so this note has no any image
            newnote.delete()  # delete that note from database
            return HttpResponse("File Type Error")  # and return "file type error"
        
        return HttpResponseRedirect('/')  # return to to homepage
        
    return HttpResponseRedirect('/')  # if request method isnot POST -> return to homepage

def detial(request,note_index): # path - <domain>/<note_index>/
    n = get_object_or_404(Note, pk=note_index)   # get note from database by note_index , if not found return 404
    images = Image.objects.filter(note=n)        # get images of note from database 
    img_url = [i.image.url for i in images]      # get list of urls of those images
    return render(request,'detail.html',{'images_url':img_url,'note':n})  # return datail.html

def search(request): # path - <domain>/search?q=<query_word>/
    query_word = request.GET.get("q",'')        # set query_word value from request parameter 'q'
    searched_notes = Note.objects.filter(Q(name__icontains=query_word) |         # get notes from database by using query with name or description or tag
                                            Q(desc__icontains=query_word) |
                                            Q(tags__title__icontains=query_word) 
                                            )   
   
    return render(request, 'search_result.html',  # return search_result.html
    {
        'search_key':query_word,
        'searched_notes':searched_notes })   

def tagQuery(request, tag_title): # path - <domain>/tag/<tag_name> 
    query_tag = get_object_or_404(Tag , title=tag_title)        # get tag from database by tag_title , if not found return 404
    return render(request, 'tag_result.html',{'tag':query_tag}) # return tag_result.html

def addcomment_api(request): # path - <domain>/api/addcomment/    
    """use for adding comment"""
    note_id = request.POST['note_id']    # set note_id value from  POST method request parameter 'note_id'
    n = Note.objects.get(id=note_id)     # use note_id to query note from database then save to  n

    author = request.POST['author']     # set author value from  POST method request parameter 'note_id'
    text = request.POST['text']         # set text value from POST method request parameter 'text'
    score = float(request.POST['score']) if request.POST['score'] in ["1","2","3","4","5"] else 0   # set score value from POST method request parameter 'score'  if score is number 0-5 else 0 

    review = Review()   # create new Review
    review.note = n     # set note of Review from n
    review.author = author # set author of Review from author
    review.text = text  # set text of Review from text
    review.score = score # set score of Review from score

    review.save()  # save Review to database
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   # return to current page