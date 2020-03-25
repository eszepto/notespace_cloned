
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from .models import Note, Image, Tag, Review
from django.template.loader import get_template
# Create your views here.
def ClearStrSpace(input):
    return " ".join(input.split())

def home_page(request):
    notes = Note.objects.order_by('-upload_time')
    return render(request,'home_page.html',{'notes':notes})
def upload_page(request):
    return render(request,'upload_page.html')
def upload_api(request):
    filetype_list = ["img", "png", "jpg" ,"jpeg", "tiff", "gif", "bmp"]
    if request.POST:
        newnote = Note()
        newnote.name  =  ClearStrSpace(request.POST['name'])
        newnote.owner =  ClearStrSpace(request.POST['guestname'])
        newnote.desc  =  ClearStrSpace(request.POST['desc'])
        newnote.save()

        i = 0
        for file in request.FILES.getlist('myfile'):
            if(len(file.name.split(".")) > 1 and
                    file.name.split(".")[-1].lower() in filetype_list):
                newimg = Image()
                newimg.image = file
                newimg.index = i
                newimg.note = newnote
                newimg.save()
                i += 1
        if(i==0): #all file is invalid
            newnote.delete()
            return HttpResponse("File Type Error")
        
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')

def detial(request,note_index):
    n = get_object_or_404(Note, pk=note_index)
    images = Image.objects.filter(note=n)
    img_url = [i.image.url for i in images]
    return render(request,'detail.html',{'images_url':img_url,'note':n})

def about(request):
    return render(request, 'about.html')

def help(request):
    return render(request, 'help_main.html')

def help_detail(request, help_topic):
    try:
        get_template("help/%s.html"%(help_topic))
        return render(request, "help/%s.html"%(help_topic) ) 
    except:
        return HttpResponseNotFound("<h1>404 Page not found</h1>")

def search(request):
    query_word = request.GET.get("q",'')
    searched_notes = Note.objects.filter(Q(name__icontains=query_word) | 
                                            Q(desc__icontains=query_word) |
                                            Q(tags__title__icontains=query_word) 
                                            ) 
   
    return render(request, 'search_result.html', 
    {
        'search_key':query_word,
        'searched_notes':searched_notes })

def tagQuery(request, tag_title):
    query_tag = get_object_or_404(Tag , title=tag_title)
    return render(request, 'tag_result.html',{'tag':query_tag})

def addcomment_api(request):
    note_id = request.POST['note_id']
    n = Note.objects.get(id=note_id)

    author = request.POST['author']
    text = request.POST['text']
    score = float(request.POST['score']) if request.POST['score'] in ["1","2","3","4","5"] else 0

    review = Review()
    review.note = n
    review.author = author
    review.text = text
    review.score = score

    review.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))