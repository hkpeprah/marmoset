#!/usr/bin/python
"""anonBrowser.py - Implements the anonymous browser for using the web behind a proxy.
   Implementation as expressed in Violent Python"""
import mechanize, cookielib, random

class anonBrowser(mechanize.Browser):
    """anonBrowser class is used for anonymously connecting to sites and performing searches.
       anonBrowser xtends the Browser class.
       Functions: change_proxy, clear_cookies, change_user_agent"""
    
    def __init__(self, proxies = [], user_agents = []):
        """constructor for the class"""
        mechanize.Browser.__init__(self) #inherit from mechanize Browser class
        self.set_handle_robots(False)
        self.proxies = proxies
        self.user_agents = user_agents + ['Mozilla/4.0', 'Firefox/6.01', 'ExactSearch', 'Nokia7110/1.0']
        self.cookie_jar = cookielib.LWPCookieJar()
        self.set_cookiejar(self.cookie_jar)
        self.anonymize()
    
    def clear_cookies(self):
        """clear the cookies stored from the session"""
        self.cookie_jar = cookielib.LWPCookieJar()
        self.set_cookiejar(self.cookie_jar)

    def change_user_agent(self):
        """change the user agent"""
        index = random.randrange(0, len(self.user_agents))
        self.addheaders = [('User-agent', (self.user_agents[index]))]

    def change_proxy(self):
        if self.proxies:
            index = random.randrange(0, len(self.proxies))
            self.set_proxies({'http': self.proxies[index]})
    
    def anonymize(self, sleep = False):
        """anonymizes the browser by clearing cookies and resetting the proxy and user agent"""
        self.clear_cookies()
        self.change_user_agent()
        self.change_proxy()
        if sleep:
            time.sleep(60)
