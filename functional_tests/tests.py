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




    def test_user_can_upload(self):
# She notices the page title ,upload button and also many lecture thumbnails.
        upload_link = self.browser.find_element_by_link_text('')
        self.assertEqual(upload_link.get_attribute('href'), 'http://localhost:8000/**/')
        time.sleep(1)
        place_link.click()
# She is invited to click on upload button.
# It's bring her to upload lecture page.
        button = self.browser.find_element_by_id('')
        inputbox = button.find_elements_by_tag_name('input')

# There is button for uploading the pictures of lecture. 
# She clicks and upload them.
# There is the box for lecture name ,subject, description and owner name​.
        time.sleep(1)
        inputbox.send_pic

        time.sleep(1)
        inputbox.send_keys('name')

        time.sleep(1)
        inputbox.send_keys('detail')
        
# She fills the name and details into the box and set owner name as Tina.
        time.sleep(1)
        inputbox.send_keys('Tina')

        time.sleep(1)
        inputbox.click() 
# She click on publish button, the page refresh then she see her lecture on the homepage.
        self.assertIn('lecture')

    def test_user_can_search(self):
        button = self.browser.find_element_by_id('')
        inputbox = button.find_elements_by_tag_name('input')
        self.assertEqual(inputbox.get_attribute('value'), 'Search')
# She types “computer” into a text box (Tina's program is Sci-Math-Com).
# When she hits the enter, the page refreshs and the lectures about computer appear.
        time.sleep(1)
        inputbox.send_keys('computer')

        time.sleep(1)
        inputbox.click() 
# She chooses one of many lectures to find out.
# She clicks on the thumbnail, the page update then the lecture appears​.
        self.assertIn('lecture')
# She notices the lecture name, owner name, description, arrow buttons and logo button.
# When she clicks on arrow button, then the next page of lecture appear​.
        inputbox.send_keys(next)
# She reads all the page after that she clicks on homepage button.
# Suddenly the page redirect to the homepage. 
# Satisfied, Tina goes back to sleep.
        time.sleep(3)
        self.browser.quit()




