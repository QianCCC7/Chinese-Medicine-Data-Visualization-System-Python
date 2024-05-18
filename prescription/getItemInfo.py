import csv
import requests
from bs4 import BeautifulSoup
import jieba

medicine_herbs_names = set()  # 所有的药材名
medicine_herbs_map = dict()  # 药材及其对应id的映射表

# 加载所有的药材名，并生成药材及其对应id的映射表
def add_custom_words_from_csv(path):
    with open(path, newline='', encoding='utf-8-sig') as file:  # with打开文件，as file将打开的文件对象赋给名为file
        reader = csv.reader(file)
        for index, row in enumerate(reader, start=1):  # 读取每一行
            medicine_herbs_names.add(row[0])
            jieba.add_word(row[0])  # jieba分词库
            medicine_herbs_map[row[0]] = index


def getByURL(url):
    prescription_info = {'名称': '', '拼音': '', '分类': '', '组成': '',
                         '用法': '', '功用': '', '主治': '', '病机': '',
                         '运用': '', '附方': '', '方歌': '', '附注': '',
                         '出处': '', '图片路径': '', '药材': '', '药材名': '',
                         }
    url = url
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
    }
    add_custom_words_from_csv('../medicine_herbs/medicine_herbs_name.csv')  # 初始化jieba库等操作

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
            if title == '组成':
                ts = jieba.lcut(text)
                yc_id_db = []  # 该方剂的组成药材的 id，用于存入 mysql
                yc_names = []  # 该方剂的组成药材的 name集合,用于 neo4j创建节点关系
                for d in ts:
                    if d in medicine_herbs_names:  # 如果该分词出来的词语在 medicine_herbs_names中，才新增数据，用于确定该方剂由哪些药材组成
                        yc_id_db.append(str(medicine_herbs_map.get(d)))  # 存入组成方剂的药材的 id
                        yc_names.append(d)
                yc_db_text = ','.join(yc_id_db)
                prescription_info.update({'药材': yc_db_text})  # 更新方剂的药材组成(id)
                prescription_info.update({'药材名': yc_names})  # 更新方剂的药材组成(名称)

            prescription_info.update({title: text})  # 更新方剂属性信息

        except AttributeError as e:
            print('Error!', e)
            continue

    return prescription_info
