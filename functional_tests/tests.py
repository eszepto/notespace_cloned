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
    # Tina is a Highschool student and tries to find another way to study for her exam. 
    # She has heard about a very amazing online lecture note app, named Note Space, from her best friend.
    # So she goes to check out its homepage.
        self.browser.get(self.live_server_url)
    # She notices the page title is "Note Space"
        self.assertIn('NoteSpace', self.browser.title)
    # and then she notices a search field.
        inputbox = button.find_elements_by_tag_name('input')
        self.assertEqual(inputbox.get_attribute('value'), 'Search')


    def test_user_can_search(self):
        self.browser.get(self.live_server_url)
        self.wait_for_page_update()
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
        self.assertIn("Economics", [item.text for item in search_results])
    # She notices the filter bar and filters the newest.
    # She chooses the most relative note.


    def test_user_can_view_the_note(self):
    # She clicks on the thumbnail, the page update then the lecture appears​.
    
    # She notices the lecture note name, owner name, and description.

    # She found left-right arrow buttons, note image between that and dots in the bottom.

    # When she clicks on the right arrow button, then the next page of the lecture appears​.

    # And she clicks on the left arrow button, then the previous page appears.

    # She reads all the pages after that she found that the logo is clickable.
    # She clicks on it and The page suddenly redirects to the homepage.


    def test_user_can_upload(self):
        self.browser.get(self.live_server_url)
        self.wait_for_page_update()
    # She notices the welcome note that invite her to upload her lecture note.

    # She realizes that she has a note from the last exam.
    # And she's proud to share it to public.
        
    # She knew how to upload her note from the welcome note.
    # She found the upload button.
        upload_btn = self.browser.find_element_by_id("upload_btn")
        self.assertTrue(upload_btn)
    # She clicks on the upload button quickly.
        upload_btn.send_keys(Keys.ENTER)
        self.wait_for_page_update()
    # It's bring her to upload the lecture note page.
    # She notices that title is "Upload the Lecture note".
        self.assertIn('Upload the Lecture note', self.browser.title)
    # There is a browse button 
        file_input_button = self.browser.find_element_by_id("file_input")
    # and all the text fields.
        lectureNameTextBox = self.browser.find_element_by_id('LectureName')
        subjectTextBox = self.browser.find_element_by_id('Subject')
        descriptionTextArea = self.browser.find_element_by_id('Description')
        writerNameTextBox = self.browser.find_element_by_id('WriterName')
    # She clicks browse button and upload her note.
        self.browser.execute_script("arguments[0].style.display = 'block';", file_input_button)
        file_input_button.send_keys("C:/Users/B/OneDrive/Documents/231B23AC-F1DB-4A2B-A922-29CC47749436.jpg")
        file_input_button.send_keys("C:/Users/B/OneDrive/Documents/61FC8C1A-D1FE-4D09-ABE4-BE1689D03C8E.jpg")
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
        main = self.browser.find_element_by_id('main')
    # She found her note and the first page of her note is a thumbnails.
        self.assertIn('Elementary Logic', [link.text for link in main.find_elements_by_tag_name('a')])
    # She check out her note.
    # Then she found that the owner name is her name

    # and click on the arrow button to check that the order is correct.

    # She proud of herself and close the browser.
        self.fail("test_user_can_upload OK!")