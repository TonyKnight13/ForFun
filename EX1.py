import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sympy.geometry import Circle, Point, Line
from sympy.geometry import *
from sympy import *

# 若在 jupyter notebook 上执行，请取消下行注释
# %matplotlib inline

sns.set_style("darkgrid")


def inputPoint(r):
    '''
    功能：输入点
    '''
    flag = 1
    while flag:
        x = float(input('横坐标：'))
        y = float(input('纵坐标：'))
        if(x**2 + y**2 < r**2):
            flag = 0
        else:
            print("点不在圆内，请重新输入")
    return Point([x, y])


def findPoint(intersectionPointCL, r, p):
    '''
    功能：寻找大圆上除直角那个点外的其他点
    '''
    dist = 0
    pstack = [Point(0, 0)]
    for i in range(len(intersectionPointCL)):
        if p.distance(intersectionPointCL[i]) > dist:
            dist = p.distance(intersectionPointCL[i])
            pstack.pop()
            pstack.append(intersectionPointCL[i])
    op = pstack.pop()
    return op


def transPoint(p):
    '''
    功能：将sympy库封装的Point2D对象的横纵坐标取出
    '''
    return [p.x, p.y]


def plotTria(tps, inpsx, inpsy, r):
    '''
    功能：描两点，画直角三角形
    '''
    fig = plt.figure(figsize=(8, 8))

    ax = fig.add_subplot(111)
    circ = plt.Circle((0, 0), r,  color='b', alpha=0.1)
    pgon = plt.Polygon(tps, color='g', alpha=0.15)
    ax.add_patch(circ)
    ax.add_patch(pgon)

    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    # .xaxis.set_ticks_position设置x坐标刻度数字或名称的位置：属性值有top，bottom，both，default，none
    ax.xaxis.set_ticks_position('bottom')
    # 设置边框位置
    ax.spines['bottom'].set_position(('data', 0))
    # .yaxis.set_ticks_position设置y坐标刻度数字或名称的位置
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data', 0))

    plt.plot()
    plt.plot(inpsx, inpsy, '*')
    plt.show()


def main():
    '''
    思路：
    输入点不在圆内重新输入
    将两个点进行连接，以这条线段为直径做圆，与大圆相交
    三种情况：
    1.相交，两个直角三角形
    2.相切，一个直角三角形
    3.相离，无直角三角形
    '''

    inpsx = []
    inpsy = []

    r = float(input("圆的半径："))
    print("点1的坐标：")
    p1 = inputPoint(r)
    inpsx.append(p1.x)
    inpsy.append(p1.y)
    print("点2的坐标：")
    p2 = inputPoint(r)
    inpsx.append(p2.x)
    inpsy.append(p2.y)

    dis = p1.distance(p2)
    r1 = dis / 2
    o = Point(0, 0)
    o1 = p1.midpoint(p2)

    c1 = Circle(o, r)  # 大圆
    c2 = Circle(o1, r1)  # 小圆
    intersectionPoint = c1.intersection(c2)  # 求两圆交点

    lenPointList = len(intersectionPoint)
    if lenPointList == 0:
        print('不存在')
        return
    ips = []
    for p in intersectionPoint:
        ips.append(p)

    for i in range(len(ips)):
        OL1 = Line(ips[i], p1)
        intersectionPointCL = c1.intersection(OL1)
        op1 = findPoint(intersectionPointCL, r, ips[i])  # 直角三角形的第二个点

        OL2 = Line(ips[i], p2)
        intersectionPointCL = c1.intersection(OL2)
        op2 = findPoint(intersectionPointCL, r, ips[i])  # 直角三角形的第三个点

        tps = []

        if Point.is_collinear(ips[i], op1, op2) is not True:
            for p in list([ips[i], op1, op2]):
                tps.append(transPoint(p))
            plotTria(tps, inpsx, inpsy, r)

    return


main()
