from bs4 import BeautifulSoup
import requests
import random
import io

# 从百度贴吧爬取发帖内容
from requests.packages.urllib3.exceptions import ReadTimeoutError

proxy = {
    'http': 'http://140.143.105.245:80',
}


def getHtmlText(url):
    try:
        r = requests.get(url, proxies=proxy, timeout=3)
        r.raise_for_status()
        r.encoding = 'utf-8'
    except ReadTimeoutError as e:
        return 'ERROR'
    return r.text


def getContent(url):
    html = getHtmlText(url)
    soup = BeautifulSoup(html, 'html.parser')
    liList = soup.find_all('li', attrs={'class': ' j_thread_list clearfix'})
    comments = []
    for li in liList:
        comment = {}
        comment['title'] = li.find('a', attrs={'class': 'j_th_tit '}).text
        comment['author'] = li.find('a', attrs={'class': 'j_user_card'}).text
        comment['link'] = 'http://tieba.baidu.com' + li.find('a', attrs={'class': 'j_th_tit '})['href']
        comment['time'] = li.find('span', attrs={'class': 'pull-right is_show_create_time'}).text
        comment['repNum'] = li.find('span', attrs={'class': 'threadlist_rep_num'}).text
        comments.append(comment)
    return comments


def Out2File(dict):
    '''
        将爬取到的文件写入到本地
        保存到当前目录的 TTBT.txt文件中。

        '''
    with open('TTBT.txt', 'a+', encoding='utf-8') as f:
        for comment in dict:
            f.write('标题： {} \t 链接：{} \t 发帖人：{} \t 发帖时间：{} \t 回复数量： {} \n'.format(
                comment['title'], comment['link'], comment['author'], comment['time'], comment['repNum']))

        print('当前页面爬取完成')


def main(deep):
    url = 'https://tieba.baidu.com/f?kw=%E6%98%9F%E9%9C%B2%E8%B0%B7%E7%89%A9%E8%AF%AD&ie=utf-8'
    for i in range(0, deep):
        url = url + '&pn=' + str((i + 1) * 50)
        comments = getContent(url)
        Out2File(comments)
    print('所有信息保存完毕')


if __name__ == '__main__':
    # main(1)
    r = requests.get('http://ip.chinaz.com/getip.aspx', proxies=proxy, timeout=3)
    print(r.status_code)
    print(r.text)
