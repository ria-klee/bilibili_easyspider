import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import jieba

stopwords = set('')
stopwords.update(
    ['个性签名', 'uid', '评论', '天前', '等级', '用户名', '是', '第', '回复', '距今', '点赞数', '时间', '内容', '发布', '了', '的', '这', '条', '个性',
     '签名', 'AV number', 'BV number', 'aV', 'BV', '你', '不', 'page', '我', '啊', '都', '她', '给', '和', '人', '就', '很', '在',
     'number', '吗', '个', '的', '呢', '要', '吧', '小时', '分钟', '前', 'av423822752', 'BV1A3411J7BN'])

filename = "BiliBiliComments.txt"
with open(filename, encoding='utf-8') as f:
    mytext = f.read()
mytext = " ".join(jieba.cut(mytext))  # 进行中文分词
backgroud_Image = plt.imread('D:/Pictures/asoul/3bb4463159bb5991e7b46fb3e4d27ece7d2eb770.jpg')
wc = WordCloud(background_color='white',  # 设置背景颜色
               mask=backgroud_Image,  # 设置背景图片
               max_words=200,  # 设置最大现实的字数
               stopwords=stopwords,  # 设置停用词
               font_path='D:/Tools/wordziti/简启体.TTF',  # 设置字体格式，如不设置显示不了中文
               max_font_size=100,  # 设置字体最大值
               color_func=None,  # 设置关键字的字体颜色
               random_state=42,  # 设置有多少种随机生成状态，即有多少种配色方案
               ).generate(mytext)

plt.imshow(wc)
image_colors = ImageColorGenerator(backgroud_Image)
wc.recolor(color_func=image_colors)
plt.imshow(wc)
plt.axis('off')
plt.show()
