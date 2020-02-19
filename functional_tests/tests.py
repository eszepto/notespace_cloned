from django.test import LiveServerTestCase
from django.test import Client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
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

        testNote = Note()
        testNote.name = "Basic Economics"
        testNote.subject = "Economics"
        testNote.desc = "This note is about demands, suplies and how market works."
        testNote.owner = "Susan"
        publishTime = datetime.datetime.now()
        testNote.save()
        # self.browser = webdriver.Edge()
        self.browser = webdriver.Firefox()
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
    # She notices the filter bar and filters the newest.
    # She chooses the most relative note.
    # She clicks on the thumbnail, the page update then the lecture appears​.
        self.assertIn("Basic Economics", [item.text for item in search_results])
    # She notices the lecture note name, owner name, and description.
        note = self.browser.find_element_by_id('note')
        self.assertIn('Basic Economics', [link.text for link in note.find_elements_by_tag_name('h1')])
        self.assertIn(('Published %s',publishTime), [link.text for link in note.find_elements_by_tag_name('span')])
        self.assertIn('By Susan', [link.text for link in note.find_elements_by_tag_name('span')])
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
        file_input_button.send_keys("../static/TestNotes/Math/IMG_0815.JPG")
        file_input_button.send_keys("../static/TestNotes/Math/IMG_0816.JPG")
        file_input_button.send_keys("../static/TestNotes/Math/IMG_0817.JPG")
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