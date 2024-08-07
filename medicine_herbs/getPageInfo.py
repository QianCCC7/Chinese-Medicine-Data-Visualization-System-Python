import csv
import requests
from bs4 import BeautifulSoup
import time
import getItemInfo
from mysql_connect import connect, create_table, insert_values, connect_close
from neo4j_connect import get_graph, create_node, delete_nodes_by_label, delete_all_relations

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
}
medicine_herbs_info = {'名称': '', '拼音': '', '英文名': '', '拉丁名': '',
                       '分类': '', '产地': '', '性状': '', '品质': '',
                       '性味': '', '功效': '', '来源': '', '图片路径': '',
                       '炙品': '',
                       }


def get_new_csv(path):
    return open(path, 'w', newline="", encoding='utf-8-sig')


# csv_file = get_new_csv('medicine_herbs.csv')  # 返回 csv文件对象
# csv_write = csv.writer(csv_file)  # 返回 csv_file写入器对象
medicine_herbs_csv = get_new_csv('medicine_herbs_name.csv')  # 记录所有药材名的 csv文件对象
medicine_herbs_csv_writer = csv.writer(medicine_herbs_csv)

# 数据库数据处理
db_connect = connect()
create_table(db_connect)
db_data = []

# 将药材名写入 csv文件，csv_medicine_herbs_data的每个元素为列表即[medicine_herbs_name]
csv_medicine_herbs_data = []

# 获取neo4j图数据库对象用于创建节点
graph = get_graph()
delete_all_relations(graph)  # 先将所有关系删除
delete_nodes_by_label(graph, 'medicine_herbs')  # 再将该 label下的所有节点删除

for page in range(1, 22):
    print('当前为第' + str(page) + '页')
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

    for d in data:
        cur_db_data = []
        neo4j_data_name = ''
        neo4j_data_category = ''
        for key in medicine_herbs_info.keys():
            if d.get(key) is None or d.get(key) == '':
                cur_db_data.append('暂无数据')
            else:
                cur_db_data.append(d.get(key))
                if key == '名称':
                    csv_medicine_herbs_data.append([d.get(key)])
                    neo4j_data_name = d.get(key)
                elif key == '分类':
                    neo4j_data_category = d.get(key)

        db_data.append(cur_db_data)  # 写入数据库数据列表，方便数据批量插入数据库
        if neo4j_data_name != '' and neo4j_data_category != '':  # 当节点的名称以及分类都不为空时，才创建 neo4j节点
            create_node(graph, 'medicine_herbs', neo4j_data_name, neo4j_data_category)  # 创建 neo4j节点

insert_values(db_connect, db_data)  # 数据库批量写入数据
connect_close(db_connect)

# 将药名批量写入 csv文件
medicine_herbs_csv_writer.writerows(csv_medicine_herbs_data)
medicine_herbs_csv.close()
