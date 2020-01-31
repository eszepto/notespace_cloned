from django.test import TestCase
from django.test import LiveServerTestCase
from django.shortcuts import get_object_or_404
from .models import Note, Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Q
# Create your tests here.
class Unittest(TestCase):
    def test_can_resolve_url_to_note_url(self):
        pass

class NoteModelTest(LiveServerTestCase):
    def test_database_canbe_query(self):
        note1 = Note()
        note1.id = 5
        note1.name = "for testing"
        note1.save()

        n=Note.objects.filter(id=5)[0]
        self.assertEqual(n.name, "for testing")


    def test_database_can_save_and_get_one_Note_multiple_images(self):
        n = Note()
        n.name = "test note"
        n.desc = "this is note for ..."
        n.save()
        n_id = n.id

        img1 = Image()
        img1.index = 1
        img1.note = n
        img1.image = SimpleUploadedFile(name='1.jpg', content=open("C:/Users/B/OneDrive/Documents/68C6277C-16C8-4E21-9910-0205EFA62918.jpg", 'rb').read(), content_type='image/jpeg') 
        img1.save()

        img2 = Image()
        img2.index = 2
        img2.note = n
        img2.image = SimpleUploadedFile(name='1.jpg', content=open("C:/Users/B/OneDrive/Documents/68C6277C-16C8-4E21-9910-0205EFA62918.jpg", 'rb').read(), content_type='image/jpeg')
        img2.save()
        

        n = Note.objects.get(pk=n_id)
        images = Image.objects.filter(note=n)
        self.assertEqual(images.count(), 2)
        
    def test_database_note_id_increte_automatically_without_declaration(self):
        note1 = Note()
        note1.save()
        note2 = Note()
        note2.save()
        
        self.assertEqual(note2.id - note1.id, 1)
    
    def test_database_automatically_add_upload_time(self):
        note1 = Note()
        note1.save()
        print(note1.upload_time)
        self.assertNotEqual(note1.upload_time, None)

    def test_database_can_search_by_similar(self):
        note1 = Note()
        note1.name = "django"
        note1.save()

        note2 = Note()
        note2.name = "djang"
        note2.save()

        note3 = Note()
        note3.name = "writing unit test"
        note3.desc = "for django"
        note3.save()

        search_result = Note.objects.filter(name__trigram_similar="django").filter(desc__trigram_similar"django")
        self.
    
    
        
