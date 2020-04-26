import time
import datetime

from django.test import LiveServerTestCase
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from notes.models import Note,Image



class NewVisitorTest(LiveServerTestCase):
    publishTime = ""
    def setUp(self):
        welcomeNote = Note()
        welcomeNote.name = "Welcome to Note Space!"
        welcomeNote.desc = "Introduction and Quick guide"
        welcomeNote.owner = "Note Space Team"
        welcomeNote.save()

        econNote = Note()
        econNote.name = "Basic Economics"
        econNote.subject = "Economics"
        econNote.desc = "This note is about demands, suplies and how market works."
        econNote.owner = "Susan"
        econNote.save()

        img1 = Image()
        img1.index = 1
        img1.note = econNote
        img1.image = SimpleUploadedFile(name='IMG_0809.JPG', content=open("C:/Users/B/Desktop/NoteSpace/static/TestNotes/Econ/IMG_0809.JPG", 'rb').read(), content_type='image/jpeg') 
        img1.save()

        img2 = Image()
        img2.index = 2
        img2.note = econNote
        img2.image = SimpleUploadedFile(name='IMG_0810.JPG', content=open("C:/Users/B/Desktop/NoteSpace/static/TestNotes/Econ/IMG_0810.JPG", 'rb').read(), content_type='image/jpeg') 
        img2.save()

        img3 = Image()
        img3.index = 3
        img3.note = econNote
        img3.image = SimpleUploadedFile(name='IMG_0811.JPG', content=open("C:/Users/B/Desktop/NoteSpace/static/TestNotes/Econ/IMG_0811.JPG", 'rb').read(), content_type='image/jpeg') 
        img3.save()

        img4 = Image()
        img4.index = 4
        img4.note = econNote
        img4.image = SimpleUploadedFile(name='IMG_0812.JPG', content=open("C:/Users/B/Desktop/NoteSpace/static/TestNotes/Econ/IMG_0812.JPG", 'rb').read(), content_type='image/jpeg') 
        img4.save()

        User.objects.create_user("smith", "smith@abcd.com", "1234") 
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_page_update(self):
        time.sleep(2)
        MAX_WAIT = 16
        start_time = time.time()
        while True:  
            try:
                header = self.browser.find_element_by_tag_name('html')
                return  True
            except (AssertionError, WebDriverException) as e:  
                if time.time() - start_time > MAX_WAIT:  
                    raise e  
                time.sleep(0.5) 

    def test_user_can_checkout_homepage(self):
        # Tina is a Highschool student and tries to find another way to study for her exam. 
        # She has heard about a very amazing online lecture note app, named Note Space, from her best friend.
        # So she goes to check out its homepage.
        self.browser.get(self.live_server_url)
        self.wait_for_page_update()
        # She notices the page title is "Note Space"
        self.assertIn('NoteSpace', self.browser.title)
        

    def test_user_can_search(self):
        self.browser.get(self.live_server_url)
        self.wait_for_page_update()
        # and then she notices a search field.
        inputbox = self.browser.find_element_by_tag_name('input')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Search')
        # She types the keyword "Economics" into a text box 
        inputbox.send_keys('Economics')
        inputbox.send_keys(Keys.ENTER)
        # When she hits the enter, the page refreshs and the lectures about "Economics" appear.
        self.wait_for_page_update()
        
        search_results = self.browser.find_elements_by_tag_name("a")
        
        webpage = self.browser.find_element_by_tag_name("body")
        self.assertIn("searching for 'Economics'", webpage.text)
        self.assertIn("Basic Economics", [item.text for item in search_results])
        # She notices the filter bar and filters the newest.

        
    def test_user_can_view_note(self):
        self.browser.get(self.live_server_url)
        self.wait_for_page_update()
        
        # She clicks on the thumbnail, the page update then the lecture appears​.
        e = self.browser.find_element_by_partial_link_text('Basic Economics')
        self.browser.execute_script("arguments[0].click();", e)
        self.wait_for_page_update()

        # She notices the lecture note name, owner name, and description.
        self.assertIn('Basic Economics', [link.text for link in self.browser.find_elements_by_tag_name('h1')])
        #self.assertIn( 'Published %s'%(publishTime), [link.text for link in note.find_elements_by_tag_name('span')])
        self.assertIn('By Susan', [link.text for link in self.browser.find_elements_by_tag_name('span')])   
        
        
        # She found left-right arrow buttons, note image between that and dots in the bottom.
        left_arrow  = self.browser.find_element_by_class_name('prev')
        self.assertTrue(left_arrow)
        right_arrow = self.browser.find_element_by_class_name('next')
        self.assertTrue(right_arrow)
        dots        = self.browser.find_elements_by_class_name('dot')
        self.assertTrue(dots)

        flag9 = False
        flag10 = False
        flag11 = False
        flag12 = False
        sources = [img.get_attribute("src")  for img in self.browser.find_elements_by_class_name('note_img')]
        for src in sources:
            if 'IMG_0809' in src:
                flag9 = True
            if 'IMG_0810' in src:
                flag10 = True
            if 'IMG_0811' in src:
                flag11 = True
            if 'IMG_0812' in src:
                flag12 = True

        self.assertTrue(flag9)
        self.assertTrue(flag10)
        self.assertTrue(flag11)
        self.assertTrue(flag12)

        # When she clicks on the right arrow button, then the next page of the lecture appears.
        # And she clicks on the left arrow button, then the previous page appears.
        

    def test_user_can_upload(self):
        self.browser.get(self.live_server_url)
        self.wait_for_page_update()
        
        login_text = self.browser.find_element_by_link_text("login")
        self.browser.execute_script("arguments[0].click();", login_text)
        self.wait_for_page_update()

        username_box = self.browser.find_element_by_id("username")
        password_box = self.browser.find_element_by_id("password")
        submit_button = self.browser.find_element_by_id("submit")

        username_box.send_keys("smith")
        password_box.send_keys("1234")
        submit_button.click()
        self.wait_for_page_update()

        #-------------------
        
        # She found the upload button.
        upload_btn = self.browser.find_element_by_id("upload_btn")
        self.assertTrue(upload_btn)
        # She clicks on the upload button.
        upload_btn.send_keys(Keys.ENTER)
        self.wait_for_page_update()
        # It's bring her to upload the lecture note page.
        # She notices that title is "Upload the Lecture note".
        self.assertIn('Upload the Lecture note', self.browser.title)
        # There is a browse button and all the text fields.
        
        file_input_button = self.browser.find_element_by_id("file_input")

        lectureNameTextBox = self.browser.find_element_by_id('LectureName')
        subjectTextBox = self.browser.find_element_by_id('Subject')
        descriptionTextArea = self.browser.find_element_by_id('Description')
        writerNameTextBox = self.browser.find_element_by_id('WriterName')
        
        # She clicks browse button and upload her note.
        self.browser.execute_script("arguments[0].style.display = 'block';", file_input_button)
        file_input_button.send_keys("C:\\Users\\B\\Desktop\\NoteSpace\\static\\TestNotes\\Math\\IMG_0815.JPG")
        file_input_button.send_keys("C:\\Users\\B\\Desktop\\NoteSpace\\static\\TestNotes\\Math\\IMG_0816.JPG")
        file_input_button.send_keys("C:\\Users\\B\\Desktop\\NoteSpace\\static\\TestNotes\\Math\\IMG_0817.JPG")
        
        # She fills the name and details into the box and sets the owner's name as Tina.
        lectureNameTextBox.send_keys('Elementary Logic')
        subjectTextBox.send_keys('Mathematics')
        descriptionTextArea.send_keys('The topics are Argument, Symbolic Logic, Tautology and Contradictory Proposition')
        writerNameTextBox.send_keys('Tina')
        
        # She sees and clicks on publish button.
        button_publish = self.browser.find_element_by_id('btnPublish')
        self.assertTrue(button_publish)
        button_publish.send_keys(Keys.ENTER)
        
        # It goes back to homepage.
        self.wait_for_page_update()
        
        # She found her note and the first page of her note is a thumbnails.
        self.assertIn('Elementary Logic', [link.text for link in self.browser.find_elements_by_class_name("card-title")])
        
        # She check out her note.
        e=self.browser.find_element_by_partial_link_text('Elementary Logic')
        self.browser.execute_script("arguments[0].click();", e)
        self.wait_for_page_update()

        # Then she found that the owner name is her name
        self.assertIn('By Tina', [link.text for link in self.browser.find_elements_by_class_name('owner')])
        
        # and click on the arrow button to check that the order is correct.
        
        
        flag15 = False
        flag16 = False
        flag17 = False
        sources = [img.get_attribute("src")  for img in self.browser.find_elements_by_class_name('note_img')]
        for src in sources:
            if 'IMG_0815' in src:
                flag15 = True
            if 'IMG_0816' in src:
                flag16 = True
            if 'IMG_0817' in src:
                flag17 = True

   
        self.assertTrue(flag15)
        self.assertTrue(flag16)
        self.assertTrue(flag17)

        # She proud of herself and close the browser.

    def test_user_can_add_and_view_review(self):
        self.browser.get(self.live_server_url)
        self.wait_for_page_update()

        e = self.browser.find_element_by_partial_link_text('Basic Economics')
        self.browser.execute_script("arguments[0].click();", e)
        self.wait_for_page_update()

        # She notices the lecture note name, owner name, and description.
        self.assertIn('Basic Economics', [link.text for link in self.browser.find_elements_by_tag_name('h1')])
        #self.assertIn( 'Published %s'%(publishTime), [link.text for link in note.find_elements_by_tag_name('span')])
        self.assertIn('By Susan', [link.text for link in self.browser.find_elements_by_tag_name('span')])   
        
        # She write some review
        star4 = self.browser.find_element_by_id("star4")
        author = self.browser.find_element_by_id("author_name")
        textbox = self.browser.find_element_by_id("text")
        post_button = self.browser.find_element_by_id("submit")
        
        star4.click()
        author.send_keys("Jane")
        textbox.send_keys("Great!")
        # She post the review
        post_button.click()
        self.wait_for_page_update()
        
        # the page refresh and She see her review appear on the website
        self.browser.refresh()
        self.assertIn("Jane", [p.text for p in self.browser.find_elements_by_tag_name('p')])
        self.assertIn("score:4.0", [p.text for p in self.browser.find_elements_by_tag_name('p')])
        self.assertIn("Great!", [p.text for p in self.browser.find_elements_by_tag_name('p')])


    def test_user_can_register_and_login(self):
        self.browser.get(self.live_server_url)
        self.wait_for_page_update()
        self.assertIn("register", [a.text for a in self.browser.find_elements_by_tag_name("a")])
        register_text = self.browser.find_element_by_link_text("register")
        self.browser.execute_script("arguments[0].click();", register_text)
        self.wait_for_page_update()
        username_box = self.browser.find_element_by_id("username")
        email_box = self.browser.find_element_by_id("email")
        password_box = self.browser.find_element_by_id("password")
        repassword_box = self.browser.find_element_by_id("re-password")
        submit_button = self.browser.find_element_by_id("submit")

        username_box.send_keys("john")
        email_box.send_keys("john@abc.com")
        password_box.send_keys("1234")
        repassword_box.send_keys("1234")
        submit_button.click()
        self.wait_for_page_update()

        self.assertIn("Register successful!", [h.text for h in self.browser.find_elements_by_tag_name("h2")])
        self.assertIn("login here", [a.text for a in self.browser.find_elements_by_tag_name("a")])

        login_text = self.browser.find_element_by_link_text("login here")
        self.browser.execute_script("arguments[0].click();", login_text)
        self.wait_for_page_update()

        username_box = self.browser.find_element_by_id("username")
        password_box = self.browser.find_element_by_id("password")
        submit_button = self.browser.find_element_by_id("submit")

        username_box.send_keys("john")
        password_box.send_keys("1234")
        submit_button.click()
        self.wait_for_page_update()

        self.assertIn("Hello, john", [p.text for p in self.browser.find_elements_by_tag_name("p")])


    

        
