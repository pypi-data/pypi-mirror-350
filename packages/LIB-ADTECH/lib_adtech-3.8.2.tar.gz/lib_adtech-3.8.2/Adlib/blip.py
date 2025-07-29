import time
from selenium.webdriver import Chrome


def ficarOnline(blip: Chrome):
    try:
        ficarOnline = blip.find_element('id' , 'set-online-btn')
        ficarOnline.click()
        time.sleep(5)
    except:
        print("ja esta online")
        time.sleep(5)