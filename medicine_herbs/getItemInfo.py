import requests
from bs4 import BeautifulSoup
import jieba


def getByURL(url):
    medicine_herbs_info = {'名称': '', '拼音': '', '英文名': '', '拉丁名': '',
                           '分类': '', '产地': '', '性状': '', '品质': '',
                           '性味': '', '功效': '', '来源': '', '图片路径': '',
                           }

    provinces = {
        '河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北',
        '湖南', '广东', '海南', '四川',
        '贵州', '云南', '陕西', '甘肃', '青海', '台湾', '内蒙古', '广西', '西藏', '宁夏', '新疆', '北京', '天津',
        '上海', '重庆', '香港', '澳门', '我国东北地区', '我国西北地区', '我国东南地区', '我国西南地区', '我国西北地区',
        '我国南方', '我国北方',
        '华北', '华南', '华东', '华西', '我国南部', '我国北部', '长江以南'
    }

    url = url
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
    }

    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    img_url = (soup.find('div', {'class': 'h-md-250'})
               .find('div', {'class': 'col-6'})
               .find('img').get('src'))  # 获取药材的图片路径
    medicine_herbs_info.update({'图片路径': img_url})
    # 药材基本信息
    basic_info_list = (soup.find('div', {'class': 'p-4'})
                       .find('div', {'class': 'small'})
                       .find_all('div', {'class': 'py-3'}))
    for basic_info in basic_info_list:
        title = basic_info.find('strong').get_text().strip()  # 每条概述的标题
        text = basic_info.get_text().strip().replace('\t', '').replace(title, '')  # 每条概述标题对应的详细信息(除去了该概述的标题)
        text = ''.join(text.splitlines())
        if title == '分类':
            print(title, text)
        medicine_herbs_info.update({title: text})  # 更新药材属性信息
    # 药材更多信息
    more_info_list = (soup.find('div', {'class': 'px-5'})
                      .find('div', {'class': 'small'})
                      .find_all('div', {'class': 'py-3'}))
    for more_info in more_info_list:
        title = more_info.find('strong').get_text().strip()  # 每条概述的标题
        text = more_info.get_text().strip().replace(title, '')  # 每条概述标题对应的详细信息(除去了该概述的标题)

        if title == '性味':
            xw = jieba.lcut(text)
            new_xw = []
            for d in xw:
                new_xw.append('味' + d)
            text = ','.join(new_xw)

        if title == '产地':
            cd = jieba.lcut(text)
            new_cd = []
            for d in cd:
                for p in provinces:
                    if d in p and (d != '地区' or d != '地'):
                        new_cd.append(p)
            text = ','.join(new_cd)

        medicine_herbs_info.update({title: text})  # 更新药材属性信息

    return medicine_herbs_info
