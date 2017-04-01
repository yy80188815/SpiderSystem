from bs4 import BeautifulSoup
from Util.Re import Re
from Util.SessionSingle import Singleton


class Apply(object):
    def __init__(self):
        self.request = Singleton.GetInstance()
        self.Re = Re()
    def apply(self):
        try:
            #获取第一个申请页面
            firsturl = 'https://ipcrs.pbccrc.org.cn/reportAction.do?method=applicationReport'
            firstheader = {
                'Referer': 'https://ipcrs.pbccrc.org.cn/menu.do',
                'User-Agent': 'Mozilla/5.0(Windows NT 6.1;WOW64;rv:52.0)Gecko/20100101Firefox/52.0'
            }
            firstresponse = self.request.get(firsturl, headers=firstheader, verify=False).content.decode('gbk')

            #获取第一个页面的token
            tokenfirst = self.Re.reFind(firstresponse, r'TOKEN" value="(.*?)"')

            askdata = {
                'org.apache.struts.taglib.html.TOKEN': tokenfirst,
                'method':'checkishasreport',
                'authtype': '2',
                'ApplicationOption': '25',
                'ApplicationOption': '24',
                'ApplicationOption': '21'
            }
            askurl = 'https://ipcrs.pbccrc.org.cn/reportAction.do?method=checkishasreport'
            askheaders = {
                'Referer':'https://ipcrs.pbccrc.org.cn/reportAction.do?method=applicationReport',
                'User-Agent': 'Mozilla/5.0(Windows NT 6.1;WOW64;rv:52.0)Gecko/20100101Firefox/52.0'
            }

            #获取答题页面
            askresponse = self.request.post(askurl, headers=askheaders, data=askdata, verify=False).content.decode('gbk')
            soup = BeautifulSoup(askresponse,'lxml')
            lis = soup.find_all('li')
            asklist = []
            for li in lis:
                # Problem = BeautifulSoup.find(li,'p').text
                # asklist.append(Problem)
                Answers = BeautifulSoup.find_all(li,'span')
                for Answer in Answers:
                    asklist.append(Answer.text)
            #写入到数据库
            print (asklist)

            #等待客户输入答案
            param = self.Re.reFindAll(askresponse, r'value="(.*?)">')
            if len(param) == 0:
                print('获取失败')
            submitdata = {
                'org.apache.struts.taglib.html.TOKEN': param[0],
                'method':'',
                'authtype': '2',
                'ApplicationOption': '25',
                'ApplicationOption': '24',
                'ApplicationOption': '21',
                'kbaList[0].derivativecode': param[1],
                'kbaList[0].businesstype':param[2],
                'kbaList[0].questionno':param[3],
                'kbaList[0].kbanum': param[4],
                'kbaList[0].question': param[5],
                'kbaList[0].options1': param[6],
                'kbaList[0].options2': param[7],
                'kbaList[0].options3': param[8],
                'kbaList[0].options4': param[9],
                'kbaList[0].options5': param[10],
                'kbaList[0].answerresult':'1',          #
                'kbaList[0].options': '1',
                'kbaList[1].derivativecode': param[11],
                'kbaList[1].businesstype':param[12],
                'kbaList[1].questionno': param[13],
                'kbaList[1].kbanum': param[14],
                'kbaList[1].question': param[15],
                'kbaList[1].options1':param[16],
                'kbaList[1].options2': param[17],
                'kbaList[1].options3': param[18],
                'kbaList[1].options4': param[19],
                'kbaList[1].options5': param[20],
                'kbaList[1].answerresult': '1',
                'kbaList[1].options': '1',
                'kbaList[2].derivativecode': param[21],
                'kbaList[2].businesstype': param[22],
                'kbaList[2].questionno': param[23],
                'kbaList[2].kbanum': param[24],
                'kbaList[2].question': param[25],
                'kbaList[2].options1': param[26],
                'kbaList[2].options2': param[27],
                'kbaList[2].options3': param[28],
                'kbaList[2].options4': param[29],
                'kbaList[2].options5': param[30],
                'kbaList[2].answerresult': '1',
                'kbaList[2].options': '1',
                'kbaList[3].derivativecode': param[31],
                'kbaList[3].businesstype': param[32],
                'kbaList[3].questionno': param[33],
                'kbaList[3].kbanum': param[34],
                'kbaList[3].question': param[35],
                'kbaList[3].options1': param[36],
                'kbaList[3].options2': param[37],
                'kbaList[3].options3': param[38],
                'kbaList[3].options4': param[39],
                'kbaList[3].options5': param[40],
                'kbaList[3].answerresult': '1',
                'kbaList[3].options': '1',
                'kbaList[4].derivativecode': param[41],
                'kbaList[4].businesstype': param[42],
                'kbaList[4].questionno': param[43],
                'kbaList[4].kbanum': param[44],
                'kbaList[4].question': param[45],
                'kbaList[4].options1': param[46],
                'kbaList[4].options2': param[47],
                'kbaList[4].options3': param[48],
                'kbaList[4].options4': param[49],
                'kbaList[4].options5': param[50],
                'kbaList[4].answerresult': '1',
                'kbaList[4].options': '1',
            }
            submitheader = {
                'Referer': 'https://ipcrs.pbccrc.org.cn/reportAction.do?method=checkishasreport',
                'User-Agent': 'Mozilla/5.0(Windows NT 6.1;WOW64;rv:52.0)Gecko/20100101Firefox/52.0'
            }
            submitUrl = 'https://ipcrs.pbccrc.org.cn/reportAction.do?method=submitKBA'

            submitresponse = self.request.post(submitUrl, headers=submitheader, data=submitdata, verify=False)
            submitresponse = submitresponse.content.decode('gbk')
            compileResult = self.Re.reFind(submitresponse,r'(您于.*?申请正在受理，请耐心等待。)')
            Result = self.Re.reFind(submitresponse, r'(您的查询.*?获取结果)')
            if compileResult:
                print(compileResult)
            if Result:
                print(Result)
        except Exception as e:
            print(e)
if __name__=='__main__':
    app = Apply()
    app.apply()

