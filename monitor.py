from sys import argv
import codecs

import colorama
from colorama import Fore, Style

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

itemlist.reverse()

while itemlist:
    item = OPSkinsItem(itemlist.pop())

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

            # There may not have any sale in history
            if history_price:
                history_min = min(history_price)
                history_avg = round(float(sum(history_price) / len(history_price)), 2)
            else:
                history_min = "N/A"
                history_avg = "N/A"

            profit = (second_lowest_price - second_lowest_price * COMMISION) - lowest_price

            print(Fore.BLUE + Style.BRIGHT + '{0:55} '.format(item.name) 
                + Fore.GREEN + '{0:>10} '.format(str(lowest_price)) 
                + Style.RESET_ALL + '{0:>15} {1:>15} {2:>15}'.format(str(second_lowest_price), str(history_min), str(history_avg)) 
                + Fore.YELLOW + Style.BRIGHT + '{0:>15}'.format(str(int(profit))))
        else:
            print('{0:55} {1:>10} {2:>15} {3:>15} {4:>15} {5:>15}'.format(item.name, "N/A", "N/A", "N/A", "N/A", "N/A"))

    except Exception as e:
        print(Fore.RED + "\n[Error]: " + str(e) + " (" + item.name + ")\n")
        itemlist.append(item.name)
        continue


