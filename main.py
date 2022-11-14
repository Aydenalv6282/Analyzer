import csv
import yfinance as yf
from matplotlib import pyplot as plt
import numpy
import scipy
# https://www.nasdaq.com/market-activity/stocks/screener?exchange=NASDAQ&render=download
# opening the CSV file
# THOUGHT: THE BEST LEARNING RATE IS (1/(D2*1/(D3*1/(D4...))) While Dn != 0 ?
suitable = []

epochs = 100  # LOOPS
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


def sinusoid(x, a, b, c, m, d):
    return a*numpy.sin(b*x+c)+m*x+d


suitable = ["AAPL", "MSFT", "TSLA", "BBY"]
print(suitable)
for s in suitable:
    stock = yf.Ticker(s)
    df = stock.history(start="2021-09-08", end="2021-10-08")
    x_vals = [c for c in range(len(df['Close']))]
    y_vals = df['Close']
    plt.scatter(x_vals, y_vals, color="blue")
    plt.title(s)

    # Line Variables (To Estimate Sine Variables)
    ml, bl = numpy.polyfit(x_vals, y_vals, 1)
    line_vals = []
    resid = []
    for x in x_vals:
        line_vals.append(ml*x+bl)
        resid.append(y_vals[x]-line_vals[-1])

    # Sine Variables
    al = (abs(max(resid))+abs(min(resid)))/2
    popt, pcov = scipy.optimize.curve_fit(sinusoid, x_vals, y_vals, p0=[al, 0.5, 0, ml, bl], maxfev=100000)
    a, b, c, m, d = popt
    sine_x_vals = []
    sine_vals = []
    sine_smooth_vals = []
    for x in x_vals:
        sine_vals.append(a * numpy.sin(b * x + c) + m * x + d)
    for i in range(len(x_vals)*100):
        x = i/100
        sine_smooth_vals.append(a * numpy.sin(b * x + c) + m * x + d)
        sine_x_vals.append(x)

    plt.plot(x_vals, line_vals, color="red")  # Linear Regression
    plt.plot(sine_x_vals, sine_smooth_vals, color="purple")  # Sinusoidal Regression
    SSE = sum(numpy.square(numpy.subtract(y_vals, sine_vals)))  # Sine Square Error
    LSE = sum(numpy.square(numpy.subtract(y_vals, line_vals)))  # Line Square Error
    SE = sum(numpy.subtract(y_vals, sine_vals))  # Sine Error
    LE = sum(numpy.subtract(y_vals, line_vals))  # Line Error
    print(LSE/SSE, LSE, SSE)
    plt.show()
