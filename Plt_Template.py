# -- coding: utf-8 --
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties
from scipy.special import comb
from scipy.interpolate import splrep, splev
import numpy as np

matplotlib.use("pgf")

latex_preamble = r'''
\usepackage{mathtools}
\usepackage{extarrows}
\usepackage{fontspec}
\usepackage{xeCJK}
\usepackage{xcolor}
\usepackage{unicode-math}
\setCJKmainfont{SimSun}
\setmainfont{Times New Roman}
\setmathfont{Latin Modern Math}
'''

pgf_config = {
        "font.family": 'serif',
        "pgf.rcfonts": False,
        "text.usetex": True,
        "pgf.preamble": latex_preamble,
}

rcParams.update(pgf_config)

x = [0, 1, 2, 3, 4, 5, 6]
y = [comb(6, i) for i in x]

tck = splrep(x, y, k=3)                     # 找到三次样条插值的表示，以拟合给定的x和y值
xnew = np.linspace(min(x), max(x), 1000)    # 在x值的范围内创建1000个等距的新x值
ynew = splev(xnew, tck)                     # 使用从splrep得到的tck评估新x值处的样条


fig, ax = plt.subplots()
ax.scatter(x, y, label=r'$n=6$') # 使用LaTeX字体
ax.plot(xnew, ynew, color='pink', label=r'$\frac{\varGamma \left( 7 \right)}{\varGamma \left( x+1 \right) \varGamma \left( 7-x \right)}$')
# 设置坐标轴刻度字体
ax.tick_params(axis='both', labelsize=12)
ax.set_xlabel(r'$x$ Value', fontsize=14) # 使用LaTeX字体
ax.set_ylabel(r'$y$ Value', fontsize=14) # 使用LaTeX字体
ax.set_title('Analytic Extension of $C_{n}^{x}$ - by know634', fontsize=16)

# 移动坐标轴交叉于点(0,0)
ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_color('none')

# 将y轴标签移动到左侧
ax.yaxis.set_label_coords(-0.1, 0.5)

# 将箭头添加到x和y轴
ax.plot((1), (0), ls='', marker='>', ms=6, color='k',
        transform=ax.get_yaxis_transform(), clip_on=False)
ax.plot((0), (1), ls='', marker='^', ms=6, color='k',
        transform=ax.get_xaxis_transform(), clip_on=False)

# 使用LaTeX在原点添加大写字母'O'
ax.text(-0.1, -0.5, r'$O$', fontsize=14, ha='right', va='top')

# 隐藏原点处的坐标值
X = [i for i in x if i != 0]
ax.set_xticks(X)
Y0 = [2.5 * i for i in range(1, 9)]
Y1 = [i for i in y if i != 0]
Y = sorted(list(set(Y0 + Y1)))
ax.set_yticks(Y)

# 创建一个指定字体的FontProperties对象
font_properties = FontProperties(family='Times New Roman')

# 获取当前的刻度位置
xticks = ax.get_xticks()
yticks = ax.get_yticks()

# 设置新的刻度标签，使用刚创建的字体属性
ax.set_xticklabels(xticks, fontproperties=font_properties)
ax.set_yticklabels(yticks, fontproperties=font_properties)

# 添加图例并将其放在左上角
ax.legend(bbox_to_anchor=(0.8, 1), fontsize=14)

# 美化
x0 = 1
y0 = comb(6, x0)
ax.axvline(x=x0, linestyle='--', color='r', ymin=(0 - plt.ylim()[0])/(plt.ylim()[1] - plt.ylim()[0]), ymax=(comb(6, x0) - plt.ylim()[0])/(plt.ylim()[1] - plt.ylim()[0]))
ax.axhline(y=y0, linestyle='--', color='r', xmin=(0 - plt.xlim()[0])/(plt.xlim()[1] - plt.xlim()[0]), xmax=(x0 - plt.xlim()[0])/(plt.xlim()[1] - plt.xlim()[0]))

ax.text(plt.xlim()[1] + 0.2, 0 - 0.6, r'$x$', fontsize=14, ha='right', va='top')
ax.text(0 - 0.2, plt.ylim()[1] + 0.8, r'$f(x)$', fontsize=14, ha='right', va='top')

# 保存
plt.savefig(f'Analytic Extension of Combinatorial Numbers.png', dpi=1200, bbox_inches='tight')