import csv
import requests
from bs4 import BeautifulSoup
import time
import getItemInfo
from mysql_connect import connect, create_table, insert_values, connect_close
from neo4j_connect import get_graph, get_matcher, create_node, delete_nodes_by_label, create_relation_by_name, delete_all_relations

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
}
prescription_info = {'名称': '', '拼音': '', '分类': '', '组成': '',
                     '用法': '', '功用': '', '主治': '', '病机': '',
                     '运用': '', '附方': '', '方歌': '', '附注': '',
                     '出处': '', '图片路径': '', '药材': '', '药材名': '',
                     }


def get_new_csv(path):
    return open(path, 'w', newline="", encoding='utf-8-sig')


# csv_file = get_new_csv('prescription.csv')  # 返回 csv文件对象
# csv_write = csv.writer(csv_file)  # 返回 csv_file写入器对象

# 数据库数据处理
db_connect = connect()
create_table(db_connect)
db_data = []

# 获取neo4j图数据库对象以及节点查询nodeMatcher对象
graph = get_graph()
matcher = get_matcher()
delete_all_relations(graph)  # 先将所有关系删除
delete_nodes_by_label(graph, 'prescription')  # 先将该 label的所有节点删除

for page in range(1, 11):
    print('当前为第' + str(page) + '页')
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
        neo4j_data_name = ''  # 方剂名称
        neo4j_data_category = ''  # 方剂种类
        neo4j_data_medicine_herbs_name = []  # 方剂对应的所有药材名称
        for key in prescription_info.keys():
            if key == '药材名':  # 药材名，不存入 mysql数据库，仅用于 neo4j创建节点关系
                if neo4j_data_name == '':  # 方剂节点名字为空，不创建关系
                    continue
                for medicine_herbs_name in d.get(key):  # 遍历当前方剂的所有药材，并创建 neo4j的关系
                    neo4j_data_medicine_herbs_name.append(medicine_herbs_name)
                continue

            if d.get(key) is None or d.get(key) == '':
                cur_db_data.append('暂无数据')
            else:
                cur_db_data.append(d.get(key))
                if key == '名称':
                    neo4j_data_name = d.get(key)
                elif key == '分类':
                    neo4j_data_category = d.get(key)

        db_data.append(cur_db_data)
        if neo4j_data_name != '' and neo4j_data_category != '':  # 当节点的名称以及分类都不为空时，才创建 neo4j节点
            create_node(graph, 'prescription', neo4j_data_name, neo4j_data_category)  # 创建 neo4j节点
            for medicine_herbs_name in neo4j_data_medicine_herbs_name:
                create_relation_by_name(graph, matcher, 'prescription', neo4j_data_name,
                                                        'medicine_herbs', medicine_herbs_name, '来源于')
insert_values(db_connect, db_data)  # 数据库批量写入数据
connect_close(db_connect)
