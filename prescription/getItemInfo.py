import requests
from bs4 import BeautifulSoup
import jieba


def getByURL(url):
    prescription_info = {'名称': '', '拼音': '', '分类': '', '组成': '',
                         '用法': '', '功用': '', '主治': '', '病机': '',
                         '运用': '', '附方': '', '方歌': '', '附注': '',
                         '出处': '', '图片路径': '',
                         }
    url = url
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
    }

    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    img_url = soup.find('div', {'id': 'solutionmod-pic-section'}).find('img').get('src')  # 获取方剂的图片路径
    prescription_info.update({'图片路径': img_url})
    info_list = (soup.find('div', {'class', 'px-5'})
                 .find('div', {'class': 'small'})
                 .find_all('div', {'class': ['border-bottom', 'border-light', 'py-3']}))
    for info in info_list:
        try:
            title = info.find('strong').get_text().strip()  # 每条概述的标题
            text = info.get_text().strip().replace(title, '')  # 每条概述标题对应的详细信息(除去了该概述的标题)
            prescription_info.update({title: text})  # 更新方剂属性信息

        except AttributeError as e:
            print('Error!', e)
            continue

    return prescription_info
