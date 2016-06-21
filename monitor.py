from queue import Queue
from sys import argv
import codecs

import colorama
from colorama import Fore, Back, Style

from opskin import *

COMMISION = 0.05

itemlist = []

colorama.init(autoreset=True)

def readItem(file):
    with codecs.open(file, encoding='utf-8-sig') as f:
        for line in f:
            itemlist.append(line.splitlines()[0])

print("# Reading item...")
readItem(argv[1])

bypassBotDetection()

print('{0:55} {1:>10} {2:>15} {3:>15} {4:>15} {5:>15}'.format('Name', 'Low', 'Second', 'Min', 'Average', 'Profit'))
print('-----------------------------------------------------------------------------------------------------------------------------------')

for _item in itemlist:
    item = OPSkinsItem(_item)

    try:
        itemInfo = item.getItemInfo()

        if itemInfo:
            price = itemInfo["price"];
            history_price = itemInfo["history_price"];

            lowest_price = price[0]

            for p in price:
                if p > price[0]:
                    second_lowest_price = p
                    break
            else:
                second_lowest_price = price[0]

            history_min = min(history_price)
            history_avg = round(float(sum(history_price) / len(history_price)), 2)

            profit = (second_lowest_price - second_lowest_price * COMMISION) - lowest_price

            print(Fore.BLUE + Style.BRIGHT + '{0:55} '.format(_item) 
                + Fore.GREEN + '{0:>10} '.format(str(lowest_price) + " USD") 
                + Style.RESET_ALL + '{0:>15} {1:>15} {2:>15}'.format(str(second_lowest_price) + " USD", str(history_min) + " USD", str(history_avg) + " USD") 
                + Fore.YELLOW + Style.BRIGHT + '{0:>15}'.format(str(int(profit)) + " USD"))
        else:
            print("Can't find such item: " + _item)

    except Exception as e:
        #print(item.html)
        print(Fore.RED + "\n[Error]: " + str(e) + " (" + _item + ")\n")
        continue


