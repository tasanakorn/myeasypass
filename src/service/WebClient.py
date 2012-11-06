import Cookie
from google.appengine.api import urlfetch

class WebClient:
    def __init__(self):
        self.cookie = Cookie.SimpleCookie()
    def request(self, url, data = None, isPost = False):
        method = urlfetch.GET
        if isPost:
            method = urlfetch.POST
        response = urlfetch.fetch(
                                    url,
                                    payload=data,
                                    method=method,
                                    headers=self._getHeaders(self.cookie),
                                    deadline=30
                                    )
        self.cookie.load(response.headers.get('set-cookie', ''))
        data = response.content        
        return data
    def _getHeaders(self, cookie):
        headers = {
                    'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2 (.NET CLR 3.5.30729)',
                    'Cookie' : self._makeCookieHeader(cookie)
                    }
        return headers    
    def _makeCookieHeader(self, cookie):
        cookieHeader = ""
        for value in cookie.values():
            cookieHeader += "%s=%s; " % (value.key, value.value)
        return cookieHeader    