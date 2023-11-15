from main.models import Site, Link
from django.core.management.base import BaseCommand, CommandError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time 
from ippanel import Client
from django.core.mail import send_mail

api_key = "qsVtNKDEKtFZ9wgS4o1Vw81Pjt-C3m469UJxCsUqtBA="

sms = Client(api_key)


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
        removelist = []
        for item in Link.objects.filter(site = Site.objects.get(name = 'modiseh'), id = 204):
            try:
                if item.size:
                    driver.get(item.link)
                    a = driver.find_elements(By.CLASS_NAME, "swatch-option")
                    if not item.sizes:
                        if len(a):
                            list = []
                            for elem in a:
                                list.append(elem.get_attribute('innerHTML'))
                            item.sizes = list
                            item.save()
                        else:
                            removelist.append('- ' + item.link)
                    else:
                        list = []
                        for elem in a:
                            list.append(elem.get_attribute('innerHTML'))
                        for elem in item.sizes:
                            if not elem in list:
                                removelist.append('- ' + elem + ' ' + item.link)
                        item.sizes = list
                        item.save()
                    if not len(a):
                        if item.have == True:
                            item.have = False
                            item.save()
                            removelist.append('- ' + item.link)
                    else:
                        item.have = True
                        item.save()
                else:
                    a = driver.find_elements(By.ID, "product_page_sticky_add_to_cart_button")
                    if not len(a):
                        if item.have == True:
                            item.have = False
                            item.save()
                            removelist.append('- ' + item.link)
                    else:
                        item.have = True
                        item.save()

            except:
                pass
            time.sleep(0.5)
        text = ''
        for item in removelist:
            text = text + item + '\n'
        send_mail( 'subject', 'list: \n' + text, 'armansaheb@devsduel.ir', ['armansaheb@gmail.com'] )
        '''
        message_id = sms.send(
            "+983000505",
            ["989123873503", "09183553490"],
            text,
            "description"
        )
        '''
        driver.close()