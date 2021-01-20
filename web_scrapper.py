from Screenshot import Screenshot_Clipping
from selenium import webdriver
from getpass import getpass
from sys import platform
from time import sleep
from os import mkdir
import wget
import os


class Scrapper:
    footer_id= 'content_footer'
    navi_id= 'navbar'
    btn_next= 'next_button_link'

    pop_up= 'modal-dialog'
    back_drop= 'modal-backdrop'

    url= 'https://learn.codingdojo.com/signin'
    start_link= 'http://learn.codingdojo.com/m/2/4643/27930'

    def __init__(self, username, pswd, browser):
        super().__init__()
        self.username= username
        self.pswd= pswd
        self.browser= browser
        self.set_driver()

    def set_file_path(self, file_path='test/'):
        if os.path.isdir(file_path):
            self.file_path= file_path
        else:
            mkdir(file_path)
            self.file_path= file_path

    def set_start_url(self, start_link):
        self.start_link= start_link

    def set_driver(self):
        self.driver= webdriver.Firefox() if self.browser == 'Firefox' else webdriver.Chrome()
        self.driver.get(self.url)

    def driver_login(self):
        self.driver.find_element_by_id('enter_email').send_keys(self.username)
        self.driver.find_element_by_id('enter_password').send_keys(self.pswd)
        self.driver.find_element_by_id('login_button').click()
        sleep(3)
        self.remove_nav()

    def start(self):
        self.driver.get(self.start_link)
        self.loop_pages()

    def remove_nav(self):
        self.driver.execute_script("$('#{nav}').attr('hidden',true)".format(nav= self.navi_id))

    def hidden_footer(self, isHidden):
        self.driver.execute_script("$('#{f}').attr('hidden',{b})".format(f=self.footer_id, b=isHidden))

    def end(self):
        self.driver.quit()

    def screen_cap(self):
        full_screen= Screenshot_Clipping.Screenshot()
        file_name = ''
        if os.path.isfile(self.get_cap_name()):
            file_name= self.get_cap_name().replace('.','(copy).')
        else:
            file_name= self.get_cap_name()
        full_screen.full_Screenshot(self.driver, self.file_path, file_name)
        

    def get_cap_name(self):
        _url= self.driver.current_url
        _url= str(_url)[5:].replace('/', '_')
        return _url + '.png'

    def check_modal(self):
        modals= self.driver.find_elements_by_class_name(self.pop_up)
        if len(modals) > 0:
            self.driver.execute_script("$('.{modal}').attr('hidden',true)".format(modal=self.pop_up))
            self.driver.execute_script("$('.{backdrop}').attr('hidden',true)".format(backdrop=self.back_drop))
        else:
            pass


    def loop_pages(self):
        sleep(2)
        btns= self.driver.find_elements_by_class_name(self.btn_next)
        while len(btns) > 0:
            self.check_modal()
            self.remove_nav()
            self.hidden_footer('true')
            sleep(2)
            self.screen_cap()
            sleep(2)
            self.hidden_footer('false')
            sleep(2)
            self.driver.find_element_by_class_name(self.btn_next).click()
            sleep(3)
            btns= self.driver.find_elements_by_class_name(self.btn_next)
            sleep(3)
        print("Last URL Before Ending: {curl}".format(curl=self.driver.current_url))


def browser_check():
    browser_select= input("Select your browser\n1:FireFox\t2:Chrome\n")
    if browser_select != '1' and browser_select != '2':
        browser_check()
    else:
        browser_name= 'Firefox' if browser_select == '1' else 'Chrome'
        driver_path= 'geckodriver.exe' if browser_name == 'Firefox' else 'chromedriver.exe'
        confirm= input('You selected {name} is that correct?\nY/N\n'.format(name=browser_name))
        if confirm == 'y' or confirm == 'yes' or confirm == 'Y' or confirm == 'YES':
            driver_check(driver_path)
            return browser_name
        else:
            browser_check()

def driver_check(driver_path):
    try:
        open(driver_path)
    except IOError:
        print('Web Driver not found...\nDownloading...\n')
        links= system_check()
        wget.download(links[0] if driver_path == 'geckodriver.exe' else links[1])
        print('\nPlease unzip the files and rerun this script.')
        exit(0)

def system_check():
    win_links=[
        'https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-win64.zip',
        'https://chromedriver.storage.googleapis.com/88.0.4324.27/chromedriver_win32.zip'
        ]
    linux_links=[
        'https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz',
        'https://chromedriver.storage.googleapis.com/88.0.4324.27/chromedriver_linux64.zip'
        ]
    osx_links=[
        'https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-macos.tar.gz',
        'https://chromedriver.storage.googleapis.com/88.0.4324.27/chromedriver_mac64.zip'
        ]

    if platform == 'win32':
        return win_links
    elif platform == 'linux' or platform == 'linux2':
        return linux_links
    elif platform == 'darwin':
        return osx_links
    else:
        print('OS error exiting...\nPlease download correct webdriver for your OS.\nPlace the file with this script.')
        exit(0)

def start_link_check(scrapper):
    start= input('Would you like to define a starting point?\n(Y/N)\n')
    if start == 'y' or start == 'yes' or start == 'Y' or start == 'YES':
        start= input('Enter the URL of where to begin:\n')
        scrapper.set_start_url(start)
    else:
        print('Scrapper will use its default starting point.')

if __name__ == "__main__":
    browser= browser_check()

    username= input("Please enter your username:\n")
    mpass= getpass("Enter your password(hidden input to prevent shoulder surfers):\n")
    file_path= input('Enter file path:\n')
    scrapper= Scrapper(username, mpass, browser)
    scrapper.set_file_path(file_path)
    start_link_check(scrapper)
    scrapper.driver_login()
    scrapper.start()

    sleep(3)
    scrapper.end()