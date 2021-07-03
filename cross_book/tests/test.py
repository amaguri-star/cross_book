from django.test import LiveServerTestCase
from django.urls import reverse_lazy
from selenium.webdriver.chrome.webdriver import WebDriver


class TestLogin(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(executable_path='/Users/nakamuraryusei/chromedriver')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('http://localhost:8000' + str(reverse_lazy('account_login')))
        email_input = self.selenium.find_element_by_name("login")
        email_input.send_keys('ryusei1597@gmail.com')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('adminpass')
        self.selenium.find_element_by_class_name('submit-button').click()

        self.assertEqual('ホーム', self.selenium.title)