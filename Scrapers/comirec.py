import requests
from bs4 import BeautifulSoup

headers = {
    'Host': 'www.gba.gob.ar',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-AR,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://mail.google.com/',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Cookie': 'botmaker_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3ZWJJZCI6IlVNUkRRRE9MQ1QiLCJidXNpbmVzc0lkIjoiUHJvdmluY2lhZGVCdWVub3NBaXJlcyIsImN1c3RvbWVySWQiOiJXS1VDUEU1V0lKOExVRjNGQVA1OCIsImV4cCI6MTY4Njg0OTgxNX0.Et53VeCO6taAkCELjfdj3RTA-GcPz1I4QpV41gT2a6Y; has_js=1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'If-Modified-Since': 'Fri, 17 Mar 2023 20:48:29 GMT',
    'If-None-Match': '"1679086109-0-gzip"'
}


response = requests.post('https://www.gba.gob.ar/comirec/licitaciones_comirec', 
                         headers=headers, 
                         
soup = BeautifulSoup(response.content, 'html.parser')

print(soup)
