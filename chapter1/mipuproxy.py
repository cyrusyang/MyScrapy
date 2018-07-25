import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from chapter1 import spyutil

# 从米铺爬取代理

url = 'https://proxy.mimvp.com'


def getHtmlRspCode(url, proxies):
    r = requests.get(url, proxies, timeout=30)
    return r.status_code


def getHtmlText(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    r.encoding = 'utf-8'
    return r.text


def getVerifyCode(url):
    response = requests.get(url, timeout=30)
    image = Image.open(BytesIO(response.content))
    text = spyutil.getverify1(image)
    # print(text)
    return text


def getProxy(url):
    html = getHtmlText(url)
    soup = BeautifulSoup(html, "html.parser")
    tbody = soup.find('div', attrs={'id':'free_freelist_open'}).find('tbody')
    trs = tbody.find_all('tr')
    results = []
    for tr in trs:
        result = {}
        print(tr)
        codeUrl = 'https://proxy.mimvp.com/'+tr.find('td', class_='tbl-proxy-port').find('img')['src']
        code = getVerifyCode(codeUrl)
        result['ip'] = 'http://' + tr.find('td', class_='tbl-proxy-ip').text + ':' + code
        result['type'] = tr.find('td', class_='tbl-proxy-type').text
        print(result['ip'])
        print(result['type'])
        if getHtmlRspCode('http://www.163.com', proxies={'http': result['ip']}) == 200:
            results.append(result)
    print(results)

getProxy(url)
