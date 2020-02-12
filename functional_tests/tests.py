from django.test import LiveServerTestCase
from django.test import Client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import WebDriverException
from notes.models import Note,Image
class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
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

        self.browser = webdriver.Edge()
    def tearDown(self):
        pass
        self.browser.quit()

    def wait_for_page_update(self):
        time.sleep(1)
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
    # Tina has heard about a very amazing online lecture note app.
    # So she goes to check out its homepage.
        self.browser.get(self.live_server_url)
        
        # She notices the page title ,
        self.assertIn('NoteSpace', self.browser.title)
        header_text = self.browser.find_element_by_link_text('NoteSpace').text 
        self.assertIn('NoteSpace', header_text)
    
        button = self.browser.find_element_by_tag_name('body')
        inputbox = button.find_elements_by_tag_name('input')
        self.assertEqual(inputbox.get_attribute('value'), 'Search')
    
   
  

    def test_user_can_search(self):
        self.browser.get(self.live_server_url)
        self.wait_for_page_update()
        inputbox = self.browser.find_element_by_tag_name('input')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Search')
    # # She types “django” into a text box 
    # # When she hits the enter, the page refreshs and the lectures about 'django' appear.
        inputbox.send_keys('django')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_page_update()
        search_results = self.browser.find_elements_by_tag_name("a")
        webpage = self.browser.find_element_by_tag_name("body")
        self.assertIn("searching for 'django'", webpage.text)
        self.assertIn("django", [item.text for item in search_results])
        self.assertIn("djang", [item.text for item in search_results])
        self.assertIn("writing unit test", [item.text for item in search_results])
    
    # # She chooses one of many lectures to find out.
    # # She clicks on the thumbnail, the page update then the lecture appears​.
    
    # # She notices the lecture name, owner name, description, arrow buttons and logo button.
    
    # # When she clicks on arrow button, then the next page of lecture appear​.
    
    # # She reads all the page after that she clicks on homepage button.
    # # Suddenly the page redirect to the homepage. 


    def test_user_can_upload(self):
    # She notices the page title ,upload button and also many lecture thumbnails.
    # She is invited to click on upload button.
        self.browser.get(self.live_server_url)
        self.wait_for_page_update()

        upload_btn = self.browser.find_element_by_id("upload_btn")
        self.assertTrue(upload_btn)
        
    # She click on upload button.
        upload_btn.send_keys(Keys.ENTER)
        self.wait_for_page_update()
    # It's bring her to upload lecture page.
        self.assertIn('Upload the Lecture note', self.browser.title)
        button_publish = self.browser.find_element_by_id('btnPublish')
        self.assertTrue(button_publish)

    # There is button for uploading the pictures of lecture. 
        file_input_button = self.browser.find_element_by_id("file_input")
       
    # She clicks and upload them.
        self.browser.execute_script("arguments[0].style.display = 'block';", file_input_button)
        
        file_input_button.send_keys("C:/Users/B/OneDrive/Documents/231B23AC-F1DB-4A2B-A922-29CC47749436.jpg")
        file_input_button.send_keys("C:/Users/B/OneDrive/Documents/61FC8C1A-D1FE-4D09-ABE4-BE1689D03C8E.jpg")
        
    # There is the box for lecture name ,subject, description and owner name​.
        lectureNameTextBox = self.browser.find_element_by_id('LectureName')
        subjectTextBox = self.browser.find_element_by_id('Subject')
        descriptionTextArea = self.browser.find_element_by_id('Description')
        writerNameTextBox = self.browser.find_element_by_id('WriterName')
        
    # She fills the name and details into the box and set owner name as Tina.
      
        lectureNameTextBox.send_keys('Form interaction')
        subjectTextBox.send_keys('Django Basic')
        descriptionTextArea.send_keys('made with love and care')
        writerNameTextBox.send_keys('Tina')
    # She click on publish button
        button_publish.send_keys(Keys.ENTER)
        
    # the page refresh then she see her lecture on the homepage.
        self.wait_for_page_update()
        main = self.browser.find_element_by_id('main')
        self.assertIn('Form interaction',
        [link.text for link in main.find_elements_by_tag_name('a')])
        self.fail("test_user_can_upload OK!")


    # # She chooses one of many lectures to find out.
    # # She clicks on the thumbnail, the page update then the lecture appears​.
    # # She notices the lecture name, owner name, description, arrow buttons and logo button.
    # # When she clicks on arrow button, then the next page of lecture appear​.
    # # She reads all the page after that she clicks on homepage button.    
    # # Suddenly the page redirect to the homepage. 
    # # Satisfied, Tina goes back to sleep.
      
      



   

