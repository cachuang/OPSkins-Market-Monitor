from selenium import webdriver
from time import sleep
import http.cookiejar

import requests
from bs4 import BeautifulSoup

REDIRECT_TIME = 10
TIMEOUT = 5

user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'
header = {'User-Agent': user_agent}
cj = http.cookiejar.CookieJar()

# To bypass CloudFare bot detection, open the real browser to get the cookie 
def bypassBotDetection():
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

class OPSkinsItem():
    def __init__(self, name):
        self.name = name

    def getItemInfo(self):
        info = {}
        url = "https://opskins.com/index.php?loc=shop_search&search_item=" + self.name + "&sort=lh"
      
        response = requests.get(url, cookies=cj, headers=header, timeout=TIMEOUT)
        
        if "We couldn't find any items that matched your search criteria" in response.text:
            return None
        else:
            price = []
            history_price = []

            soup = BeautifulSoup(response.text, "html.parser")
            
            # find item's price
            # <div class='item-amount'>$10.00</div>
            for target in soup.find_all('div', class_='item-amount'):
                # convert the string format price into float, example: $1,000 -> 1000.0
                price.append(float(target.string.strip('$').replace(",", "")))
            
            # get item's history sale url
            # <a class='market-name market-link' href='?loc=shop_view_item&item=25500541'>
            temp = soup.find(class_='market-name market-link')
            history_url = "https://opskins.com/index.php" + temp['href']
            response = requests.get(history_url, cookies=cj, headers=header, timeout=TIMEOUT)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # <span class="pull-left">$5.81 <small>(Wear: 18.432%)</small></span>
            for target in soup.find_all('span', class_="pull-left"):
                history_price.append(float(target.contents[0].strip('$')))

            info['price'] = price
            info['history_price'] = history_price

            return info



