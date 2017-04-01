from Util.Re import Re
from Util.SessionSingle import Singleton
from Util.captcha import getCaptcha
from Util.nameCheck import nameCheck
import urllib
class Register(object):

    def __init__(self):

        self.request = Singleton.GetInstance()
        self.Re = Re()
        self.getcpatcha = getCaptcha()
        self.namecheck = nameCheck()

    def register(self):
        firstUrl = 'https://ipcrs.pbccrc.org.cn/login.do?method=initLogin'
        firstHeader = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64;rv:52.0) Gecko / 20100101 Firefox / 52.0',
            'Referer': 'https://ipcrs.pbccrc.org.cn/index1.do'
        }

        firstResponse = self.request.get(firstUrl, headers=firstHeader, verify=False)
        if firstResponse.status_code == 200:
            firstResponse = firstResponse.content.decode('gbk')
            tokenfirst = self.Re.reFind(firstResponse, r'TOKEN" value="(.*?)"')
            print('第一个页面请求成功')




        #获取第二个页面
        secondUrl = 'https://ipcrs.pbccrc.org.cn/userReg.do'
        secondHeader = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64;rv:52.0) Gecko / 20100101 Firefox / 52.0',
            'Referer':'https://ipcrs.pbccrc.org.cn/page/login/loginreg.jsp'
        }
        secondData = {
            'org.apache.struts.taglib.html.TOKEN': tokenfirst,
            'method': 'initReg'
        }
        secondResponse = self.request.post(secondUrl, headers=secondHeader, data=secondData, verify=False)
        if secondResponse.status_code == 200:
            secondResponse = secondResponse.content.decode('gbk')
            tokensecond = self.Re.reFind(secondResponse, r'TOKEN" value="(.*?)"')
            print('第二个页面请求成功')


        #获取第三个页面
        thirdUrl = 'https://ipcrs.pbccrc.org.cn/userReg.do'
        captcha = self.getcpatcha.predict()
        thirdHeader = {
            'Referer': 'https://ipcrs.pbccrc.org.cn/userReg.do',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            #'Accept': 'text/html, application xhtml+xml, application/xml;q=0.9,image/webp,*/*;q=0.8',
            #'Accept-Encoding': 'gzip, deflate, br',
           # 'Accept-Language': 'zh-CN,zh;q = 0.8',
           # 'Cache-Control': 'max-age=0',
            #'Connection': 'keep-alive',
           # 'Content-Length': '203',
            #'Host': 'ipcrs.pbccrc.org.cn',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
           # 'Origin': 'https://ipcrs.pbccrc.org.cn',
            #'Upgrade-Insecure-Requests': '1'
        }
        thirdData = {
            'org.apache.struts.taglib.html.TOKEN': tokensecond,
            'method':'checkIdentity',
            'userInfoVO.name': '王大丽',
            'userInfoVO.certType':'0',
            'userInfoVO.certNo': '532129198806123369',
            '_@IMGRC@_': captcha,
            '1':'on'
        }

       # thirdData = urllib.parse.urlencode(thirdData)
        thirdResponse = self.request.post(thirdUrl, headers=thirdHeader, data=thirdData, verify=False)
        thirdResponse = thirdResponse.content.decode('gbk')
        compileCaptchaError = self.Re.reFind(thirdResponse, r'(验证码输入错误)')
        while compileCaptchaError:
            captcha = self.getcpatcha.predict()
            thirdData = {
                 'org.apache.struts.taglib.html.TOKEN': tokensecond,
                 'method':'checkIdentity',
                 'userInfoVO.name': '杨帆',
                 'userInfoVO.certType':'0',
                 'userInfoVO.certNo': '510184198907130057',
                 '_@IMGRC@_': captcha,
                 '1':'on'
            }
            thirdresponse = self.request.post(thirdUrl, headers=thirdHeader,data=(thirdData), verify=False)
            thirdresponse = thirdresponse.content.decode('gbk')
            compileCaptchaError = self.Re.reFind(thirdresponse, r'(验证码输入错误)')
            print('')


        result = self.namecheck.namecheck('yy80188815')

        dmtUrl = 'https://ipcrs.pbccrc.org.cn/userReg.do';
        dtmHeader = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64;rv:52.0) Gecko / 20100101 Firefox / 52.0',
            'Referer': 'ipcrs.pbccrc.org.cn/userReg.do'
        }
        dtmData = {
            'method': 'getAcvitaveCode',
            'mobileTel': '18980920233'
        }
        dtmResponse = self.request.post(secondUrl, headers=dtmHeader, data=dtmData, verify=False)

