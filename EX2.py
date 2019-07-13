import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import seaborn as sns
from sympy.geometry import Circle, Point, Line
from sympy import *

sns.set_style("darkgrid")


def inputCirc():

    r = float(input('半径；'))
    x = float(input('圆心横坐标：'))
    y = float(input('圆心纵坐标：'))
    o = Point(x, y)
    c = Circle(o, r)
    return o, c, r


def main():
    print('圆1')
    o1, c1, r1 = inputCirc()
    print('圆2')
    o2, c2, r2 = inputCirc()

    intersectionPoint = c1.intersection(c2)  # 求两圆交点
    lenPointList = len(intersectionPoint)
    if lenPointList == 0:
        print('两圆相离')
        return
    
    lpsx = []
    lpsy = []
    ls = []
    
    fig = plt.figure(figsize=(8, 8))

    ax = fig.add_subplot(111)
    circ1 = plt.Circle((o1.x, o1.y), r1,  color='b', alpha=0.1)
    circ2 = plt.Circle((o2.x, o2.y), r2,  color='g', alpha=0.1)
    ax.add_patch(circ1)
    ax.add_patch(circ2)

    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    # .xaxis.set_ticks_position设置x坐标刻度数字或名称的位置：属性值有top，bottom，both，default，none
    ax.xaxis.set_ticks_position('bottom')
    # 设置边框位置
    ax.spines['bottom'].set_position(('data', 0))
    # .yaxis.set_ticks_position设置y坐标刻度数字或名称的位置
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data', 0))

    if o1.y == o2.y:
        
        for i in range(len(intersectionPoint)):
            pl1 = intersectionPoint[i]
            lpsx.append(pl1.x)
            lpsy.append(pl1.y)

            x = np.arange(2 * abs(o1.x - o2.x) + 1)
            x = x + pl1.x - abs(o1.x - o2.x)
            y = np.zeros_like(x)
            y = y + pl1.y
            ls.append(lines.Line2D(x, y, color='r', alpha=0.2713))

            ax.add_line(ls[i])
    else:
        rdis2 = r1 ** 2 - r2 ** 2
        for i in range(len(intersectionPoint)):
            pl1 = intersectionPoint[i]
            m = Symbol('m')
            n = Symbol('n')
            out = solve([pl1.y + m * pl1.x + n, rdis2 * (m**2 + n**2) +
                         (o2.y + o2.x * m + n)**2 - (o1.y + o1.x * m + n)**2], [m, n])

            x = np.arange(2 * abs(o1.x - o2.x) + 1)
            x = x + pl1.x - abs(o1.x - o2.x)
            
            y = -(out[0][0] * x + out[0][1])

            lpsx.append(pl1.x)
            lpsy.append(pl1.y)

            ls.append(lines.Line2D(x, y, color='r', alpha=0.2713))

            ax.add_line(ls[i])

    plt.plot(lpsx, lpsy, '*')

    plt.show()


main()

