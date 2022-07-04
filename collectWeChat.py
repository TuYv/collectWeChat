#-*-coding:utf-8-*-

# from imp import reload
import json
import jieba
import wordcloud
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import time
import re

#获取聊天内容
def getMessage():
    text = open(openFile,"r", encoding="utf8").read()

    #text.encode('gbk', 'replace').decode('gbk')
    json1 = json.loads(text)
    return json1["message"]

#写年月统计图
def setMonth(messages):
    aDays = {}
    bDays = {}
    xB = []
    yB = []
    xA = []
    yA = []
    tempAfterNightLength = 0

    firstTimeObj = time.localtime(messages[0]['m_uiCreateTime'])
    startDay = time.strftime("%y年%m月%d日 %H:%M", firstTimeObj)
    for msg in messages:
        timeObj = time.localtime(msg['m_uiCreateTime'])
        yearMonth = time.strftime("%y.%m", timeObj)
        yearMonthDay = time.strftime("%y.%m.%d", timeObj)
        hour = time.strptime("%h", timeObj)
        dayTime = time.strftime("%y年%m月%d日 %H:%M", timeObj)

        if (hour < 5 & hour >= 0):
            if(mostNightDay < dayTime):
                mostNightDay =  dayTime
            if (tempAfterNightLength == 0):
                afterNightStartDay = yearMonthDay
            else:
                afterNightendDay = yearMonthDay
                tempAfterNightLength+=1
        elif(hour > 5 & hour < 8):
            if (mostMorningDay > dayTime):
                mostMorningDay = dayTime
        else:
            afterNightLength = max(tempAfterNightLength, afterNightLength)

        if (msg['m_nsFromUsr'] == toUser) :
            aDays.setdefault(yearMonth, 0)
            aDays[yearMonth] = aDays[yearMonth] + 1
        else:
            bDays.setdefault(yearMonth, 0)
            bDays[yearMonth] = bDays[yearMonth] + 1

    for numbers in aDays:
        xA.append(numbers)
        yA.append(aDays[numbers])

    for number in bDays:
        xB.append(number)
        yB.append(bDays[number])
    
    plt.figure()
    plt.rcParams["font.sans-serif"]=["SimHei"]
    plt.rcParams['figure.figsize'] = (20.0, 4.0)
    plt.rcParams['savefig.dpi'] = 500
    plt.plot(xA, yA, label="郭娟")
    plt.plot(xB, yB, label="涂瑜")
    plt.xlabel('date')
    plt.ylabel('records')

    plt.legend()

    # 显示或者下载
    #plt.show()
    plt.savefig('day.jpg')

#写每日统计
def setDays(messages):
    aHours = {}
    bHours = {}
    hxB = []
    hyB = []
    hxA = []
    hyA = []
    hoursDict = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
    for h in hoursDict:
        aHours[h] = 0
        bHours[h] = 0

    for msg in messages:
        timeObj = time.localtime(msg['m_uiCreateTime'])
        hour = time.strftime("%H", timeObj)
        if (msg['m_nsFromUsr'] == toUser) :
            aHours[hour] = aHours[hour] + 1
        else:
            bHours[hour] = bHours[hour] + 1
    
    for numbers in aHours:
        hxA.append(numbers)
        hyA.append(aHours[numbers])

    for numbers in bHours:
        hxB.append(numbers)
        hyB.append(bHours[numbers])
    
    x = np.arange(24)
    plus = 0.2
    plt.rcParams["font.sans-serif"]=["SimHei"]
    plt.rcParams['figure.figsize'] = (8.0, 4.0)
    plt.rcParams['savefig.dpi'] = 500
    plt.bar(x, hyA, label="郭娟", width=plus)
    plt.bar(x + plus, hyB, label="涂瑜", width=plus)
    plt.xlabel('hours')
    plt.ylabel('records')
    plt.xticks(x + plus/2, hxA)

    plt.legend()

    # 显示或者下载
    #plt.show()
    plt.savefig('hour.jpg')

