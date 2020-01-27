from django.test import TestCase
from django.test import LiveServerTestCase
from django.shortcuts import get_object_or_404
from .models import Note, Image
from django.core.files.uploadedfile import SimpleUploadedFile
# Create your tests here.
class Unittest(TestCase):
    def test_can_resolve_url_to_note_url(self):
        pass

class NoteModelTest(LiveServerTestCase):
    def test_database_can_save_and_get_one_Note_multiple_images(self):
        n = Note()
        n.name = "test note"
        n.desc = "this is note for ..."
        n.save()

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
        

        n =Note.objects.filter(id=1)
        images = Image.objects.filter(note=n[0])
        self.assertEqual(images.count(), 2)

    def test_database_note_id_increte_automatically_without_declaration(self):
        note1 = Note()
        note1.save()
        note2 = Note()
        note2.save()
        
        print(f"note2.id : {note2.id}")
        self.assertEqual(note2.id - note1.id, 1)