from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Image,Note
# Create your views here.
def home_page(request):
    notes = Note.objects.order_by('-upload_time')
    return render(request,'home_page.html',{'notes':notes})
def upload_page(request):
    return render(request,'upload_page.html')

def detial(request,note_index):
    n = get_object_or_404(Note, pk=note_index)
    images = Image.objects.filter(note=n)
    img_url = []
    for i in images:
        img_url.append(i.image.url)
    return render(request,'detail.html',{'images_url':img_url,'note':n})

def search(request):
    query_word = request.GET.get("q",'')
    print(query_word)
    searched_notes = Note.objects.filter(name__icontains=query_word)
   
    print(searched_notes)
    return render(request, 'search_result.html', 
    {
        'search_key':query_word,
        'searched_notes':searched_notes })
