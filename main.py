import csv
from urllib.request import urlopen
import yfinance as yf
from matplotlib import pyplot as plt
# https://www.nasdaq.com/market-activity/stocks/screener?exchange=NASDAQ&render=download
# opening the CSV file
suitable = []
L = 0.01  # LEARNING RATE
epochs = 1000  # LOOPS

with open('Assets/RAW_DATA.csv', mode='r') as file:
    # reading the CSV file
    csvFile = csv.reader(file)

    # displaying the contents of the CSV file
    cnt = 0
    for line in csvFile:
        if line[6] == "United States" and float(line[2].replace("$", "")) >= 6\
                and float(line[4].replace("%", "")) <= -10 and float(line[8]) > 86400:
            suitable.append(line[0])
            cnt += 1
    print(cnt)


def loss_function(m, b, x_vals, y_vals):
    total_error = 0
    n = len(x_vals)
    for i in range(len(x_vals)):
        total_error += (y_vals[i]-(m*x_vals[i]+b))**2
    return total_error/n


def gradient_descent(m_now, b_now, x_vals, y_vals):
    m_gradient = 0
    b_gradient = 0
    n = len(x_vals)
    for i in range(n):
        x = x_vals[i]
        y = y_vals[i]

        m_gradient += -(2/n) * x * (y - (m_now * x + b_now))
        b_gradient += -(2/n) * (y - (m_now * x + b_now))
    m = m_now - m_gradient * L
    b = b_now - b_gradient * L
    return m, b


suitable = ["TSLA"]
for s in suitable:
    stock = yf.Ticker(s)
    df = stock.history(start="2021-09-08", end="2021-10-08")
    x_vals = [c for c in range(len(df['Close']))]
    y_vals = df['Close']
    plt.scatter(x_vals, y_vals, color="blue")
    m = 0
    b = 0
    for i in range(epochs):
        m, b = gradient_descent(m, b, x_vals, y_vals)

    line_vals = []
    for x in x_vals:
        line_vals.append(m*x+b)

    plt.plot(x_vals, line_vals, color="red")
plt.show()
