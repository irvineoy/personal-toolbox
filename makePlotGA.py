#coding=utf-8
import numpy as np
import matplotlib.pyplot as pl
import os
N = 600
keyWord = 'individual_10'

def plotOneLine(keyWord, color, label):
    dotAndNub = r'1234567890.'
    allNumber = []
    for root, dirs, files in os.walk('/Users/irvine/Google Drive/Programming/Clanguage/graphData'):
        for filePath in files:
            if keyWord in filePath:
                filePath = os.path.join(root, filePath)
                print filePath
                with open(filePath, 'r') as f:
                    while True:
                        line = f.readline()
                        if line:
                            if 'max' in line:
                                line = line[5:]
                                maxNum = []
                                while True:
                                    temp = line[0]
                                    if temp in dotAndNub:
                                        line = line[1:]
                                        maxNum.append(temp)
                                    else:
                                        allNumber.append(float("".join(maxNum)))
                                        maxNum = []
                                        break
                        else:
                            break
    print len(allNumber)
    x1 = allNumber[:N]
    allNumber = allNumber[N + 1:]
    x2 = allNumber[:N]
    allNumber = allNumber[N + 1:]
    x3 = allNumber[:N]
    allNumber = allNumber[N + 1:]
    x4 = allNumber[:N]
    allNumber = allNumber[N + 1:]
    x5 = allNumber[:N]
    allNumber = allNumber[N + 1:]
    x6 = allNumber[:N]
    allNumber = allNumber[N + 1:]
    x7 = allNumber[:N]
    allNumber = allNumber[N + 1:]
    x8 = allNumber[:N]
    allNumber = allNumber[N + 1:]
    x9 = allNumber[:N]
    allNumber = allNumber[N + 1:]
    x10 = allNumber[:N]
    allNumber = allNumber[N + 1:]
    x = []
    y = []
    for i in range(N):
        temp = x1[i] + x2[i] + x3[i] + x4[i] + x5[i] + x6[i] + x7[i] + x8[i] + x9[i] + x10[i]
        temp = temp/10.0
        y.append(temp)
        x.append(i)
    return pl.plot(x, y, color, label = label)# use pylab to plot x and y

plot1 = plotOneLine('greedy__', 'r', 'Greedy Elite GA')
plot2 = plotOneLine('penalty__', 'g', 'Penalty Elite GA')
# plot3 = plotOneLine('crossover_06_', 'b', 'crossover:0.6')
# plot4 = plotOneLine('crossover_09_', 'c', 'crossover:0.9')


pl.xlabel('Generation number')
pl.ylabel('Fitness')
pl.legend(loc = 'center right')
pl.show()


        # if 'pen' in filePath:
        #     filePath = os.path.join(root, filePath)
        #     print filePath
        #     with open(filePath, 'r') as f:
        #         while True:
        #             line = f.readline()
        #             if line:
        #                 if 'max' in line:
        #                     line = line[5:]
        #                     maxNum = []
        #                     while True:
        #                         temp = line[0]
        #                         if temp in dotAndNub:
        #                             line = line[1:]
        #                             maxNum.append(temp)
        #                         else:
        #                             allNumber.append(float("".join(maxNum)))
        #                             maxNum = []
        #                             break
        #             else:
        #                 break



# print len(x1)
# for i in range(N):
#     temp = x1[i] + x2[i] + x3[i] + x4[i] + x5[i] + x6[i] + x7[i] + x8[i] + x9[i] + x10[i]
#     temp = temp/10.0
#     y.append(temp)
#     x.append(i)
# xx = []
# yy = []
# for i in range(N):
#     temp = yy1[i] + yy2[i]+ yy3[i]+ yy4[i]+ yy5[i]+ yy6[i]+ yy7[i]+ yy8[i]+ yy9[i]+ yy10[i]
#     temp = temp/10.0
#     yy.append(temp)
#     xx.append(i)

