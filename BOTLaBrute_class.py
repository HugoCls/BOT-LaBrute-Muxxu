import requests
import pandas as pd
from bs4 import BeautifulSoup

from Brute_class import Brute
from data.http_parameters import login_headers, login_data, twinoid_headers, twinoid_url, login_url, brute_headers, brute_action_headers
from Database_class import Database

labrute_scheme = "http:"
labrute_domain = "labrute.muxxu.com"

twinoid_scheme = "https:"
twinoid_domain = "twinoid.com"

database = Database()

class BOTLaBrute:
    def __init__(self):
        print("Connecting & getting cookies..")
        self.initiate_cookies()

        self.connected = True
        
        print("Getting brutes from fronted")
        self.brutes = self.get_brutes()

    def run(self):        

        print("Loop on brutes")
        for id in self.brutes:
            brute = self.brutes[id]

            brute.update_dependencies(self)

            brute.show()
            
            brute.detail = True
            while True:
                brute.loop()
                print('\n')
                if brute.healed and brute.payer:
                    break
            break
            print('\n')
            

    def initiate_cookies(self):
        
        endpoint = "bar/view?lang=fr;chk=e478ae8600d5be76bae65ee279425298;ver=397;infos=n;ch=d41d8cd98f00b204e9800998ecf8427e;tz=-60;fver=100.0.0;jsm=1;url=%2F;host=labrute.muxxu.com;proto=http%3A"
        
        r = requests.get(url=f"{twinoid_scheme}//{twinoid_domain}/{endpoint}", headers=twinoid_headers)
        
        if r.status_code != 200:
            raise ValueError(f"Failed to get '{twinoid_scheme}//{twinoid_domain}/{endpoint}', check connexion")
        
        cookies = requests.utils.dict_from_cookiejar(r.cookies)

        endpoint = "user/login"
        
        login_data['sid'] = cookies['tw_sid']
        #login_headers['Cookie'] = cookies['tw_sid']
        
        r = requests.post(url=f"{twinoid_scheme}//{twinoid_domain}/{endpoint}", headers=login_headers, cookies=cookies, data=login_data)

        if r.status_code not in [200,201]:
            raise ValueError(f"Failed to login to '{twinoid_scheme}//{twinoid_domain}/{endpoint}', check credentials")

        soup=BeautifulSoup(r.text,'html.parser')

        for i in range(len(soup.find_all('input'))):
            if soup.find_all('input')[i]['name']=="url":
                url = soup.find_all('input')[i]['value']
                break
        
        r = requests.get(url, headers=brute_headers)

        new_cookies = cookies | requests.utils.dict_from_cookiejar(r.cookies)

        if "tw_sid" in new_cookies and "sid" in new_cookies:
            self.cookies = new_cookies
        else:
            raise ValueError(f"Failed to login to '{twinoid_scheme}//{twinoid_domain}/{endpoint}', check credentials")

    def get_brutes(self):
        
        endpoint = "team"
        
        r = requests.get(f"{labrute_scheme}//{labrute_domain}/{endpoint}", cookies=self.cookies)
        
        if r.status_code not in [200,201]:
            raise ValueError(f"Failed to get team to '{labrute_scheme}//{labrute_domain}/{endpoint}', check connexion")
        
        soup=BeautifulSoup(r.text,'html.parser')
        
        brutes = {}

        soup_brutes = soup.find_all('td',class_="sheet")
        
        for brute in soup_brutes:
            id = brute.find_all('a')[0]['href'].strip('/b/')
            name = brute.select('h2 > a')[0].text
            level = brute.find_all('p')[0].text.strip(' ')
            hps = brute.find_all('p')[1].text.strip(' Vie ')
            strength = brute.find_all('p')[2].text.strip(' Force ')
            agility = brute.find_all('p')[3].text.strip(' Agilité ')
            rapidity = brute.find_all('p')[4].text.strip(' Rapidité ')
            
            brutes[id] = Brute(self, id, name, level, hps, strength, agility, rapidity)

        return brutes