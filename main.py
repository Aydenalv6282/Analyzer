import csv
from urllib.request import urlopen
import json
import yfinance as yf
from matplotlib import pyplot as plt
# https://www.nasdaq.com/market-activity/stocks/screener?exchange=NASDAQ&render=download
# opening the CSV file
suitable = []
with open('Assets/RAW_DATA.csv', mode='r') as file:
    # reading the CSV file
    csvFile = csv.reader(file)

    # displaying the contents of the CSV file
    linenum = 0
    cnt = 0
    for line in csvFile:
        if line[6] == "United States" and 15 >= float(line[2].replace("$", "")) >= 6\
                and float(line[4].replace("%", "")) <= -10 and float(line[8]) > 86400:
            suitable.append(line[0])
            cnt += 1
        linenum += 1
    print(cnt)

for s in suitable:
    stock = yf.Ticker(s)
    df = stock.history(start="2022-09-08", )
    plt.plot(df['Close'])
print(suitable)
plt.show()
