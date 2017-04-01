from lxml import etree
from Util.removeSymbol import removeSymbol
from Util.Re import Re
class Parser(object):

    def parser(self, html):
      Credit = {}
      selector = etree.HTML(html)
      #基本信息
      basicInfo = {}
      infos = selector.xpath(r'//tr[2]/td/table[1]//td/strong/text()')
      for info in infos:
          temp = info.split('：')
          basicInfo[temp[0]] = temp[1]

      infos = selector.xpath(r'//tr[2]/td/table[2]//td/strong/text()')
      for info in infos:
          temp = info.split('：')
          if len(temp) == 1:
              basicInfo['婚否'] = temp[0]
          else:
              basicInfo[temp[0]] = temp[1]
      Credit['基本信息'] = basicInfo

      #信贷记录
      xindai = {}
      xindai = {}
      infos = selector.xpath(r'//tr[2]/td/table[3]//td/strong/text()')
      xindai['注释'] = infos[1].replace('\xa0','')
      infos = selector.xpath(r'//tr[2]/td/table[4]//td/text()')
      listinfo = ['信息概要']
      for info in infos:
          info = removeSymbol.removesymbol(self, info)
          if info != '':
              listinfo.append(info)
      #sinfos = str(infos).replace('\\n','').replace('\\r','').replace('\\t','').replace('\\`\\`','')
      xindai['信息概要'] = listinfo
      infos = selector.xpath(r'//tr[2]/td/table[4]//tr[1]/td[2]//span/text()')
      infofull = ''
      for info in infos:
          info = removeSymbol.removesymbol(self, info)
          if info != '':
            infofull += info
      xindai['逾期记录'] = infofull
      Credit['信贷记录'] = xindai

      #信用卡
      CreditCard = {}
      infos = selector.xpath(r'//div/div/table//tr[2]/td/ol[1]//text()')
      infolist = []
      #去除一些空的项
      for info in infos:
          info = removeSymbol.removesymbol(self, info)
          if info != '':
              infolist.append(info)

      key = infolist[0]
      infolist = infolist[1:]
      jsonlist = []

      for info in infolist:
          info = removeSymbol.removesymbol(self, info)
          if info != '':
              json = {}
              json['发卡时间'] = Re.reFind(self, info, r'(\d+年\d+月\d+日)')
              json['发卡行'] = Re.reFind(self, info, r'日(.*?)截')
              json['截止时间'] = Re.reFind(self, info, r'截至(.*?)，信用')
              print(Re.reFind(self, info, r'信用额度(.*?)，'))
              json['信用额度'] = Re.reFind(self, info, r'信用额度(.*?)，')
              json['已使用额度'] = Re.reFind(self, info, r'0，(.*?)。')
              jsonlist.append(json)
      CreditCard = {key:jsonlist}
      Credit['信用卡'] = CreditCard
      print(Credit)

      #公共记录

      recordlist = []
      infos = selector.xpath(r'//tr[2]/td/table[5]//text()')
      for info in infos:
          info = removeSymbol.removesymbol(self, info)
          if info != '':
              recordlist.append(info)
      recordlist = recordlist[1:]
      Credit['公共记录'] = recordlist

      #查询记录
      qrecordlist = []
      infos = selector.xpath(r'//tr[2]/td/table[7]//text()')
      for info in infos:
          info = removeSymbol.removesymbol(self, info)
          if info != '':
              qrecordlist.append(info)
      Credit['查询记录'] = qrecordlist
      print (Credit)


