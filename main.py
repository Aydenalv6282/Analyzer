import csv
import yfinance as yf
from matplotlib import pyplot as plt
import numpy
# https://www.nasdaq.com/market-activity/stocks/screener?exchange=NASDAQ&render=download
# opening the CSV file
# THOUGHT: THE BEST LEARNING RATE IS (1/(D2*1/(D3*1/(D4...))) While Dn != 0 ?
suitable = []

epochs = 100000  # LOOPS
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


def gradient_descent_linear(x_vals, y_vals, m_now, b_now):
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
    m = m_now - m_gradient * abs(1/m_gradient2)
    b = b_now - b_gradient * abs(1/b_gradient2)
    return m, b


def gradient_descent_sine(x_vals, y_vals, a_now, b_now, c_now, m_now, d_now):
    n = len(x_vals)
    a_gradient = 0
    b_gradient = 0
    c_gradient = 0
    m_gradient = 0
    d_gradient = 0
    a_gradient2 = 0
    b_gradient2 = 0
    c_gradient2 = 0
    m_gradient2 = 0
    d_gradient2 = 2/n+2
    # (Divide[1,n])*Sum[Power[\(40)y\(40)i\(41)-\(40)a*sin\(40)bx\(40)i\(41)+c\(41)+mx\(40)i\(41)+d\(41)\(41),2],{i,0,n}]
    for i in range(n):
        x = x_vals[i]
        y = y_vals[i]
        bx = b_now*x
        sbcx = numpy.sin(bx+c_now)
        cbcx = numpy.cos(bx+c_now)
        a_gradient += (-2/n)*(sbcx)*(y-(a_now*sbcx+d_now+m_now*x))
        a_gradient2 += (2/n)*(sbcx**2)
        b_gradient += (-2/n)*(a_now*cbcx*x)*(y-(a_now*sbcx+d_now+m_now*x))
        b_gradient2 += (2/n)*(a_now*(x**2))*(-a_now*(sbcx**2)+a_now*(cbcx**2)-d_now*sbcx-m_now*x*sbcx+y*sbcx)
        c_gradient += (-2/n)*(a_now*cbcx)*(y-(a_now*sbcx+d_now+m_now*x))
        c_gradient2 += (2/n)*(a_now)*(a_now*(cbcx**2)+y*sbcx-a_now*(sbcx**2)-d_now*sbcx-m_now*x*sbcx)
        m_gradient += (-2/n)*(x)*(y-(a_now*sbcx+d_now+m_now*x))
        m_gradient2 += (2/n)*(x**2)
        d_gradient += (-2/n)*(y-(a_now*sbcx+d_now+m_now*x))
    a = a_now - a_gradient * abs(1/a_gradient2)
    b = b_now - b_gradient * abs(1/b_gradient2)
    c = c_now - c_gradient * abs(1/c_gradient2)
    m = m_now - m_gradient * abs(1/m_gradient2)
    d = d_now - d_gradient * abs(1/d_gradient2)
    return a, b, c, m, d


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


suitable = ["AAPL"]
for s in suitable:
    stock = yf.Ticker(s)
    df = stock.history(start="2021-09-08", end="2021-10-08")
    x_vals = [c for c in range(len(df['Close']))]
    y_vals = df['Close']
    plt.scatter(x_vals, y_vals, color="blue")
    m1, b1 = 0, 0

    #Sine Variables
    a, b, c, m, d = 0.1, 0.1, 0.1, 0.1, 0.1
    for i in range(epochs):
        m1, b1 = gradient_descent_linear(x_vals, y_vals, m1, b1)
        a, b, c, m, d = gradient_descent_sine(x_vals, y_vals, a, b, c, m, d)
    m2, b2 = absolute_best_line(x_vals, y_vals)
    line_vals = []
    sine_x_vals = []
    sine_vals = []
    sine_smooth_vals = []
    for x in x_vals:
        line_vals.append(m1*x+b1)
        sine_vals.append(a * numpy.sin(b * x + c) + m * x + d)
    for i in range(len(x_vals)*100):
        x = i/100
        sine_smooth_vals.append(a * numpy.sin(b * x + c) + m * x + d)
        sine_x_vals.append(x)
    plt.plot(x_vals, line_vals, color="red")  # Linear Gradient Descent
    plt.plot(sine_x_vals, sine_smooth_vals, color="purple")  # Sine Gradient Descent
    print(sum(numpy.subtract(y_vals, sine_vals)), sum(numpy.square(numpy.subtract(y_vals, sine_vals))))
    print(a, b, c, m, d)
plt.show()
