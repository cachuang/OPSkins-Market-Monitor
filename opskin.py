from selenium import webdriver
from time import sleep
import http.cookiejar

REDIRECT_TIME = 10

# To bypass CloudFare bot detection, open the real browser to get the cookie 
def bypassBotDetection():
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'
    cj = http.cookiejar.CookieJar()

    # Set User-Agent
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.User-Agent'] = user_agent
    print('# Launching browser...')

    # Show the browser
    # browser = webdriver.Chrome()

    # Do not show the browser
    browser = webdriver.PhantomJS()

    print('# Heading to OPSkins.com...')
    browser.get("https://opskins.com/?loc=shop_search&app=730_2&search_item=%22AK-47%22")

    print('# Waiting to redirect...')
    sleep(REDIRECT_TIME)

    print('# Get cookies...')
    cookie = browser.get_cookies()

    print('# Closing browser...\n')
    browser.quit()

    for i in cookie:
        ck = http.cookiejar.Cookie(name=i['name'], value=i['value'], domain=i['domain'], path=i['path'], secure=i['secure'], rest=False, version=0, port=None, port_specified=False, domain_specified=False, domain_initial_dot=False, path_specified=True, expires=1522674906, discard=True, comment=None, comment_url=None, rfc2109=False)
        cj.set_cookie(ck)


