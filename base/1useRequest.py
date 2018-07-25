import requests


def getHtmlText(url):
    r = requests.get(url, timeout=3000)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text


print(getHtmlText("http://www.baidu.com"))
