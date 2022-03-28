import requests
from bs4 import BeautifulSoup
from time import sleep


def ksnews(html_url):
    """
    Get data from page on news
    :param html_url: Goal Web Link site
    :return: all_data: Type List and item like {title: news title, url: news url}
    """
    all_data = list()
    response = requests.get(html_url)  # 利用 get 方法爬取指定頁面
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser") # 使用BS4建立網頁根系
    result = soup.find_all(class_="text") # 透過 html 的 class(style) 去篩出資料
    for item in result:
        data = dict()
        data['title'] = item.h2.text
        data['url'] = item.a['href']
        all_data.append(data)
    return all_data


def filter_news(all_data):
    keyword = ['工程', '弊案', '貪污', '落成', '啟用']
    findout = []
    for item in all_data:
        if item in findout:
            continue
        elif item['title'].find(keyword[0]) > 0:
            findout.append(item)
        elif item['title'].find(keyword[1]) > 0:
            findout.append(item)
        elif item['title'].find(keyword[2]) > 0:
            findout.append(item)
        elif item['title'].find(keyword[3]) > 0:
            findout.append(item)
        elif item['title'].find(keyword[4]) > 0:
            findout.append(item)
    return findout


def sentToLine(data: str):
    line_notify_token = "9pXImZReNlwp8HpAdySKp80GUr0sNEtUAVM28smONFU"
    send_res = requests.post(
        url='https://notify-api.line.me/api/notify',
        headers={
            "Authorization": "Bearer " + line_notify_token },
        params={'message': data})
    return send_res.status_code


all_data = list()
html_url = "http://www.ksnews.com.tw/index.php/news/news_subList/16/125/"  # 設定爬取網址
for idx in range(5):
    webResData = ksnews(f"{html_url}{idx}")  # 格式化網址並分頁爬取
    all_data.extend(webResData)
    sleep(1)

filter_data = filter_news(all_data)

res_all_data = ''

for idx in range(len(filter_data)):
    news_id = idx + 1
    news_title = filter_data[idx]['title']
    news_url = filter_data[idx]['url']
    res_all_data += "\n" + f"{news_id:02} 新聞標題:{news_title}" + "\n" + f"網址:{news_url}"
    if (idx+1)%5 == 0:
        sentToLine(res_all_data)
        res_all_data = ''
    elif idx == len(filter_data)-1:
        sentToLine(res_all_data)
        res_all_data = ''
