import csv
import requests
from bs4 import BeautifulSoup
import time
import getItemInfo
from mysql_connect import connect, create_table, insert_values, connect_close

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
}
prescription_info = {'名称': '', '拼音': '', '分类': '', '组成': '',
                     '用法': '', '功用': '', '主治': '', '病机': '',
                     '运用': '', '附方': '', '方歌': '', '附注': '',
                     '出处': '', '图片路径': '', '药材': ''
                     }


def get_new_csv(path):
    return open(path, 'w', newline="", encoding='utf-8-sig')


# csv_file = get_new_csv('prescription.csv')  # 返回 csv文件对象
# csv_write = csv.writer(csv_file)  # 返回 csv_file写入器对象

# 数据库数据处理
db_connect = connect()
create_table(db_connect)
db_data = []

for page in range(1, 2):
    data = []  # 每一页的数据
    page_url = 'https://www.zhongyifangji.com/prescription/index/p/' + str(page)
    res = requests.get(page_url, headers=headers)
    res.encoding = 'utf-8'
    time.sleep(1)
    soup = BeautifulSoup(res.text, 'lxml')
    try:
        prescriptions = soup.find('div', {'class': 'g-3'}).find_all('div', {'class': 'col'})
        for prescription in prescriptions:
            # 通过 a标签中对应的 url爬取药品的详细信息
            url = 'https://www.zhongyifangji.com/' + prescription.find('div', {'class': 'card'}).find('a').get('href')
            data.append(getItemInfo.getByURL(url))  # 放入药物的详细信息

    except AttributeError as e:
        print('Error!', e)
        continue

    for d in data:
        cur_db_data = []
        for key in prescription_info.keys():
            if d.get(key) is None or d.get(key) == '':
                cur_db_data.append('暂无数据')
            else:
                cur_db_data.append(d.get(key))
        print("=========================")
        db_data.append(cur_db_data)

insert_values(db_connect, db_data)  # 数据库批量写入数据
connect_close(db_connect)
