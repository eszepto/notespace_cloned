from selenium import webdriver
import unittest
import time

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()


    def test_can_find_homepage(self):
        self.browser.get('http://localhost:8000/')
# Tina has heard about a very amazing online lecture note app.
# So she goes to check out its homepage.
        self.assertIn('Django', self.browser.title)
        time.sleep(3)
        self.fail('Finish the test')

"""
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

# There is button for uploading the pictures of lecture, she clicks and upload them.
# There is the box for lecture name ,details and owner name​.
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
# The upload completed, the page refresh then she see her lecture on the homepage.
        self.assertIn('lecture')


​    def test_user_can_search(self):
        button = self.browser.find_element_by_id('')
        inputbox = button.find_elements_by_tag_name('input')
        self.assertEqual(inputbox.get_attribute('value'), 'Search')
# She types “computer” into a text box (Tina's major is computer engineering).
# When she hits the enter, the page refresh and the lectures about computer appear.
        time.sleep(1)
        inputbox.send_keys('computer')

        time.sleep(1)
        inputbox.click() 
# She chooses one of many lectures to find out.
# She click on the thumbnail the page update and the lecture appear​.
        self.assertIn('lecture')
# She notices the arrow buttons and home button.
# When she clicks on arrow button, then the next page of lecture appear​.
        inputbox.send_keys(next)
# Satisfied, Tina goes back to sleep
        time.sleep(3)
        self.browser.quit()

"""
if __name__ == '__main__':
    unittest.main(warnings='ignore')
​
