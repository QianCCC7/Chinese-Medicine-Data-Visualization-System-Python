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
        cur.execute("drop table if exists prescription")
        cur.execute("CREATE TABLE prescription "
                    "("
                    "id int AUTO_INCREMENT primary key comment 'id',"
                    "name varchar(255) comment '名称', "
                    "pinyin varchar(255) comment '拼音', "
                    "category varchar(255) comment '分类', "
                    "make_up text comment '组成', "
                    "`usage` text comment '用法', "
                    "benefits text comment '功用', "
                    "treat text comment '主治', "
                    "cause text comment '病机', "
                    "apply text comment '运用', "
                    "addendum text comment '附方', "
                    "song text comment '方歌', "
                    "note text comment '附注', "
                    "source text comment '出处', "
                    "url varchar(255) comment '图片路径', "
                    "herbs text comment '组成方剂的药材id集合', "
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
        sql = ("insert into prescription "
               "(name, pinyin, category, make_up, `usage`, benefits, treat, cause, apply, addendum, song, note, source, url, herbs)"
               "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        cur.executemany(sql, values)  # 批量写入数据
        con.commit()  # 提交
        print("插入数据->执行成功")
    except Exception as err:
        print("插入数据->执行失败", err)


# 关闭连接
def connect_close(con):
    con.close()
    print("关闭连接<--")
