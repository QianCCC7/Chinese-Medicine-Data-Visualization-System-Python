import pymysql


# 连接数据库
def connect():
    conn = pymysql.connect(host='localhost', user='root', password='xiaoqian666', db='pcrp', port=3306)
    print("数据库连接成功-->")
    return conn


# 创建数据库表
def create_table(con):
    try:
        cur = con.cursor()
        cur.execute("drop table if exists medicine_herbs")
        cur.execute("CREATE TABLE medicine_herbs "
                    "("
                    "id int AUTO_INCREMENT primary key comment 'id',"
                    "name varchar(255) comment '名称', "
                    "pinyin varchar(255) comment '拼音', "
                    "english_name varchar(255) comment '英文名', "
                    "latin_name varchar(255) comment '拉丁名', "
                    "category varchar(255) comment '分类', "
                    "provinces varchar(255) comment '产地', "
                    "nature text comment '性状', "
                    "quality text comment '品质', "
                    "flavor varchar(255) comment '性味', "
                    "benefits text comment '功效', "
                    "source text comment '来源', "
                    "url varchar(255) comment '图片路径', "
                    "roasted_food text comment '炙品', "
                    "create_date timestamp default CURRENT_TIMESTAMP comment '创建时间', "
                    "update_date timestamp default CURRENT_TIMESTAMP comment '修改时间'"
                    ")"
                    )
        print("创建数据库->执行成功")
    except Exception as err:
        print('创建数据库->执行失败', err)


def insert_values(con, values):
    try:
        cur = con.cursor()
        sql = ("insert into medicine_herbs "
               "(name, pinyin, english_name, latin_name, category, provinces, nature, quality, flavor, benefits, source, url, roasted_food)"
               "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        cur.executemany(sql, values)   # 批量写入数据
        con.commit()  # 提交
        print("插入数据->执行成功")
    except Exception as err:
        print("插入数据->执行失败", err)


# 关闭连接
def connect_close(con):
    con.close()
    print("关闭连接<--")

