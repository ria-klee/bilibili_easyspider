# 不含楼中楼评论
import requests
import time
import json
import re
import os
import pygal
from pygal.style import Style

Folderpath = os.getcwd()  # 取当前目录为生成的txt和svg文件储存位置
dianzan = []  # 统计点赞数

# BV to AV
table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr = {}
for i in range(58):
    tr[table[i]] = i
s = [11, 10, 3, 8, 4, 6]
xor = 177451812
add = 8728348608

def dec(x):
    r = 0
    for i in range(6):
        r += tr[x[s[i]]] * 58 ** i
    return (r - add) ^ xor

def get_html(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    r = requests.get(url, timeout=30, headers=headers)
    r.raise_for_status()
    r.endcodding = 'utf-8'
    # print(r.text)
    return r.text  # 评论者账号信息和评论信息
    # "member":
    # {"mid":"59861632",
    # "uname":"芒果味的星云",
    # "sex":"男",
    # "sign":"爱不会通关",
    # "avatar(头像)":"http://i1.hdslb.com/bfs/face/5c6bec68fc23050c845f6a28cb6c80d91ff9c831.jpg",
    # "level_info(b站等级)":"current_level":5,
    # "pendant(装扮)":{"pid":32948,"name":"贝拉kira","image(头像框)":"http://i1.hdslb.com/bfs/garb/item/82898a454a648be3a05e57d5c6cca1f81f95eb15.png",
    # "nameplate":{"nid":58,"name":"收集达人","image_"condition":"同时拥有粉丝勋章\u003e=15个"},
    # "content":{"message":"解压密码：y18",
    # "reply_control":{"time_desc":"498天前发布"}
    # https://space.bilibili.com/uid即可查看uid对应用户

def get_content(url):
    comments = []
    html = get_html(url)

    try:
        s = json.loads(html)
    except:
        print("jsonload error")

    num = len(s['data']['replies'])
    i = 0
    while i < num:
        comment = s['data']['replies'][i]

        InfoDict = {}

        InfoDict['Mid'] = comment['member']['mid']
        InfoDict['Level'] = comment['member']['level_info']['current_level']
        InfoDict['Uname'] = comment['member']['uname']
        InfoDict['Sign'] = comment['member']['sign']
        InfoDict['Like'] = comment['like']
        InfoDict['Content'] = comment['content']['message']
        InfoDict['Time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(comment['ctime']))
        # InfoDict['Pname'] = comment['pendant']['name']
        # InfoDict['Nname'] = comment['nameplate']['name']
        # InfoDict['Ncon'] = comment['nameplate']['condition']
        # 不是所有人都有，值为空时程序异常退出
        InfoDict['Reply'] = comment['reply_control']['time_desc']

        dianzan.append(InfoDict['Like'])
        comments.append(InfoDict)
        i = i + 1
    if InfoDict['Mid'] is None:
        exit(1)
    return comments


def Out2File(dict, j):

    with open(Folderpath + '\\BiliBiliComments.txt', 'a', encoding='utf-8') as f:
        i = 0
        f.write('!********AV number : av{}********!\t\n'.format(av))
        f.write('!********BV number : {}********!\t\n'.format(x))
        f.write('         !~~~~~~~~page {}~~~~~~~~!\n'.format(j))
        j = j + 1
        for comment in dict:
            i = i + 1
            try:
                f.write(
                    'uid:{}\t  等级:{}\t  用户名:{}\t  个性签名:{}\t\n  评论内容:{}\t  点赞数:{}\t\n 评论时间:{}\t 回复距今:{}\t\n '.format(
                        comment['Mid'], comment['Level'], comment['Uname'], comment['Sign'],
                        comment['Content'], comment['Like'], comment['Time'], comment['Reply']))
            #     f.write(
            #         'uid:{}\t  等级:{}\t  用户名:{}\t  个性签名:{}\t\n  评论内容:{}\t  点赞数:{}\t\n 评论时间:{}\t 回复距今:{}\t 装扮名称:{}\t 勋章名称:{}\t 已拥有粉丝牌:{}\t\n '.format(
            #             comment['Mid'], comment['Level'], comment['Uname'], comment['Sign'],
            #             comment['Content'], comment['Like'], comment['Time'], comment['Reply'],
            #             comment['Pname'], comment['Nname'], comment['Ncon']))
                f.write("-----------------这是第%d条评论-----------------\n\n" % ((page - 1) * 20 + i))
            except:
                print("out2File error")
        global ti  # 最后一页的i的值
        ti = i
        # print(ti)
        print('finish')


a = input("请输入BV号 or B站链接:")
pattern = re.compile(r'BV[^?|/]*')
bv = 'r' + a
x = ''.join(pattern.findall(bv))  # 将list转换为string
# BV号输入
av = dec(x)
print("AV number is: AV" + str(av))
print("connect to the url call(YOUR CRAWLING DATA WILL SAVE AS " + Folderpath + "!!) :\n")
print("https://api.bilibili.com/x/v2/reply?pn= (here should the page of webside) &type=1&oid=" + str(av))

if __name__ == '__main__':
    e = 0
    page = 1
    j = 1
    while e == 0:
        url = "https://api.bilibili.com/x/v2/reply?pn=" + str(page) + "&type=1&oid=" + str(av)
        try:
            print()
            content = get_content(url)
            print("page:", page)

            Out2File(content, j)
            j = j + 1
            page = page + 1
        except:
            e = 1
    with open(Folderpath + '\\BiliBiliComments.txt', 'a', encoding='utf-8') as f:
        f.write("-----------------本条视频一共%d条评论(不含回复)-----------------" % ((page - 2) * 20 + ti))
    dianzan.sort(reverse=True)  # 降序排序

    custom_style = Style(
        background='transparent',
        plot_background='transparent',
        foreground='#E95355',
        foreground_strong='#53A0E8',
        foreground_subtle='#630C0D',
        opacity='.8',
        opacity_hover='.2',
        transition='400ms ease-in',
        colors=('#FC966E', '#E87653', '#E89B53'))
    hist = pygal.Bar(style=custom_style)
    hist.title = '视频评论区统计'
    hist.x_labels = ['累计评论数', '点赞数第一', '点赞数第二', '点赞数第三', '点赞数第四', '点赞数第五']
    hist.x_title = '热门评论点赞数'
    # hist.y_title = ''
    # 添加数据
    hist.add(x, [((page - 2) * 20 + ti), dianzan[0], dianzan[1], dianzan[2], dianzan[3], dianzan[4]])
    # 格式必须是svg
    hist.render_to_file('details.svg')