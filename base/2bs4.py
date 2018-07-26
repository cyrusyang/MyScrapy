from bs4 import BeautifulSoup
import requests

r = requests.get('http://www.baidu.com', timeout=30)
r.encoding = r.apparent_encoding
print(r.encoding)
soup = BeautifulSoup(r.text, 'html.parser')
print(soup.prettify())
print(soup.p)
print(type(soup.p))
print(soup.p.name)
print(soup.p.string)
print(soup.p.contents)
for tag in soup.p.descendants:
    print("tag:" + str(tag))

print(soup.p['id'])
print("test:" + str(soup.find('a', attrs={'id': 'lh'})))
print(soup.find_all('a')[0])
print(soup.find(id='lh'))
links = soup.find_all('a')
for link in links:
    print(link)

print('主题作者: 晴朗的zc'.strip('主题作者: '))
