import datetime
import time
import json
import requests

from django.test import TestCase
from django.test import LiveServerTestCase
from django.test import Client
from django.shortcuts import get_object_or_404
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


from notes.models import Note, Image, Tag, Review


# Create your tests here.
class Unit_test(LiveServerTestCase):
    def setup(self):
        pass
    


    def test_api_can_register(self):
        response = self.client.post("/api/register/",data={'username':"jay",'email':"jay@abcd.com" ,"password":"123456"},follow=True)
        response = response.json()
        self.assertEqual(response["status"], "success")

        jay = User.objects.get(username="jay")
        self.assertEqual(jay.username, "jay")
        self.assertEqual(jay.email, "jay@abcd.com")
        self.assertNotEqual(jay.password, "123456")
    
    def test_api_cant_register_same_username(self):
        response = self.client.post("/api/register/",data={'username':"bob",'email':"bob@abcd.com" ,"password":"123456"},follow=True)
        response = response.json()
        self.assertEqual(response["status"], "success")

        response = self.client.post("/api/register/",data={'username':"bob",'email':"bobby@abcd.com" ,"password":"123456"},follow=True)
        response = response.json()
        self.assertEqual(response["status"], "fail")

        bob = User.objects.get(username="bob")
        self.assertEqual(bob.username, "bob")
        self.assertEqual(bob.email, "bob@abcd.com")
    
    def test_api_cant_upload_without_login(self):
        img1 = SimpleUploadedFile(name='1.jpg', content=open("C:/Users/B/Desktop/NoteSpace/static/TestNotes/Math/IMG_0815.JPG", 'rb').read(), content_type='image/jpeg') 
        response = self.client.post("/api/upload/",data={'name':"noteNo1",'guestname':'boy','desc':'','imagefiles':[img1]},follow=True)
        response = response.json()
        self.assertEqual(response["status"], "fail")

    def test_api_can_add_review(self):
        sample_note = Note()
        sample_note.name = 'testing note'
        sample_note.save()
        note_id = sample_note.id

        response = self.client.post("/api/addreview/",
                    data={'note_id':str(note_id),'author':'bobby','text':'very good','score':'5'},
                    follow=True)
        self.assertEqual(response.json()["status"], "success")
        
        review = Review.objects.filter(author='bobby')[0]
        self.assertEqual(review.note, sample_note)
        self.assertEqual(review.author, 'bobby')
        self.assertEqual(review.text, 'very good')
        self.assertEqual(review.score, 5)

    def test_api_can_auth_user(self):
        User.objects.create_user("george", "george@abcd.com", "1234")
        
        response = self.client.post("/api/login/",data={'username':"george", "password":"abcd"},follow=True)
        response = response.json()
        self.assertEqual(response["status"], "fail")

        response = self.client.post("/api/login/",data={'username':"george", "password":"1234"},follow=True)
        response = response.json()
        self.assertEqual(response["status"], "success")
        


class NoteModelTest(LiveServerTestCase):
    def setUp(self):
        pass

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
        img1.image = SimpleUploadedFile(name='1.jpg', content=open("C:/Users/B/OneDrive/Documents/61FC8C1A-D1FE-4D09-ABE4-BE1689D03C8E.jpg", 'rb').read(), content_type='image/jpeg') 
        img1.save()

        img2 = Image()
        img2.index = 2
        img2.note = n
        img2.image = SimpleUploadedFile(name='1.jpg', content=open("C:/Users/B/OneDrive/Documents/61FC8C1A-D1FE-4D09-ABE4-BE1689D03C8E.jpg", 'rb').read(), content_type='image/jpeg')
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
        time.sleep(1)
        self.assertLess(note1.upload_time, datetime.datetime.now())

    def test_database_can_search_by_similar(self):
        from django.db.models import Q

        note1_namesearch = Note()
        note1_namesearch.name = "django"
        note1_namesearch.save()

        note2_descsearch = Note()
        note2_descsearch.name = "writing unit test"
        note2_descsearch.desc = "for django"
        note2_descsearch.save()


        Tag_django = Tag()
        Tag_django.title = "django"
        Tag_django.save()

        note3_tagsearch = Note()
        note3_tagsearch.name = "Html Template Tags"
        note3_tagsearch.save() 
        note3_tagsearch.tags.add(Tag_django)
        note3_tagsearch.save()

        note4_ownersearch = Note()
        note4_ownersearch.name = "FAQ"
        note4_ownersearch.owner = "Django official"
        note4_ownersearch.save()

        search_result = list(Note.objects.filter(Q(name__icontains="django") | 
                                            Q(desc__icontains="django") |
                                            Q(tags__title__icontains="django") |
                                            Q(owner__icontains="django")
                                            ) )
        print(search_result)
        
        self.assertGreaterEqual(len(search_result), 4)

        self.assertIn(note1_namesearch, search_result)
        self.assertIn(note2_descsearch, search_result )
        self.assertIn(note3_tagsearch,  search_result)
        self.assertIn(note4_ownersearch, search_result)

        search_result = Note.objects.filter(name__trigram_similar="django").filter(desc__trigram_similar="django")
    

    def test_can_store_and_get_review(self):
        n = Note()
        n.save()

        review1 = Review()
        review1.note = n
        review1.author = "Smith"
        review1.score = 5
        review1.text = "very good"
        review1.save()

        self.assertEqual(n.reviews.all().count(), 1)
        self.assertIn(review1, n.reviews.all())

        self.assertEqual(n.reviews.all()[0], review1)
        self.assertEqual(n.reviews.all()[0].author, "Smith")
        self.assertEqual(n.reviews.all()[0].text, "very good")

    

    

        

