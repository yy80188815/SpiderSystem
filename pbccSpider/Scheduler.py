from pbcc_Login_Register.Apply import Apply
from pbcc_Login_Register.Login import Login
from pbcc_Login_Register.Query import Query
from pbcc_Login_Register.Register import Register
class Scheduler(object):

    def __init__(self):
        self.login = Login()
        self.apply = Apply()
        self.query = Query()
        self.register = Register()
    def crawler(self):
        self.register.register()
        # self.login.login('yy80188815','yy1212520')
        # self.query.query()
         #self.apply.apply()


if __name__ == '__main__':
    spider = Scheduler()
    spider.crawler()