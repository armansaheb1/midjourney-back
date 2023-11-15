from main.models import Site, Link
from django.core.management.base import BaseCommand, CommandError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time 

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


class Command(BaseCommand):

    def handle(self, *args, **options):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        for item in Link.objects.filter(site = Site.objects.get(name = 'modiseh')):
            try:
                if item.size:
                    driver.get(item.link)
                    a = driver.find_elements(By.CLASS_NAME, "swatch-option")
                    if not item.sizes:
                        list = []
                        for elem in a:
                            list.append(elem.get_attribute('innerHTML'))
                        item.sizes = list
                        item.save()
                    else:
                        list = []
                        for elem in a:
                            list.append(elem.get_attribute('innerHTML'))
                        for elem in item.sizes:
                            if not elem in list:
                                print('- ' + elem)
                        item.sizes = list
                        item.save()
                else:
                    a = driver.find_elements(By.ID, "product_page_sticky_add_to_cart_button")
                    if not len(a):
                        print('- ' + item.link)
            except:
                pass
            time.sleep(0.5)
        driver.close()