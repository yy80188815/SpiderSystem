import time
from Util.SessionSingle import Singleton
from Util.captcha import getCaptcha
from Util.Re import Re


class Login(object):

    def __init__(self):
        self.request = Singleton.GetInstance()
        self.getcpatcha = getCaptcha()
        self.Re = Re()
    def login(self, username, password):

        firstHeader = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64;rv:52.0) Gecko / 20100101 Firefox / 52.0',
            'Referer':'https://ipcrs.pbccrc.org.cn/index1.do'
        }
        #获取第一个页面的token
        firstUrl = 'https://ipcrs.pbccrc.org.cn/login.do?method=initLogin'
        firstresponse = self.request.get(firstUrl, headers = firstHeader,verify=False).content.decode('gbk')
        tokenfirst = self.Re.reFind(firstresponse,r'TOKEN" value="(.*?)"')


        #验证码下载预测
        captcha = self.getcpatcha.predict()
        #获取登陆页面
        loginpostdata = {
            'org.apache.struts.taglib.html.TOKEN':tokenfirst,
            'method':'login',
            'data': time.time() * 1000,
            'loginname': username,
            'password': password,
            '_@IMGRC@_':captcha,
        }

        loginHeader = {
            'User-Agent': 'Mozilla/5.0(Windows NT 6.1;WOW64;rv:52.0)Gecko/20100101Firefox/52.0',
            'Referer': 'https://ipcrs.pbccrc.org.cn/page/login/loginreg.jsp'
        }
        try:
            response = self.request.post('https://ipcrs.pbccrc.org.cn/login.do', headers=loginHeader,
                                         data=loginpostdata, verify=False)
            if response.status_code == 200:
                response = response.content.decode('gbk')
                compileerror = self.Re.reFind(response,r'(因登录名与密码.*?分钟。)')
                compilePassword = self.Re.reFind(response, r'(登录名或密码错误)')
                if compileerror :
                    #错误登陆5次
                    #把状态码和错误原因存入数据库然后退出
                    print(compileerror)
                    exit()

                elif compilePassword:
                    # 密码错误
                    print(compilePassword)
                    exit()

                #验证码输入错误
                compileCaptchaError = self.Re.reFind(response, r'(验证码输入错误)')
                while compileCaptchaError:
                    captcha = self.getcpatcha.predict()
                    loginpostdata = {
                        'org.apache.struts.taglib.html.TOKEN': tokenfirst,
                        'method': 'login',
                        'data': time.time() * 1000,
                        'loginname': username,
                        'password': password,
                        '_@IMGRC@_': captcha,
                    }
                    response = self.request.post('https://ipcrs.pbccrc.org.cn/login.do', headers=loginHeader,
                                                 data=loginpostdata, verify=False)
                    response = response.content.decode('gbk')
                    compileCaptchaError = self.Re.reFind(response, r'(验证码输入错误)')
                print('登陆成功')
            else:
                #存入数据库失败原因
                exit()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    login = Login()
    login.crawl('zxc80188815','yy1212520')