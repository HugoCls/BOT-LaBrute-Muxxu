import requests
from bs4 import BeautifulSoup
import cookies
import pandas as pd

def reset_cookies():
    global cookie,sid
    cookies.get_cookies()

    with open('cookies.txt', 'r') as f:
        text=f.readline().split(':')
        
    sid={'sid': text[1]}

    cookie={'hcw': '1',
            'sid': sid['sid']
            }

reset_cookies()

def get_brutes():
    
    data={'b_id': [],
          'level': [],
          'hps': [],
          'strength': [],
          'agility': [],
          'rapidity': []
          }

    df=pd.DataFrame(data,dtype=int)
    
    r_team=requests.get('http://labrute.muxxu.com/team',cookies=sid)
    
    soup=BeautifulSoup(r_team.text,'html.parser')
    
    brutes=soup.find_all('td',class_="sheet")
    
    for brute in brutes:
        b_id=brute.find_all('a')[0]['href'].strip('/b/')
        
        level=brute.find_all('p')[0].text.strip(' ')
        
        hps=brute.find_all('p')[1].text.strip(' Vie ')
        
        strength=brute.find_all('p')[2].text.strip(' Force ')
        
        agility=brute.find_all('p')[3].text.strip(' Agilité ')
        
        rapidity=brute.find_all('p')[4].text.strip(' Rapidité ')
        
        
        brute_raw={'b_id': [int(b_id)],
                   'level': [int(level)],
                   'hps': [int(hps)],
                   'strength': [int(strength)],
                   'agility': [int(agility)],
                   'rapidity': [int(rapidity)]
                   }
        df_brute=pd.DataFrame.from_dict(brute_raw)
        
        df = pd.concat([df,df_brute], ignore_index=True)
    return(df)


def attack_brute(b_id):
    url='http://labrute.muxxu.com/b/'+str(b_id)+'/train'
    
    headers={
        'Host': 'labrute.muxxu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://labrute.muxxu.com/b/'+str(b_id)+'/train',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'close'
        }

    r=requests.get(url,cookies=cookie,headers=headers)
    add_r_count()
    soup=BeautifulSoup(r.text,'html.parser')
    
    brutes=soup.find_all('td',class_="sheet")
    if len(brutes)>=2:
        hp_min=1000
        j=0
        for i in range(len(brutes)):
            hps=int(brutes[i].find_all('p')[1].text.strip(' Vie '))
            #print(i,hps)
            if hps<=hp_min:
                j=i
                hp_min=hps
        b_to_attack=brutes[j].find_all('a')[0]['href'].strip('/b/')
        
        headers['Referer']=url
        
        url=url.strip('/train')+'/attack?b='+str(b_to_attack)
        
        r=requests.get(url,headers=headers,cookies=cookie)        
        add_r_count()
        return(True,r)
    else:
        return(False,r)

######################################################################################
def loop():
    df=get_brutes()
    total_r=0
    for i in range(len(df)):
        reset_r_count()
        b_id=df.loc[i]['b_id']
        fxp,blessures,payer,level_up,attacks,rang=b_loop(b_id)
        print('Requests '+get_r_count()+' | Trained '+str(b_id)+' | Attacks '+str(attacks)+' | '+str(fxp[0])+'/'+str(fxp[1])+' '+rang)
        total_r+=int(get_r_count())
    print(total_r)

def b_loop(b_id):
    global cookie,sid
    
    url='http://labrute.muxxu.com/b/'+str(b_id)
    
    headers={
        'Host': 'labrute.muxxu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'close'
        }
    attacks=0
    healed=False
    while True:
        r=requests.get(url,cookies=cookie,headers=headers)
        add_r_count()
        soup=BeautifulSoup(r.text,'html.parser')
        
        #4 injuries 4085909
        fxp,blessures,payer,level_up,disconnected,rang=get_b_infos(soup)
        
        
        if disconnected:
            print('-- Reconnecting --')
            reset_cookies()
        else:
            if level_up:
                levelup(b_id)

            elif not soup.select('#mxcontent > div.box2top > div')[0].find_all('span')[0].has_attr('class'):
                if soup.select('#mxcontent > div.box2top > div')[0].find_all('span')[0].text=='3':
                    max_injuries=4
                else:
                    max_injuries=3
                for i in range(min(fxp[1]-fxp[0],max_injuries-blessures)):
                    attack_brute(b_id)
                    attacks+=1
            
            if payer:
                if healed==False:
                    if soup.select('#mxcontent > div.box2top > div > div > table')[0].find_all('li')[1].has_attr('class'):
                        healed=True
                    else:
                        heal(b_id,soup)
                        healed=True
                else:
                    r=requests.get(url,cookies=cookie,headers=headers)
                    add_r_count()
                    soup=BeautifulSoup(r.text,'html.parser')
                    
                    fxp,blessures,payer,level_up,disconnected,rang=get_b_infos(soup)
                    return(fxp,blessures,payer,level_up,attacks,rang)

