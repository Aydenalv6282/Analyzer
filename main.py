import csv
# https://www.nasdaq.com/market-activity/stocks/screener?exchange=NASDAQ&render=download
# opening the CSV file
with open('Assets/RAW_DATA.csv', mode='r') as file:
    # reading the CSV file
    csvFile = csv.reader(file)

    # displaying the contents of the CSV file
    cnt = 0
    for lines in csvFile:
        print(lines)
