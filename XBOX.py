import os
from selenium import webdriver
from inputs import get_gamepad
button = ''
left_active = False
right_active = False
b_active = False
a_active = False
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
os.environ["webdriver.chrome.driver"] = 'X:\chromedriver.exe'
driver = webdriver.Chrome(executable_path='X:\chromedriver.exe', chrome_options=options)
driver.get('http://192.168.1.112:/carcontrol.php')
while 1:
    events = get_gamepad()
    for event in events:
        if event.code == 'BTN_TR':
            button = 'right'

        if event.code == 'BTN_TL':
            button = 'left'

        if event.code == 'BTN_NORTH':
            button = 'B'

        if event.code == 'BTN_SOUTH':
            button = 'A'

    if button == 'A':
        button = ''
        a_active = not a_active
        if a_active == True:
            print("A Down")
            submit_button = driver.find_elements_by_xpath('//*[@id="carbackward"]')[0]
            submit_button.click()

        else:
            print("A Up")
            submit_button = driver.find_elements_by_xpath('//*[@id="carstop"]')[0]
            submit_button.click()

    if button == 'B':
        button = ''
        b_active = not b_active
        if b_active == True:
            print("B Down")
            submit_button = driver.find_elements_by_xpath('//*[@id="carforward"]')[0]
            submit_button.click()

        else:
            print("B Up")
            submit_button = driver.find_elements_by_xpath('//*[@id="carstop"]')[0]
            submit_button.click()



    if button == 'left':
        button = ''
        left_active = not left_active

        if left_active == True:
            print("Left Down")
            submit_button = driver.find_elements_by_xpath('//*[@id="carleft"]')[0]
            submit_button.click()

        else:
            print("Left Up")
            submit_button = driver.find_elements_by_xpath('//*[@id="carstop"]')[0]
            submit_button.click()


    if button == 'right':
        button = ''
        right_active = not right_active


        if right_active == False:
            print("Right Up")
            submit_button = driver.find_elements_by_xpath('//*[@id="carstop"]')[0]
            submit_button.click()

        else:
            print("Right Down")
            submit_button = driver.find_elements_by_xpath('//*[@id="carright"]')[0]
            submit_button.click()

s.close()
