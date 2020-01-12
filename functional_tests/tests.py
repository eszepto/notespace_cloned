from django.test import LiveServerTestCase
from django.test import Client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import WebDriverException

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
    def tearDown(self):
        pass
        self.browser.quit()

    def wait_for_page_redirect(self):
        MAX_WAIT = 5
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
        #upload button 
        upload_btn = self.browser.find_elements_by_id('upload_btn')[0]
        self.assertTrue(upload_btn)

        #and also many lecture thumbnails.
        pass
        
        # She is invited to click on upload button.
        upload_btn.send_keys(Keys.ENTER)
        time.sleep(2)
        # It's bring her to upload lecture page.
        self.assertIn('Upload', self.browser.title)




# There is button for uploading the pictures of lecture, she clicks and upload them.
# There is the box for lecture name ,details and owner name​.
# She fills the name and details into the box and set owner name as Tina.
# The upload completed, the page refresh then she see her lecture on the homepage.
# She types “computer” into a text box (Tina's major is computer engineering).
# When she hits the enter, the page refresh and the lectures about computer appear.
# She chooses one of many lectures to find out.
# She click on the thumbnail the page update and the lecture appear​.
# She notices the arrow buttons and home button.
# When she clicks on arrow button, then the next page of lecture appear​.
# Satisfied, Tina goes back to sleep

