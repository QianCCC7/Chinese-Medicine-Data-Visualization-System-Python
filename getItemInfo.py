import requests
from bs4 import BeautifulSoup
import jieba

jieba.add_word('小肠经')
jieba.add_word('心经')
jieba.add_word('性微寒')


def getByURL(url):
    url = url
    medicine_info = {'中药名': '', '别名': '', '英文名': '', '药用部位': '',
                     '植物形态': '', '产地分布': '', '采收加工': '',
                     '药材性状': '', '性味归经': '', '功效与作用': '', '临床应用': '',
                     '主要成分': '', '配伍药方': '', '药理研究': '', '使用禁忌': '',
                     '图片路径': '', '来源省份': '', '药性': '', '药味': '', '归经': ''
                     }

    title_mappings = {
        '药名': '中药名', '别名': '别名', '英文': '英文名', '部位': '药用部位',
        '来源': '药用部位', '形态': '植物形态', '分布': '产地分布', '产地': '产地分布', '加工': '采收加工',
        '性状': '药材性状', '归经': '性味归经', '功效': '功效与作用', '应用': '临床应用', '成分': '主要成分',
        '禁忌': '使用禁忌', '配伍': '配伍药方', '药理': '药理研究', '药方': '配伍药方', '图片路径': '图片路径'
    }
    provinces = {
        '河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北',
        '湖南', '广东', '海南', '四川',
        '贵州', '云南', '陕西', '甘肃', '青海', '台湾', '内蒙古', '广西', '西藏', '宁夏', '新疆', '北京', '天津',
        '上海', '重庆', '香港', '澳门', '我国东北', '我国西北', '我国东南', '我国西南', '我国南方', '我国北方',
        '华北', '华南', '华东', '华西', '我国南部', '我国北部'
    }
    # 药性：药的性质
    # 药味：药味道
    # 归经：对什么部位有好处
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    res.encoding = 'GBK'
    soup = BeautifulSoup(res.text, 'lxml')

    name = soup.find('div', {'class': 'title'}).find('h1').get_text().strip()  # 药名
    # medicine_info.update({'Name': name})  # 将药名添加到 medicine_info字典中

    info_list = soup.find('div', {'class': 'gaishu'}).find('div', {'class': 'text'})  # 药品的所有概述
    descriptions = info_list.find_all('p')  # 概述中有多个 p标签，对应多个概述
    for description in descriptions:  # 枚举每个概述
        try:
            if description.find('img') is not None:  # 找到图片的 url
                title = '图片路径'
                text = 'http://www.zhongyoo.com/' + description.find('img').get('src')
                medicine_info.update({title: text})

            title = description.find('strong').get_text().strip()  # 每条概述的标题
            del_str = '【' + title + '】'
            text = description.get_text().strip().replace(del_str, '')  # 每条概述标题对应的详细信息(除去了该概述的标题)

            if title in '产地分布':  # 分析来源省份
                add_province = []
                ps = jieba.lcut(text)  # 分词
                for p in ps:
                    if p in provinces:
                        add_province.append(p)
                if len(add_province) > 0:
                    p_str = ','.join(add_province)
                    medicine_info.update({'来源省份': p_str})

            if title in '性味归经':  # 分析药的性味归经
                data = jieba.lcut(text.replace('归', '').replace('(《吉林省中药材标准第一册（2019年版）》)', ''))  # 分词
                yx = []  # 药性
                yw = []  # 药味
                gj = []  # 归经
                for d in data:
                    if '性' in d:
                        yx.append(d)  # 药性
                    elif '经' in d:
                        gj.append(d)  # 归经
                    else:
                        if d not in ['，', '。', '、']:
                            yw.append(d)  # 药味
                if len(yx) > 0:
                    a_str = ','.join(yx)
                    medicine_info.update({'药性': a_str})
                if len(gj):
                    b_str = ','.join(gj)
                    medicine_info.update({'归经': b_str})
                if len(yw):
                    c_str = ','.join(yw)
                    medicine_info.update({'药味': c_str})

        except AttributeError as e:
            # print('Error!', e)
            continue

        find = False
        for key in title_mappings.keys():
            if key in title:
                title = title_mappings[key]
                find = True
                break

        if find is False:  # 无用数据，跳过写入该数据
            continue

        medicine_info.update({title: text})  # 将药品的概述添加到 medicine_info字典中

    return medicine_info