#统计Emoji
def setEmojiCollect(messages):
    
    aEmojis = {}
    bEmojis = {}

    for msg in messages:
        value = msg["m_nsContent"]
        emoji_start = str(value)[0:11]
        if (emoji_start == '<msg><emoji'):
            emojiList = re.findall("(?<=cdnurl = \")http:.*?(?=\")", value)
            if (len(emojiList) > 0):
                if (msg['m_nsFromUsr'] == 'wxid_mou6ypc152t421') :
                    aEmojis.setdefault(emojiList[0], 0)
                    aEmojis[emojiList[0]] = aEmojis[emojiList[0]] + 1
                else:
                    bEmojis.setdefault(emojiList[0], 0)
                    bEmojis[emojiList[0]] = bEmojis[emojiList[0]] + 1
    
    print(sorted(aEmojis.items(), key=lambda x : -x[1]))
    print(sorted(bEmojis.items(), key=lambda x : -x[1]))

#写词云
def setWordCloud(messages):
    str_value = ''
    for msg in messages:
        totalCount += 1
        value = msg["m_nsContent"]
        v = str(value)[0:5]
        start_with = str(value)[0:1]
        if((start_with != '<') & (v != 'image') & (v != 'audio') & (start_with != '[') & (v != 'video')) :
            totalWord += len(str(value))
            str_value += ';' + value
    cut_text = ' '.join(jieba.lcut(str_value))
    backgroud = np.array(Image.open(imageFile))

    STOPWORDS = set()
    content = [line.strip() for line in open('stopWord.txt', 'r', encoding="utf8").readlines()]
    STOPWORDS.update(content)
    # STOPWORDS.add("说")
    # STOPWORDS.add("想")
    # STOPWORDS.add("吃")
    # STOPWORDS.add("感觉")
    # STOPWORDS.add("今天")
    # STOPWORDS.add("一个")
    # STOPWORDS.add("会")
    # STOPWORDS.add("找")
    # STOPWORDS.add("可能")
    # STOPWORDS.add("喜欢")
    STOPWORDS.add("哈")
    STOPWORDS.add("哈哈")
    STOPWORDS.add("哈哈哈")
    STOPWORDS.add("哈哈哈哈")
    # STOPWORDS.add("哦哦哦")
    # STOPWORDS.add("反正")
    # STOPWORDS.add("有点")
    # STOPWORDS.add("太")
    # STOPWORDS.add("真的")
    # STOPWORDS.add("买")
    # STOPWORDS.add("做")
    # STOPWORDS.add("不想")
    # STOPWORDS.add("朋友")
    # STOPWORDS.add("完")
    # STOPWORDS.add("看到")
    # STOPWORDS.add("之前")
    # STOPWORDS.add("好看")
    # STOPWORDS.add("是不是")
    # STOPWORDS.add("问题")
    # STOPWORDS.add("晚上")
    # STOPWORDS.add("玩")
    # STOPWORDS.add("不要")
    # STOPWORDS.add("不能")
    # STOPWORDS.add("看看")
    # STOPWORDS.add("回")

    wc = WordCloud(width=8000, height=8000, background_color='white',mode='RGB', mask=backgroud, max_words=500, stopwords=STOPWORDS, font_path='C:\Windows\Fonts\simhei.ttf',
                max_font_size=150, relative_scaling=0.6, random_state=50, scale=2).generate(cut_text)

    image_color = ImageColorGenerator(backgroud)
    wc.recolor(color_func=image_color)
    plt.imshow(wc)
    plt.axis('off')
    #plt.show()
    wc.to_file('try.png')

def clearPlt():
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()
 
#主函数
#获取聊天消息
toUser = 'wxid_6rpruv5mg1yn12'
openFile = 'mingliang.json'
imageFile = '69dd75b9204be7eb7079d8d26a0d7fdf_1.jpg'
startDay = ''
messages=getMessage()
totalCount = 0
totalWord = 0
afterNightStartDay = ""
afterNightendDay = ''
afterNightLength = 0
mostNightDay = ''
mostMorningDay = ''
mostWordDay = ''
mostWordDayCount = 0
#写月份统计
#setMonth(messages)
#clearPlt()
#写每日统计
#setDays(messages)
#写词云
setWordCloud(messages)
#统计表情包
#setEmojiCollect(messages)
