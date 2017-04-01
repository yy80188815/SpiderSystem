import re


class Re(object):

    # def ReYesOrNo(self, html, copm):
    #     compile= re.compile(copm)
    #     if len(compile.findall(html)) != 0:
    #         return True
    #     else:
    #         return False

    def reFind(self, html, comp):
        compile = re.compile(comp)
        if len(compile.findall(html)) != 0:
            return compile.findall(html)[0]
        else:
            return False

    def reFindAll(self, html, comp):
        compile = re.compile(comp)
        if len(compile.findall(html)) != 0:
            print(type(compile.findall(html)))
            return compile.findall(html)
        else:
            return False