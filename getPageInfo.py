import csv
import requests
from bs4 import BeautifulSoup
import getItemInfo
import time
from connect import connect, connect_close, create_table, insert_values

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}


# def get_new_csv(path='medicineTable.csv'):
def get_new_csv(path):
    return open(path, 'w', newline="", encoding='utf-8-sig')


csv_file = get_new_csv('medicineTable.csv')  # 返回 csv文件对象
csv_file2 = get_new_csv('neo4jTable.csv')  # 返回 neo4j的 csv文件对象
csv_write = csv.writer(csv_file)  # 返回 csv_file写入器对象
csv_write2 = csv.writer(csv_file2)  # 返回 csv_file2的写入器对象

# 先写下csv文件的第一行
first_row = ['中药名', '别名', '英文名', '药用部位',
             '植物形态', '产地分布', '采收加工',
             '药材性状', '性味归经', '功效与作用', '临床应用',
             '主要成分', '配伍药方', '药理研究', '使用禁忌',
             '图片路径', '来源省份', '药性', '药味', '归经']
csv_write.writerow(first_row)
# 连接数据库
con = connect()
# 创建数据库
create_table(con)
# 写入每一页的具体数据
value_list = []

# 药名节点
medicine_name = set()
# 药性节点
attribution = set()
# 药味节点
flavor = set()
# 归经节点
target = set()
# 省份节点
provinces = set()
# 关系
relation = dict()

for page in range(1, 3):
    data = []  # 每一页的数据
    page_url = 'http://www.zhongyoo.com/name/page_' + str(page) + '.html'
    res = requests.get(page_url, headers=headers)
    res.encoding = 'GBK'
    time.sleep(1)
    soup = BeautifulSoup(res.text, 'lxml')

    try:
        medicines = soup.find('div', {'class': 'r2-con'}).find_all('div', {'class': 'sp'})
        for medicine in medicines:
            # 通过 a标签中对应的 url爬取药品的详细信息
            url = medicine.find('a').get('href')
            data.append(getItemInfo.getByURL(url))  # 获取药物的详细信息

    except AttributeError as e:
        print('Error!', e)
        continue

    for item in data:  # data为当前页爬到的所有药品的信息，item为每一个药品的数据信息，是一个字典
        # if (not len(item) == 0) and (not len(item.get('Name')) == 0):  # 药名存在则数据存在？
        if not len(item) == 0:
            writerow = []  # 创建一个列表 writerow，药名作为第一个元素
            db_data = []  # 该数据待插入数据库
            neo4j_key = ''  # 添加至 neo4j字典中的 key
            neo4j_value = set()  # 添加至 neo4j字典中的 value
            for key in item.keys():  # 遍历字典的 key，即 medicine_info
                # if not key == 'Name':  # 不再放入药名
                if item.get(key) is None or len(item.get(key)) == 0:  # 没有爬到数据或数据为空
                    writerow.append('暂无数据')
                    if key != '性味归经':  # 数据库数据不放入性味归经，而是分别放入药性，药味，归经
                        db_data.append('暂无数据')
                else:
                    writerow.append(item.get(key))
                    if key != '性味归经':  # 数据库数据不放入性味归经，而是分别放入药性，药味，归经
                        db_data.append(item.get(key))

                ''' 添加 neo4j节点数据 '''
                if item.get(key) == '':  # 没有爬到数据，跳过
                    continue
                if key == '中药名':
                    zym = item.get(key).strip().split(' ')[0].strip()  # 只取中文名
                    medicine_name.add(zym)
                    neo4j_key = zym
                elif key == '药性':
                    yx = item.get(key).split(',')
                    for d in yx:
                        if d[0] == '性':
                            attribution.add(d)
                            neo4j_value.add('attribution,' + d + ',药性')
                        else:
                            attribution.add('性' + d)  # 添加性字作为开头
                            neo4j_value.add('attribution,' + '性' + d + ',药性')
                elif key == '药味':
                    yw = item.get(key).split(',')
                    for d in yw:
                        if d[0] == '味':
                            if len(d) == 1:  # 单独一个味字，跳过
                                continue
                            flavor.add(d)
                            neo4j_value.add('flavor,' + d + ',药味')
                        else:
                            flavor.add('味' + d)
                            neo4j_value.add('flavor,' + '味' + d + ',药味')
                elif key == '归经':
                    gj = item.get(key).split(',')
                    for d in gj:
                        target.add(d)
                        neo4j_value.add('target,' + d + ',归经')
                elif key == '来源省份':
                    sf = item.get(key).split(',')
                    for d in sf:
                        provinces.add(d)
                        neo4j_value.add('provinces,' + d + ',来源')

            relation[neo4j_key] = neo4j_value
            if not len(writerow) == 0:  # 列表中存在元素，则写入数据至 csv
                # print(writerow)
                csv_write.writerow(writerow)  # 将数据写入csv文件
                # print('db_data = ', db_data)
                value_list.append(db_data)  # 写入列表，方便数据批量插入数据库

insert_values(con, value_list)  # 将数据写入mysql数据库
csv_file.close()  # 关闭连接
csv_file2.close()  # 关闭连接
connect_close(con)  # 关闭连接

''' 导入 neo4j节点 '''
from neo4j_connect import create_node, delete_all, create_relation_by_name
# 1. 清空所有节点
print('准备清空Neo4j节点-->')
delete_all()
print('已清空Neo4j节点<--')
# 2. 创建节点
print('开始创建节点-->')
# 2.1 创建药品节点
for d in medicine_name:
    create_node('medicine', d, 'medicine')
# 2.2 创建药性节点
for d in attribution:
    create_node('attribution', d, 'attribution')
# 2.3 创建药味节点
for d in flavor:
    create_node('flavor', d, 'flavor')
# 2.4 创建归经节点
for d in target:
    create_node('target', d, 'target')
# 2.5 创建省份节点
for d in provinces:
    create_node('provinces', d, 'provinces')
print('创建节点完成<--')
# 3. 建立关系
print('开始创建关系-->')
for k in relation.keys():  # key
    v = relation.get(k)
    for p in v:  # value
        ps = p.split(',')
        label = ps[0]  # 节点的标签
        name = ps[1]  # 节点的名称
        r = ps[2]  # 节点间的关系
        # print(k, label, name, r)
        create_relation_by_name('medicine', k, label, name, r)
print('创建关系完成<--')
