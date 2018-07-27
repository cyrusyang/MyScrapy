import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

from requests.packages.urllib3.exceptions import ReadTimeoutError

from base import spyutil
import time
import sched
import re

# 从米铺爬取代理
url = 'https://proxy.mimvp.com'

def getHtmlText(url , proxies=None):
    try:
        r = requests.get(url, proxies=proxies, timeout=3)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except Exception as e:
        return 'ERROR'



def getVerifyCode(url):
    try:
        response = requests.get(url, timeout=5)
        image = Image.open(BytesIO(response.content))
        text = spyutil.getverify1(image)
    except Exception as e:
        pass
    # print(text)
    return text


def getProxy(url):
    '开始爬取'
    html = getHtmlText(url)
    soup = BeautifulSoup(html, "html.parser")
    tbody = soup.find('div', attrs={'id': 'free_freelist_open'}).find('tbody')
    trs = tbody.find_all('tr')
    results = []
    for tr in trs:
        result = {}
        codeUrl = 'https://proxy.mimvp.com/' + tr.find('td', class_='tbl-proxy-port').find('img')['src']
        code = getVerifyCode(codeUrl)
        result['ip'] = 'http://' + tr.find('td', class_='tbl-proxy-ip').text + ':' + code
        result['type'] = tr.find('td', class_='tbl-proxy-type').text
        if getHtmlText('http://www.163.com', proxies={'http': result['ip']}) != 'ERROR':
            print('代理ip:' + result['ip'] + '已加入代理池')
            results.append(result)
        else:
            print('代理ip:' + result['ip'] + '无效')

    with open('proxies.txt', 'a') as f:
        for result in results:
            if not existProxy(result['ip']):
                f.write(result['ip'] + '\n')


def existProxy(proxy):
    with open('proxies.txt', 'r') as f:
        lines = f.read().splitlines()
    proxySet = set(lines)
    if proxy in proxySet:
        return True
    else:
        return False


def timeTask(second):
    print('开始执行，现在时间:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    getProxy(url)
    s.enter(second, 1, timeTask, (second,))


def test():
    with open('proxies.txt', 'a') as f:
        if not existProxy('http://117.127.0.209:8080'):
            print('exist')


if __name__ == '__main__':
    s = sched.scheduler(time.time, time.sleep)
    s.enter(0, 1, timeTask, (60,))
    s.run()
