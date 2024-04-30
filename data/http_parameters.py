import os

def get_logins():

    with open(os.getcwd()+'/data/logins.txt', 'r') as f:

        text=f.readline().split(':')

    email,password = text[0],text[1]

    return email,password

EMAIL, PASSWORD = get_logins()

twinoid_url = 'https://twinoid.com/bar/view?lang=fr;chk=e478ae8600d5be76bae65ee279425298;ver=397;infos=n;ch=d41d8cd98f00b204e9800998ecf8427e;tz=-60;fver=100.0.0;jsm=1;url=%2F;host=labrute.muxxu.com;proto=http%3A'

login_url='https://twinoid.com/user/login'

brute_action_headers={
        'Host': 'labrute.muxxu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'close'
        }

brute_headers={
        'Host': 'muxxu.com',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36',    
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'close'
    }

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

login_data={
        'login': EMAIL,
        'pass': PASSWORD,
        'submit': 'Me connecter',
        'host': 'labrute.muxxu.com',
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