
import random
from Util.SessionSingle import Singleton


class nameCheck(object):

    def __init__(self):
        self.request = Singleton.GetInstance()

    def namecheck(self, name):
        num = random.random()
        url = 'https://ipcrs.pbccrc.org.cn/userReg.do'
        data = {
            'method':'checkRegLoginnameHasUsed',
            'loginname': name
        }
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
            'Referer':'https://ipcrs.pbccrc.org.cn/userReg.do',
            # 'Origin': 'https://ipcrs.pbccrc.org.cn',
            # 'Host': 'ipcrs.pbccrc.org.cn',
            # 'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            # 'Accept': 'text/plain,*/*;q = 0.01',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'zh - CN,zh;q = 0.8',
        }
        response = self.request.post(url, headers=header, data=data, verify=False)
        response = response.content.decode('gbk')

        return response