######################################################################################
def get_b_infos(soup):
    if 'Maître' in soup.text:
        disconnected=True
        return(None,None,None,None,disconnected,None)
    p=soup.text.find('Expérience : ')+len('Expérience : ')
    xp=soup.text[p:p+15]
    while xp.strip('\r')!=xp or xp.strip('\t')!=xp or xp.strip('\n')!=xp:
        xp=xp.strip('\r')
        xp=xp.strip('\n')
        xp=xp.strip('\t')
    xp=xp.strip('Expérience : ')
    xp=xp.replace(' ','')

    fxp=[int(xp[:xp.find('/')]),int(xp[xp.find('/')+1:])]

    j=soup.text.find('Blessures ')+len('Blessures ')
    blessures=soup.text[j:j+1]

    payer=False
    level_up=False
    disconnected=False

    if 'Payer' in soup.text:
        payer=True
    if 'niveau' in soup.text:
        level_up=True
        
    N=soup.text.find('Classement')+60
    rang=soup.text[N:]
    
    while rang.strip('\r')!=rang or rang.strip('\t')!=rang or rang.strip('\n')!=rang:
        rang=rang.strip('\r')
        rang=rang.strip('\n')
        rang=rang.strip('\t')
    
    j=0
    while rang[j] not in ['\r','\n','\t']:
        j+=1
    rang=rang[:j]
    
    return(fxp,int(blessures),payer,level_up,disconnected,rang)

def heal(b_id,soup):
    url='http://labrute.muxxu.com/b/'+str(b_id)+'/heal'
    
    headers={
        'Host': 'labrute.muxxu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://labrute.muxxu.com/b/'+str(b_id),
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'close'
        }
    end_url=soup.select('#mxcontent > div.box2top > div > div > table')[0].find_all('a')[1]['href']
    N=end_url.find('?chk')
    end_url=end_url[N:]
    
    url=url+end_url
    
    r=requests.get(url,cookies=sid,headers=headers)
    add_r_count()
    return(r)

def levelup(b_id):
    url='http://labrute.muxxu.com/b/'+str(b_id)+'/levelup'
    headers={
        'Host': 'labrute.muxxu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://labrute.muxxu.com/b/'+str(b_id),
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'close'
        }  
    r=requests.get(url,cookies=cookie,headers=headers)
    add_r_count()
    soup=BeautifulSoup(r.text,'html.parser')
    
    end_url=soup.select('#mxcontent > div > ul.learn > li.one > a')[0]['href']
    
    N=end_url.find(';chk')
    end_url=end_url[N:]
    
    choice_url='http://labrute.muxxu.com/b/'+str(b_id)+'/levelup?c='
    
    choice1=soup.find_all('li',class_='one')[0].text
    choice2=soup.find_all('li',class_='two')[0].text
    
    
    if 'Intouchable' or 'Immortel' or 'compétence' or 'Ours' in choice1:
        choice_url+='0'
    elif 'Intouchable' or 'Immortel' or 'compétence' or 'Ours' in choice2:
        choice_url+='1'
    else:
        if 'Force' in choice1:
            choice_url+='0'
        elif 'Force' in choice2:
            choice_url+='1'
        else:
            choice_url+='0'
    
    choice_url=choice_url+end_url
    
    headers['Refer']=choice_url
    r_choice=requests.get(choice_url,headers=headers,cookies=cookie)
    return(r_choice)

def add_r_count():
    with open('requests.txt', 'r') as f:
        count=f.read()
    with open('requests.txt', 'w') as f:
        f.write(str(int(count)+1))

def reset_r_count():
    with open('requests.txt', 'w') as f:
        f.write('0')

def get_r_count():
    with open('requests.txt', 'r') as f:
        count=f.read()
    return(count)

loop()