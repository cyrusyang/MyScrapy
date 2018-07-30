# coding=utf-8
import requests
from bs4 import BeautifulSoup


class ProxyCollect():
    """
        代理收集类
    """

    def __init__(self, name):
        self.__name = name

    def getProxies(self):
        """
        获取代理
        """
        results = []
        if self.__name == 'mipu':
            pass
        elif self.__name == 'xici':
            for page in range(1, 3332):
                print('page :'+str(page)+'============================')
                url = 'http://www.xicidaili.com/nn/' + str(page)
                try:
                    html = self.getHtml(url, proxy={'http': 'http://117.127.0.203:8080'})
                    print(html)
                    soup = BeautifulSoup(html, 'html.parser')
                    trs = soup.find('table', attrs={'id': 'ip_list'}).find_all('tr', attrs={'class': True})
                    for tr in trs:
                        proxy = {}
                        tds = tr.find_all('td')
                        proxy['ip'] = tds[1].text
                        proxy['port'] = tds[2].text
                        proxy['http'] = str(tds[5].text).lower()
                        if self.isAlive(proxy['ip'], proxy['port'], proxy['http']):
                            print(str(proxy) + ' is alive')
                            results.append(proxy)
                        else:
                            print(str(proxy) + ' no alive')
                except:
                    print(url+'请求失败')
                    page -= 1
                    continue
        return results

    @staticmethod
    def isAlive(ip, port, http):
        """
        检测代理是否存活
        :param ip:
        :param port:
        :param http:
        """
        try:
            r = requests.get('http://wwww.163.com', proxies={http: http + '://' + ip + ':' + port}, timeout=1)
        except:
            return False
        return True

    @staticmethod
    def getHtml(url, proxy=None):
        """
        获取html
        """
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        html = requests.get(url, proxies=proxy, headers=headers, timeout=1)
        html.encoding = 'utf-8'
        html.raise_for_status()
        return html.text


if __name__ == '__main__':
    p = ProxyCollect('xici')
    results = p.getProxies()
    # print(p.getHtml('http://ip.chinaz.com/getip.aspx', proxy={'http': '101.236.60.48:8866'}))
    with open('proxies.txt', 'w') as f:
        for r in results:
            f.write(r['http'] + '://' + r['ip'] + ':' + r['port'] + '\n')
