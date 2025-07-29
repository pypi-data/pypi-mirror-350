import requests
from datetime import datetime
from bs4 import BeautifulSoup
from .models import Topic, Reply



def get_hot():
    data = []
    for line in requests.get('https://www.v2ex.com/api/topics/hot.json').json():
        id = line['id']
        line_title = line['title']
        url = line['url']
        content = line['content']
        content_rendered = line['content_rendered']
        replies = line['replies']
        created = datetime.fromtimestamp(line['created']).strftime('%Y-%m-%d %H:%M:%S')
        node_title = line['node']['title']
        username = line['member']['username']
        data.append(Topic(id, line_title, replies, url, content, content_rendered, node_title, username, created))
    return data


def get_replies(topic_id):
    data = []
    for line in requests.get('https://www.v2ex.com/api/replies/show.json?topic_id={}'.format(topic_id)).json():
        id = str(line['id'])
        content = line['content']
        content_rendered = line['content_rendered']
        username = line['member']['username']
        created = datetime.fromtimestamp(line['created']).strftime('%Y-%m-%d %H:%M:%S')
        data.append(Reply(id, topic_id, content, content_rendered, username, created))
    return data


def get_tab(tab):
    page = requests.get("https://www.v2ex.com/?tab={}".format(tab))
    soup = BeautifulSoup(page.text,features="lxml")

    topics = soup.body.find_all('div', 'item')
    data = []
    for i in topics:
        id = i.find('a', 'topic-link')['href'].split('#')[0].split('/')[-1]
        title = i.find('a', 'topic-link').text
        replies = i.find('a', 'count_livid').text if i.find('a', 'count_livid') else '0'
        url = 'https://www.v2ex.com/t/{}'.format(id)
        node_title = i.find('a', 'node').text
        username = i.find_all('strong')[0].text
        last_reply_user = i.find_all('strong')[1].text  if len(i.find_all('strong')) >= 2 else ''
        created = i.find_all('span')[2].text
        data.append(Topic(id, title, replies, url, '', '', node_title, username, last_reply_user, created))


    data_hot = []
    s = soup.body.find_all('span', 'item_hot_topic_title')
    for i in s:
        topic = i.find('a').text
        id = i.find('a')['href'].split('/')[2]

        data_hot.append(Topic(id=id, title=topic))
    return data, data_hot


def get_page_replies(topic_id):
    page = requests.get("https://www.v2ex.com/?tab={}".format(tab))
    soup = BeautifulSoup(page.text,features="lxml")
    pass


def get_topic_content(topic_id):
    url = f'https://www.v2ex.com/t/{topic_id}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features="lxml")
    content_div = soup.find('div', class_='topic_content')
    if content_div:
        return content_div.text.strip()
    return ''
