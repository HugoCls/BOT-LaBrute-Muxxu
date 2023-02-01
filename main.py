import requests
from bs4 import BeautifulSoup
import cookies
import pandas as pd
import time
import random as rd
import display
import fantasynames
import os

def reset_cookies():
    global cookie,sid,tw_sid
    cookies.get_cookies()

    with open(os.getcwd()+"/data/cookies.txt", 'r') as f:
        text=f.readline().split(':')
        
    sid={'sid': text[1]}

    cookie={'hcw': '1',
            'sid': sid['sid']
            }
    
    tw_sid={'tw_sid': text[0]}

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
    display.add_r_count()
    soup=BeautifulSoup(r.text,'html.parser')
    
    brutes=soup.find_all('td',class_="sheet")
    if len(brutes)>=2:
        j=rd.randint(0,7)
        
        b_to_attack=brutes[j].find_all('a')[0]['href'].strip('/b/')
        
        """
        health=brutes[j].find_all('p')[1].text.strip(' Vie ')
        straight=brutes[j].find_all('p')[2].text.strip(' Force ')
        agility=brutes[j].find_all('p')[3].text.strip(' Agilité ')
        rapidity=brutes[j].find_all('p')[4].text.strip(' Rapidité ')
        """
        
        brute=brutes[j]
        
        """
        p=brute.text.find('Vie ')+len('Vie ')
        health=brute.text[p:p+1]
        """
        health=int(brutes[j].find_all('p')[1].text.strip(' Vie '))
        """
        p=brute.text.find('Vie ')+len('Vie ')
        health=brute.text[p:p+2]
        """
        p=brute.text.find('Force ')+len('Force ')
        straight=brute.text[p:p+1]
        
        p=brute.text.find('Agilité ')+len('Agilité ')
        agility=brute.text[p:p+1]
        
        p=brute.text.find('Rapidité ')+len('Rapidité ')
        rapidity=brute.text[p:p+1]
        
        headers['Referer']=url
        
        url=url.strip('/train')+'/attack?b='+str(b_to_attack)
        
        r=requests.get(url,headers=headers,cookies=cookie)        
        display.add_r_count()
        return(health,straight,agility,rapidity)
    else:
        return(None,None,None,None)

######################################################################################
def loop():
    df=get_brutes()
    total_r=0
    
    brutes_data=[]
    
    for i in range(len(df)):
        display.reset_r_count()
        b_id=df.loc[i]['b_id']
        
        t_b=time.time()
        fxp,blessures,payer,level_up,attacks,rang=b_loop(b_id)
        b_time=time.time()-t_b
        print('Requests '+display.get_r_count()+' | '+str(round(b_time,2))+' | Trained '+str(b_id)+' | Attacks '+str(attacks)+' | '+str(fxp[0])+'/'+str(fxp[1])+' '+rang)
        
        brutes_data.append([display.get_r_count(),b_time,b_id,attacks,rang])
        
        total_r+=int(display.get_r_count())    

    print(total_r)
    return(brutes_data)

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
        display.add_r_count()
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
                ###RETHINK THE ATTACK LOOP
                for i in range(min(fxp[1]-fxp[0],max_injuries-blessures)):
                    health,straight,agility,rapidity=attack_brute(b_id)
                    
                    if health!=None:
                        #Get new injuries count
                        r=requests.get(url,cookies=cookie,headers=headers)
                        display.add_r_count()
                        soup=BeautifulSoup(r.text,'html.parser')
                        fxp,new_blessures,payer,level_up,disconnected,rang=get_b_infos(soup)
                        if blessures!=new_blessures:
                            blessures=new_blessures
                            win='0'
                            
                        else:
                            win='1'
                            
                        display.add_data(b_id,health,straight,agility,rapidity,win)
                        
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
                    display.add_r_count()
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
    display.add_r_count()
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
    display.add_r_count()
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



def recrut():
    global cookie,sid
    url='http://labrute.muxxu.com/recrut'
    
    headers={
        'Host': 'labrute.muxxu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://labrute.muxxu.com/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'close'
        }
    
    r=requests.get(url,cookies=cookie,headers=headers)
    soup=BeautifulSoup(r.text,'html.parser')
    end_url=soup.select('#mxcontent > ul > li:nth-child(1) > a')[0]['href'].strip('/recrut')
    headers['Referer']='http://labrute.muxxu.com/recrut'
    url+=end_url
    r=requests.get(url,cookies=cookie,headers=headers)
    
    name=fantasynames.anglo()
    
    brute_data={
        'name': name,
        'ok': 'on'
        }
    
    headers={
        'Host': 'labrute.muxxu.com',
        'Content-Lenght': str(len('name='+name+'&ok='+'on')),
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://labrute.muxxu.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': url,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'close'
        }
    
    r=requests.post(url, cookies=cookie, headers=headers,data=brute_data)
    
    if 'chk' in r.url:
        return(False)
    b_id=r.url.strip('http://labrute.muxxu.com/b/')
    
    brute=soup.select('#mxcontent > ul > li:nth-child(1)')[0]
    
    p=brute.text.find('Vie ')+len('Vie ')
    health=brute.text[p:p+2]
   
    p=brute.text.find('Force ')+len('Force ')
    straight=brute.text[p:p+1]
    
    p=brute.text.find('Agilité ')+len('Agilité ')
    agility=brute.text[p:p+1]
    
    p=brute.text.find('Rapidité ')+len('Rapidité ')
    rapidity=brute.text[p:p+1]
    
    #print(b_id,health,straight,agility,rapidity)
    display.add_chosen_brute(b_id,health,straight,agility,rapidity)
    
    return(True)
"""
j=0
while True:
    print(recrut(),end='-')
    j+=1
    print(j)
"""
brutes_data=loop()