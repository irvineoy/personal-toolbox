# -*- coding:utf-8 -*-  
import matplotlib.pyplot as pl
import matplotlib.ticker as ticker
from matplotlib.font_manager import FontProperties  
myfont = FontProperties(fname='/Library/Fonts/ipag.ttf')  

# font_prop = FontProperties(fname='/Library/Fonts/ipag.ttf')
# pl.rcParams['font.family'] = font_prop.get_name()
# , fontproperties=myfont

pl.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
pl.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
pl.rcParams['font.sans-serif']=['AppleGothic'] #用来正常显示中文标签
# pl.rcParams['font.family'] = ['Toppan Bunkyu Gothic'] #全体のフォントを設定
pl.rcParams["figure.figsize"] = [7, 4]
pl.rcParams['font.size'] = 10 #フォントサイズを設定 default : 12
pl.rcParams['xtick.labelsize'] = 15 # 横軸のフォントサイズ
pl.rcParams['ytick.labelsize'] = 15
pl.rcParams['axes.unicode_minus']=False #用来正常显示负号


# x1 = [0.001, 0.5, 1, 1.502, 2, 2.501, 3]
# y1 = [-1.001, -1.5, -1.998, -2.5, -2.997, -3.497, -3.996]
# kasan

# x1 = [-2.994, -1.996, -1.007, 0, 1.003, 1.998, 2.998]
# y1 = [2.986, 1.991, 1.003, 0, -1.001, -1.994, -2.991]
# hanten

# x1 = [-2.994, -2.001, -1, 0, 1, 2, 3]
# y1 = [-5.981, -3.996, -1.997, 0, 1.996, 3.994, 5.992]
# hihanten

x1 = [0, 0.501, 1, 1.501, 2]
y1 = [-1, -0.499, 0, 0.499, 0.998]
# gensan

# x1 = [99.9, 500, 1012, 2000, 3001, 4000, 6000, 8000, 10000, 12000, 15000, 20000, 30000, 40000, 50010]
# x2 = [100, 500, 1000, 2000, 3000, 4000, 6000, 8000, 10000, 12000, 15000, 20000, 30000, 40000, 50000]
# y1 = [0.035, 0.030, 0.026, 0.030, 0.039, 0.022, -0.202, -0.862, -2.086, -3.731, -6.521, -10.945, -17.822, -22.853, -26.985]
# y2 = [0.000, 0.000, 0.000, -0.004, -0.022, -0.069, -0.337, -0.988, -2.104, -3.604, -6.187, -10.404, -17.118, -22.057, -25.918]
# ALPF

# x1 = [100, 200.1, 300, 399.9, 500, 599, 800, 1199, 1500, 1999, 3000, 3499, 4001, 4999, 10000, 50000]
# y1 = [-42.499, -29.625, -22.437, -17.393, -13.581, -10.593, -6.254, -2.143, -1.076, -0.515, -0.336, -0.323, -0.318, -0.314, -0.318, -0.171]
# x2 = [100, 200, 300, 400, 500, 600, 800, 1200, 1500, 2000, 3000, 3500, 4000, 5000, 10000, 50000]
# y2 = [-42.052, -30.015, -22.989, -18.039, -14.259, -11.264, -6.916, -2.488, -1.195, -0.415, -0.085, -0.046, -0.027, -0.011, -0.001, 0.000]
# AHPF


# pl.xlabel(u'周波数f(Hz)', fontproperties=myfont)
# pl.ylabel(u'ゲインG(dB)')
# pl.semilogx(x1, y1, marker='o', color = 'k', label = u'ゲイン計算値')
# pl.semilogx(x2, y2, marker='', label = u'ケイン理論値')
# pl.scatter(x1, y1, marker='o', color='k', label=u'ゲイン計算値')


pl.xlabel(u'入力電圧(V)', fontproperties=myfont)
pl.ylabel(u'出力電圧(V)', fontproperties=myfont)
pl.scatter(x1, y1, marker='o', color='k', label=u'Output voltage')
pl.plot(x1, y1, label=u'Theoretical Output Voltage')


pl.legend(loc = 'upper left')
ax = pl.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
pl.show()


