import requests
from bs4 import BeautifulSoup

def get_logins():
    with open('logins.txt', 'r') as f:
        text=f.readline().split(':')
    (email,password)=(text[0],text[1])
    return(email,password)

def get_cookies():
    twinoid_url = 'https://twinoid.com/bar/view?lang=fr;chk=e478ae8600d5be76bae65ee279425298;ver=397;infos=n;ch=d41d8cd98f00b204e9800998ecf8427e;tz=-60;fver=100.0.0;jsm=1;url=%2F;host=labrute.muxxu.com;proto=http%3A'

    twinoid_headers={
        'Host': 'twinoid.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36',    
        'Accept': '*/*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'http://labrute.muxxu.com/',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        'Te': 'trailers',
        'Connection': 'close'
    }

    r=requests.get(twinoid_url, headers=twinoid_headers)
    
    
    login_url='https://twinoid.com/user/login'
    tw_sid=r.headers['Set-Cookie'][:r.headers['Set-Cookie'].find(';')]
    
    email,password=get_logins()
    
    login_data={
        'login': email,
        'pass': password,
        'submit': 'Me connecter',
        'host': 'labrute.muxxu.com',
        'sid': tw_sid,
        'ref': '',
        'refid': '',
        'url': '/',
        'mode': '',
        'proto': 'http:',
        'mid': '',
        'fver': '100.0.0'
        }
    
    login_headers={
        'Host': 'twinoid.com',
        'Cookie': tw_sid,
        'Content-Length': '175',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': "Windows",
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://twinoid.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36',
        'Accept': '*/*', #tobechanged
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'iframe',
        'Referer': 'https://twinoid.com/user/login',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'close'
    }
    r_login=requests.post(login_url, headers=login_headers,data=login_data)
    
    soup=BeautifulSoup(r_login.text,'html.parser')
    
    for i in range(len(soup.find_all('input'))):
        if soup.find_all('input')[i]['name']=="url":
            url=soup.find_all('input')[i]['value']
            break
    
    headers={
        'Host': 'muxxu.com',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36',    
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'close'
    }
    
    r_muxxu=requests.get(url,headers=headers)
    sid=r_muxxu.headers['Set-Cookie'][:r_muxxu.headers['Set-Cookie'].find(';')]
    
    cookies_dict={'tw_sid': tw_sid.strip('tw_sid='),
                  'sid': sid.strip('sid=')
                  }
    with open('cookies.txt', 'w') as f:
        f.write(tw_sid.strip('tw_sid=')+':'+sid.strip('sid='))
    f.close()