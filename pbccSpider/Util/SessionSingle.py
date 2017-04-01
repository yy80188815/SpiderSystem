import threading
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Singleton():
    instance=None
    mutex= threading.Lock()

    @staticmethod
    def GetInstance():
        if(Singleton.instance==None):
            Singleton.mutex.acquire()
            if(Singleton.instance==None):
                Singleton.instance= requests.session()
            Singleton.mutex.release()
        return Singleton.instance
