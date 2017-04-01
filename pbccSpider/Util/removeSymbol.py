

class removeSymbol(object):

    def removesymbol(self, info):
        info = info.replace('\t','')
        info = info.replace('\n','')
        info = info.replace('\t','')
        info = info.replace('\xa0','')
        info = info.replace('\r','')
        info = info.replace('-','')
        info = info.replace(' ','')
        return info