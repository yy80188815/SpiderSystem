import os
import time
from PIL import Image
from pyocr import pyocr
from urllib.request import urlretrieve
from Util.SessionSingle import Singleton


class getCaptcha(object):
    def __init__(self):
        self.request = Singleton.GetInstance()

    def charReplace(self, chars):
        chars= chars.replace(".", "")
        chars= chars.replace("'", "")
        chars= chars.replace("\"", "")
        chars= chars.replace(";", "")
        chars= chars.replace(r"/","")
        chars= chars.replace(" ","")
        chars= chars.replace("\\\\", "")
        chars= chars.replace("-", "")
        chars= chars.replace("‘", "")
        chars= chars.replace("}", "")

        return chars

    def Download(self):
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
                'Referer': 'https://ipcrs.pbccrc.org.cn/index1.do'
            }
            #captchaImage\\' + str(time.time()) + '.jpg 自运行时候用这个目录
            captchapath = 'Util\\captchaImage\\' + str(time.time()) + '.jpg'
            response = self.request.get(r'https://ipcrs.pbccrc.org.cn/imgrc.do', headers=header, stream=True, verify=False)
            with open(captchapath, 'wb') as f:
                for chunk in response:
                    f.write(chunk)
                f.close()
            return captchapath
        except Exception as e:
            print(e)

    def predict(self):
        captchapath = self.Download()
        im = Image.open(captchapath)

        width = im.size[0];
        height = im.size[1]
        # 创建Draw对象:
        # draw = ImageDraw.Draw(im)
        # 填充每个像素:
        for x in range(0, width):
            for y in range(0, height):
                r, g, b = im.getpixel((x, y))
                if r > 130 and g > 130 and b > 130:
                    im.putpixel((x, y), (255, 255, 255))
                else:
                    im.putpixel((x, y), (0, 0, 0))
                    #   im.save('124.jpg')
        # 验证码破解
        tools = pyocr.get_available_tools()[:]
        #验证码修正表
        redata = {
            'I': 'r',
            'E': 'g',
            'G': '6',
            "L": 'i',
            "l": 'k'
        }
        captcha = tools[0].image_to_string(im, lang='eng')
        captcha = self.charReplace(captcha)
        l = list(captcha)
        for i in range(len(l)):
            for j in redata.keys():
                if l[i] == j:
                    l[i] = redata[j]

        newcaptcha = "".join(l)
        #预测完了 删除原来的验证图片
        os.remove(captchapath)
        return newcaptcha

if __name__=='__main__':
    getcaptcha = getCaptcha()
    print (getcaptcha.predict())