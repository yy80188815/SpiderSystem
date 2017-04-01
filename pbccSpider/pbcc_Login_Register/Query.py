from Util.SessionSingle import Singleton
from Util.Parser import Parser
from Util.Re import Re
class Query(object):

    def __init__(self):
        self.request = Singleton.GetInstance()
        self.parser = Parser
        self.Re = Re()
    def query(self):

        CreditUrl = 'https://ipcrs.pbccrc.org.cn/simpleReport.do?method=viewReport'
        CreditHeader = {
            'Referer': 'https://ipcrs.pbccrc.org.cn/reportAction.do?method=queryReport',
            'User-Agent': 'Mozilla/5.0(Windows NT 6.1;WOW64;rv:52.0)Gecko/20100101Firefox/52.0'
        }

        CreditData = {
            'counttime': '',
            'reportformat': '21',
            'tradeCode': 'xubjjc'
        }
        CreditReponse = self.request.post(CreditUrl, headers=CreditHeader, data=CreditData, verify=False)
        #这个报告要存一份到原始数据库
        CreditReponse = CreditReponse.content.decode('gbk')
        #调用解析器解析并放入数据库
        CodeError = self.Re.reFind(CreditReponse, r'(查询码输入错误，请重新输入)')
        if CodeError:
            print('查询码输入错误')
            exit()
        self.parser.parser(self,CreditReponse)
        print(type(CreditReponse))
        print('')

       #url : https://ipcrs.pbccrc.org.cn/simpleReport.do?method=viewReport
       #参数 : counttime:''
        #      reportformat : 21
        #      tradeCode:验证码
        # Referer : https://ipcrs.pbccrc.org.cn/reportAction.do?method=queryReport