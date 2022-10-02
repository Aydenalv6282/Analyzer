import csv
from urllib.request import urlopen
import yfinance as yf
from matplotlib import pyplot as plt
import numpy
# https://www.nasdaq.com/market-activity/stocks/screener?exchange=NASDAQ&render=download
# opening the CSV file
# THOUGHT: THE BEST LEARNING RATE IS (1/(D2*1/(D3*1/(D4...))) While Dn != 0
suitable = []

epochs = 50  # LOOPS

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


def loss_function(m, b, x_vals, y_vals):
    total_error = 0
    n = len(x_vals)
    for i in range(len(x_vals)):
        total_error += (y_vals[i]-(m*x_vals[i]+b))**2
    return total_error/n


def gradient_descent_linear(m_now, b_now, x_vals, y_vals):
    m_gradient = 0
    b_gradient = 0
    m_gradient2 = 0
    b_gradient2 = 2
    # M AND B ARE ONLY DIFFERENTIABLE 2 TIMES
    n = len(x_vals)
    for i in range(n):
        x = x_vals[i]
        y = y_vals[i]
        m_gradient += -(2/n) * x * (y - (m_now * x + b_now))
        b_gradient += -(2/n) * (y - (m_now * x + b_now))
        m_gradient2 += (2/n) * x**2
    m = m_now - m_gradient * abs((1/m_gradient2))
    b = b_now - b_gradient * abs((1/b_gradient2))
    print(m, b)
    line_vals_app = []
    for x in x_vals:
        line_vals_app.append(m*x+b)
    plt.plot(x_vals, line_vals_app, color="yellow")  # Gradient Descent
    return m, b


def absolute_best_line(x_vals, y_vals):  # AP STAT METHOD
    sy = numpy.std(y_vals)
    sx = numpy.std(x_vals)
    my = numpy.mean(y_vals)
    mx = numpy.mean(x_vals)
    nume = 0
    denomx = 0
    denomy = 0
    for i in range(len(x_vals)):
        nume += (x_vals[i]-mx)*(y_vals[i]-my)
        denomx += (x_vals[i]-mx)**2
        denomy += (y_vals[i]-my)**2
    denom = numpy.sqrt(denomx*denomy)
    r = nume/denom
    m = r*(sy/sx)
    b = my-m*mx

    return m, b


suitable = ["TSLA"]
for s in suitable:
    stock = yf.Ticker(s)
    df = stock.history(start="2021-09-08", end="2021-10-08")
    x_vals = [c for c in range(len(df['Close']))]
    y_vals = df['Close']
    plt.scatter(x_vals, y_vals, color="blue")
    m1 = 0
    b1 = 0
    for i in range(epochs):
        m1, b1 = gradient_descent_linear(m1, b1, x_vals, y_vals)
    m2, b2 = absolute_best_line(x_vals, y_vals)
    line_vals1 = []
    line_vals2 = []
    for x in x_vals:
        line_vals1.append(m1*x+b1)
        line_vals2.append(m2*x+b2)
    plt.plot(x_vals, line_vals2, color="green")  # Absolute Method (Stats)
    plt.plot(x_vals, line_vals1, color="red")  # Gradient Descent
plt.show()
