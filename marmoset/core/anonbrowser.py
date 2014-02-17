import mechanize
import cookielib
import random
import os


class AnonBrowser(mechanize.Browser):
    """
    The AnonBrowser is a browser class for navigating the web without
    leaving identification.  It supports loading session cookies,
    and making itself anonymous.
    """

    def __init__(self, proxies = [], 
                 user_agents = ['Mozilla/4.0', 'Firefox/6.01', 'ExactSearch', 'Nokia7110/1.0'], cookiefile = None):
        """
        Initialize the AnonBrowser instance.

        @param self: The current instance.
        @param proxies: List of proxies to use.
        @param user_agents: List of user agents.
        @param cookiefile: A cookiefile, if any, to use.
        @return: AnonBrowser
        """
        mechanize.Browser.__init__(self) #inherit from mechanize Browser class
        self.set_handle_robots(False)
        self.proxies = proxies
        self.user_agents = user_agents
        self.cookie_path = cookiefile
        self.cookie_jar = cookielib.MozillaCookieJar(cookiefile)
        self.set_cookiejar(self.cookie_jar)
        self.load_cookies()
        self.change_user_agent()
        self.change_proxy()

    def clear_cookies(self, cookiefile=None):
        """
        Clear the active cookies in the current session.

        @param self: The current instance.
        @param cookiefile: Name of new cookiefile
        @return: None
        """
        if cookiefile:
            self.cookie_path = cookiefile
            self.cookie_jar = cookielib.MozillaCookieJar(cookiefile)
        else:
            self.cookie_jar = cookielib.LWPCookieJar()
        self.set_cookiejar(self.cookie_jar)

    def delete_cookies(self):
        """
        Deletes a cook file on the system.

        @param self: The current instance
        @return: None
        """
        self.clear_cookies()
        try:
            os.remove(self.cookie_path)
        except OSError:
            pass

    def load_cookies(self):
        """
        Load the file in the current cookie jar into the browser
        session.
        
        @param self: The current instance
        @return: None
        """
        try:
            self.cookie_jar.load(ignore_discard=True, ignore_expires=True)
        except IOError:
            pass

    def save_cookies(self):
        """
        Save the cookie jar.

        @param self: The current instance.
        @return: None
        """
        self.cookie_jar.save(ignore_discard=True, ignore_expires=True)

    def change_user_agent(self):
        """
        Change the active user agent; a user agent is selected randomly.

        @param self: The current instance.
        @return: None
        """
        index = random.randrange(0, len(self.user_agents))
        self.addheaders = [('User-agent', (self.user_agents[index]))]

    def change_proxy(self):
        """
        Change the proxy being used; a proxy is selected randomly.

        @param self: The current instance.
        @return: None
        """
        if self.proxies:
            index = random.randrange(0, len(self.proxies))
            self.set_proxies({'http': self.proxies[index]})

    def anonymize(self, sleep = False):
        """
        Anonymizes the current browser instance by clearing cookies and changing
        the proxies and user agents.

        @param self: The current instance.
        @param sleep: Whether to stall the instance or not.
        @return: None
        """
        self.clear_cookies()
        self.change_user_agent()
        self.change_proxy()
        if sleep:
            time.sleep(60)
