import csv
import requests
from bs4 import BeautifulSoup
import time
import getItemInfo

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
}
medicine_herbs_info = {'名称': '', '拼音': '', '英文名': '', '拉丁名': '',
                       '分类': '', '产地': '', '性状': '', '品质': '',
                       '性味': '', '功效': '', '来源': '', '图片路径': '',
                       }


def get_new_csv(path):
    return open(path, 'w', newline="", encoding='utf-8-sig')


# csv_file = get_new_csv('medicine_herbs.csv')  # 返回 csv文件对象
# csv_write = csv.writer(csv_file)  # 返回 csv_file写入器对象

for page in range(1, 2):
    data = []  # 每一页的数据
    page_url = 'https://www.zhongyifangji.com/materials/index/p/' + str(page)
    res = requests.get(page_url, headers=headers)
    res.encoding = 'utf-8'
    time.sleep(1)
    soup = BeautifulSoup(res.text, 'lxml')
    try:
        medicine_herbs = (soup.find('div', {'class': 'g-3'})
                          .find_all('div', {'class': 'col'}))
        for medicine_herb in medicine_herbs:
            # 通过 a标签中对应的 url爬取药品的详细信息
            url = ('https://www.zhongyifangji.com/' + medicine_herb.find('div', {'class': 'card'})
                                                                    .find('a').get('href'))
            data.append(getItemInfo.getByURL(url))  # 放入药物的详细信息

    except AttributeError as e:
        print('Error!', e)
        continue

    # for d in data:
    #     for key in medicine_herbs_info.keys():
    #         if d.get(key) is None or d.get(key) == '':
    #             print(key, '暂无数据')
    #         else:
    #             print(key, d.get(key))
    #     print("=========================")
