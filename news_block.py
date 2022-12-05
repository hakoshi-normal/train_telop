import requests as req
import random
import re
import time
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

def get_weather():
    areas = ['札幌', '仙台', '東京', '名古屋', '大阪', '広島', '福岡']
    codes = ['016000', '040000', '130000', '230000', '270000', '340000', '400000']
    rules = [['くもり', '曇'],
            ['\u3000', ''],
            ['晴れ', '晴'],
            ['所により', '時々'],
            ['でふぶく', ''],
            ['夜のはじめ頃', '時々']]

    text = ""
    for i, (area, code) in enumerate(zip(areas, codes)):
        url = "https://www.jma.go.jp/bosai/forecast/data/forecast/"+code+".json"
        res = req.get(url).json()[0]
        weather = res['timeSeries'][0]['areas'][0]['weathers'][0]

        for rule in rules:
            weather = weather.replace(rule[0],rule[1])

        if i == 0:
            date = res["reportDatetime"][8:10]
            date = date.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))+"日天気"
            text += date
        text += f" {area}＝{weather}"
    return text

def get_title(media, url, pattern):
    response = req.get(url)
    response.encoding = response.apparent_encoding
    pattern = re.compile(pattern)
    matchobj = pattern.finditer(response.text)
    titles = []
    for i in matchobj:
        text = f"◇{media}◇" + i.group(1)
        text = text.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))
        titles.append(text)
    return titles

### PIL型 => OpenCV型　の変換関数
def pil2opencv(in_image):
    out_image = np.array(in_image, dtype=np.uint8)
    if out_image.shape[2] == 3:
        out_image = cv2.cvtColor(out_image, cv2.COLOR_RGB2BGR)
    return out_image

### OpenCV型 => PIL型　の変換関数
def opencv2pil(in_image):
    new_image = in_image.copy()   #複製
    if new_image.shape[2] == 3:
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    new_image = Image.fromarray(new_image)
    return new_image


medias = ["NHK NEWS WEB", "両丹日日新聞"]
urls = ["https://www3.nhk.or.jp/news/catnew.html", "https://www.ryoutan.co.jp/articles/"]
patterns = ['<em class="title">(.*)</em>', '<h2>(.*)</h2>']

key = True
i = 0
while key:
    if i%20==0:
        news = [get_weather()]
        for media, url, pattern in zip(medias, urls, patterns):
            news += get_title(media, url, pattern)
    else:
        pass
    i+=1

    text = random.choice(news)
    speed = 10
    width_num = 7
    height = 200
    width = height * len(text)

    img = np.zeros((height, width+height*width_num*2, 3), np.uint8)
    img = opencv2pil(img)

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('アプリ明朝.otf', height)
    draw.text((height*width_num, 0), text, 'white', font=font)
    img = pil2opencv(img)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, dsize=None, fx=0.2, fy=0.2)
    img = cv2.resize(img, dsize=None, fx=5, fy=5)

    for i in range(height*width_num , len(img[0]), speed):
        view_img = img[:, i-height*width_num :i]
        cv2.imshow("news", view_img)
        time.sleep(0.01)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            key = False
            break
    time.sleep(3)

cv2.destroyAllWindows()
