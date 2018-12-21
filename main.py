import re

import imageio
import matplotlib.pyplot as plt  # 数学绘图库
from jieba import analyse
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import sqlite3
import re

back_img = 'back.png'


# back_img = '背景图片'


# 返回要解析的文本
def get_text():
    conn = sqlite3.connect('../weibospider/test.db')
    cursor = conn.cursor()
    cursor.execute('select content from weibo')
    contents = cursor.fetchall()
    text = ''
    for content in contents:
        text += clear_text(content[0])
        text += clear_text(content[0])
        text += '\n'
    return text


def main():
    # 0、背景图
    back_color = imageio.imread(back_img)  # 解析该图片
    # 1、读入txt文本数据
    text = get_text()
    # 2、结巴分词，默认精确模式。可以添加自定义词典userdict.txt,然后jieba.load_userdict(file_name) ,file_name为文件类对象或自定义词典的路径
    # 自定义词典格式和默认词库dict.txt一样，一个词占一行：每一行分三部分：词语、词频（可省略）、词性（可省略），用空格隔开，顺序不可颠倒

    # cut_text = jieba.cut(text)
    # result = "/".join(cut_text)  # 必须给个符号分隔开分词结果来形成字符串,否则不能绘制词云
    analyse.set_stop_words("stopwords.txt")
    # withWeight=True为显示字符出现的频率，格式为[('aa',0.23),('a',0.11)]
    # 不加这个参数，或者参数值为false的时候格式为['a','b']
    result = analyse.extract_tags(text, topK=100, withWeight=True)

    # 3、生成词云图，这里需要注意的是WordCloud默认不支持中文，所以这里需已下载好的中文字库
    # 无自定义背景图：需要指定生成词云图的像素大小，默认背景颜色为黑色,统一文字颜色：mode='RGBA'和colormap='pink'

    wc = WordCloud(font_path=r"msyh.ttc", background_color='white', width=800,
                   height=600, max_font_size=50,
                   mask=back_color,  # 以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
                   max_words=200)  # ,min_font_size=10)#,mode='RGBA',colormap='pink')
    # wc.generate(result)
    wc.fit_words(dict(result))
    # 基于彩色图像生成相应彩色
    image_colors = ImageColorGenerator(back_color)
    # 4、显示图片
    plt.imshow(wc)  # 以图片的形式显示词云
    plt.figure("词云图")  # 指定所绘图名称
    plt.axis("off")  # 关闭图像坐标系
    wc.to_file("result.png")  # 按照设置的像素宽高度保存绘制好的词云图，比下面程序显示更清晰


# 去掉表情  如[]  去掉@ 的人
def clear_text(text):
    text = re.sub(r'\[.*?\]', '', text, 0)
    text = re.sub(r'@.*\s+?', '', text, 0)
    text = re.sub(r'http://t.cn/.*\s?', '', text, 0)
    return text


if __name__ == '__main__':
    main()


