from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Note, Image, Tag
# Create your views here.
def ClearStrSpace(input):
    return " ".join(input.split())

def home_page(request):
    notes = Note.objects.order_by('-upload_time')
    return render(request,'home_page.html',{'notes':notes})
def upload_page(request):
    return render(request,'upload_page.html')
def upload_api(request):
    filetype_list = ["img", "png", "jpg", "jpeg", "tiff", "gif", "bmp"]
    if request.POST:
        newnote = Note()
        newnote.name  =  ClearStrSpace(request.POST['name'])
        newnote.owner =  ClearStrSpace(request.POST['guestname'])
        newnote.desc  =  ClearStrSpace(request.POST['desc'])
        newnote.save()

        i = 0
        for file in request.FILES.getlist('myfile'):
            if(len(file.name.split(".")) > 1 and
                    file.name.split(".")[-1] in filetype_list):
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
    img_url = []
    for i in images:
        img_url.append(i.image.url)
    return render(request,'detail.html',{'images_url':img_url,'note':n})

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