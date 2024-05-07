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
        cur.execute("drop table if exists medicine")
        cur.execute("CREATE TABLE medicine ("
                    "id int AUTO_INCREMENT primary key comment 'id',"
                    "name varchar(50) comment '中药名', "
                    "alias varchar(255) comment '别名', "
                    "english_name varchar(50) comment '英文名', "
                    "position text comment '药用部位', "
                    "morphology text comment '植物形态', "
                    "source text comment '产地分布', "
                    "process text comment '采收加工', "
                    "nature text comment '药材性状', "
                    "characteristic text comment '药性', "
                    "flavor text comment '药味', "
                    "target_area text comment '归经', "
                    "benefits text comment '功效与作用', "
                    "application text comment '临床应用', "
                    "components text comment '主要成分', "
                    "prescription text comment '配伍药方', "
                    "researches text comment '药理研究', "
                    "contraindication text comment '使用禁忌', "
                    "url varchar(255) comment '图片路径', "
                    "provinces text comment '来源省份')")
        print("创建数据库->执行成功")
    except Exception as err:
        print('创建数据库->执行失败', err)


def insert_values(con, values):
    try:
        cur = con.cursor()
        sql = ("insert into medicine "
               "(name, alias, english_name, position, morphology, source, process, nature, benefits, application, components, prescription, researches, contraindication, url, provinces, characteristic, flavor, target_area) "
               "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        cur.executemany(sql, values)   # 批量写入数据
        con.commit()  # 提交
        print("插入数据->执行成功")
    except Exception as err:
        print("插入数据->执行失败", err)


# 关闭连接
def connect_close(con):
    con.close()
    print("关闭连接<--")

