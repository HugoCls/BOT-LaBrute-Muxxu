import requests
from bs4 import BeautifulSoup
import random as rd
from datetime import datetime

from AI import use_model
from data.http_parameters import brute_headers, brute_action_headers
from Database_class import Database

labrute_scheme = "http:"
labrute_domain = "labrute.muxxu.com"

twinoid_scheme = "https:"
twinoid_domain = "twinoid.com"

database = Database()

class Brute:
    def __init__(self, bot, id, name, level, hps, strength, agility, rapidity):
        database.insert_into_database(data = (id, name, None, level, hps, strength, agility, rapidity, None, None, None, None, None))
        self.detail = False
        self.bot = bot
        self.id = id
        self.name = name
        self.healed = False
        self.level = level
        self.hps = hps
        self.strength = strength
        self.agility = agility
        self.rapidity = rapidity
        self.brute_headers = brute_action_headers
        self.brute_headers['Referer'] = f'{labrute_scheme}//{labrute_domain}/b/{self.id}'

    def show(self):
        print(f"id: {self.id}")
        print(f"name: {self.name}")
        print(f"level: {self.level}")
        print(f"hps: {self.hps}")
        print(f"strength: {self.strength}")
        print(f"agility: {self.agility}")
        print(f"rapidity: {self.rapidity}")

    def update_dependencies(self, bot):
        self.bot = bot

    def loop(self):
        #4 injuries 4085909
        self.get_infos()
        
        if not self.bot.connected:
            print('-- Reconnecting --')
            self.bot.initiate_cookies()
        elif self.payer and not self.healed:
            print('-- Healing --')
            """
            if soup.select('#mxcontent > div.box2top > div > div > table')[0].find_all('li')[1].has_attr('class'):
                self.healed = True
            else:
                self.heal()
            """
            self.heal()
        elif self.level_up:
            print('-- Leveling up --')
            self.levelup()
        else:
            print('-- Attacking --')
            #self.get_infos()
            
            #if not soup.select('#mxcontent > div.box2top > div')[0].find_all('span')[0].has_attr('class'):
            ###RETHINK THE ATTACK LOOP
            for i in range(min(self.fxp[1] - self.fxp[0],self.max_injuries - self.blessures)):

                self.attack_brute()
                
                """
                if health!=None:
                    #Get new injuries count
                    self.get_infos()

                    if self.blessures != self.new_blessures:
                        blessures= self.new_blessures
                        win='0'
                        
                    else:
                        win='1'
                        
                    display.add_data(id,health,straight,agility,rapidity,win)
                    
                    attacks+=1

                """
    
    def heal(self):
        endpoint = f'b/{self.id}/heal{self.chk}'
        
        r = requests.get(f"{labrute_scheme}//{labrute_domain}/{endpoint}",cookies=self.bot.cookies,headers=self.brute_headers)

        self.healed = True

    def levelup(self):

        endpoint= f"b/{self.id}/levelup"

        r = requests.get(f"{labrute_scheme}//{labrute_domain}/{endpoint}",cookies=self.bot.cookies,headers=self.brute_headers)

        soup = BeautifulSoup(r.text,'html.parser')
    
        chk = soup.select('#mxcontent > div > ul.learn > li.one > a')[0]['href']
        N = chk.find(';chk')

        self.chk = chk[N:]

        choice1=soup.find_all('li',class_='one')[0].text

        choice2=soup.find_all('li',class_='two')[0].text

        endpoint = f"{self.choose_upgrade(choice1, choice2)}{self.chk}"
        
        self.brute_headers['Refer'] = endpoint

        r = requests.get(f"{labrute_scheme}//{labrute_domain}/{endpoint}", headers=self.brute_headers, cookies=self.bot.cookies)

        del self.brute_headers['Refer']

    def choose_upgrade(self, choice1, choice2):
        if 'Intouchable' or 'Immortel' or 'compétence' or 'Ours' in choice1:
            choice = 0
        elif 'Intouchable' or 'Immortel' or 'compétence' or 'Ours' in choice2:
            choice = 1
        elif 'Force' in choice1:
                choice = 0
        elif 'Force' in choice2:
            choice = 1
        else:
            choice = 0

        return f'b/{self.id}/levelup?c={choice}'

    def get_infos(self):

        endpoint = f"b/{self.id}"

        cookies = {
            'sid': self.bot.cookies['sid'],
            'hcw': '1'
            }

        #brute_action_headers['Referer'] = f"{labrute_scheme}//{labrute_domain}/{endpoint}""
 
        r = requests.get(f"{labrute_scheme}//{labrute_domain}/{endpoint}", cookies=cookies, headers=brute_action_headers)

        if self.id not in r.text:
            print(r.text)
            raise ValueError(f"Failed reach '{labrute_scheme}//{labrute_domain}/{endpoint}', check credentials")

        soup = BeautifulSoup(r.text,'html.parser')

        if 'Maître' in soup.text:
            self.bot.connected = False

        p = soup.text.find('Expérience : ') + len('Expérience : ')
        
        xp = soup.text[p:p+15].replace('Expérience : ','').replace('\r','').replace('\n','').replace('\t','').replace(' ','')

        self.fxp = [int(xp[:xp.find('/')]), int(xp[xp.find('/')+1:])]

        j = soup.text.find('Blessures ') + len('Blessures ')
        
        self.blessures = int(soup.text[j:j+1])

        if 'Payer' in soup.text:
            self.payer = True
            
            chk = soup.select('#mxcontent > div.box2top > div > div > table')[0].find_all('a')[1]['href']
            N = chk.find('?chk')
            self.chk = chk[N:]

        else:
            self.payer = False
        
        if 'niveau' in soup.text:
            self.level_up = True
        else:
            self.level_up = False
            
        N = soup.text.find('Classement')+60

        self.rang = soup.text[N:].replace('\r','').replace('\n','').replace('\t','').split()[0] # A revoir, Regex?

        self.max_injuries = 3 if soup.select('#mxcontent > div.box2top > div')[0].find_all('span')[0].text == '3' else 4

        if self.detail:
            print('-- Dynamic infos --')
            print(f"fxp: {self.fxp}")
            print(f"blessures: {self.blessures}")
            print(f"payer: {self.payer}")
            print(f"healed: {self.healed}")
            print(f"level_up: {self.level_up}")
            print(f"rang: {self.rang}")
            print(f"max_injuries: {self.max_injuries}")
        
        database.insert_into_database(data = (self.id, self.name, self.rang, self.level, self.hps, self.strength, self.agility, self.rapidity, self.fxp[0], self.fxp[1], self.blessures, None, datetime.utcnow() if self.healed else None))
        

    def attack_brute(self):
        endpoint = f'b/{self.id}/train'

        r = requests.get(f"{labrute_scheme}//{labrute_domain}/{endpoint}", cookies=self.bot.cookies, headers=self.brute_headers)

        soup = BeautifulSoup(r.text,'html.parser')
        
        brutes = soup.find_all('td',class_="sheet")

        if len(brutes) >= 2:
            
            win_probability = []

            for brute in brutes:
                p=brute.text.find('Vie ') + len('Vie ')
                health = int(brute.text[p:p+2])
                
                p=brute.text.find('Force ') + len('Force ')
                straight = int(brute.text[p:p+1])
                
                p=brute.text.find('Agilité ') + len('Agilité ')
                agility = int(brute.text[p:p+1])
                
                p=brute.text.find('Rapidité ') + len('Rapidité ')
                rapidity = int(brute.text[p:p+1])

                win_probability.append(use_model([health, straight, agility, rapidity]))

            AI_guess = max(win_probability)

            j = win_probability.index(AI_guess)
            
            id = brutes[j].find_all('a')[0]['href'].strip('/b/')
            
            brute = brutes[j]
            
            self.brute_headers['Referer'] = f"{labrute_scheme}//{labrute_domain}/{endpoint}"
            
            endpoint = f'b/{self.id}/attack?b={id}'
            
            r = requests.get(f"{labrute_scheme}//{labrute_domain}/{endpoint}",headers=self.brute_headers,cookies=self.bot.cookies)

            # Créez un objet Beautiful Soup
            soup = BeautifulSoup(r.text, 'html.parser')

            # Trouvez tous les scripts dans la page
            scripts = soup.find_all('script')

            # Parcourez les scripts pour trouver ceux contenant "FlashVars"
            for script in scripts:
                if "FlashVars" in script.text:
                    flash_script = script
                    break

            FlashVars = flash_script.text

            i = FlashVars.find('so.addParam("FlashVars","') + len('so.addParam("FlashVars","')
            j = FlashVars.find('so.addParam("menu"')

            FlashVars = FlashVars[i:j].strip('\n')

        
            database.log_fight(self.id, self.rang, id, health, straight, agility, rapidity, None, AI_guess, FlashVars) # rajouter le bool WIN