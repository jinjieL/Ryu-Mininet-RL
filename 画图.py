import matplotlib.pyplot as plt

# x_values =list(range(11))
# # x轴的数字是0到10这11个整数
# y_values =[ x**2 for x in x_values]
# # y轴的数字是x轴数字的平方
# plt.plot(x_values ,y_values ,c='green')
# # 用plot函数绘制折线图，线条颜色设置为绿色
# plt.title('Squares' ,fontsize=24)
# # 设置图表标题和标题字号
# plt.tick_params(axis='both' ,which='major' ,labelsize=14)
# # 设置刻度的字号
# plt.xlabel('Numbers' ,fontsize=14)
# # 设置x轴标签及其字号
# plt.ylabel('Squares' ,fontsize=14)
# # 设置y轴标签及其字号
# plt.show()
# # 显示图表
#
# import matplotlib.pyplot as plt
# from matplotlib.pyplot import MultipleLocator
#
# # 从pyplot导入MultipleLocator类，这个类用于设置刻度间隔
#
# x_values = list(range(11))
# y_values = [x ** 2 for x in x_values]
# plt.plot(x_values, y_values, c='green')
# plt.title('Squares', fontsize=24)
# plt.tick_params(axis='both', which='major', labelsize=14)
# plt.xlabel('Numbers', fontsize=14)
# plt.ylabel('Squares', fontsize=14)
# x_major_locator = MultipleLocator(1)
# # 把x轴的刻度间隔设置为1，并存在变量里
# y_major_locator = MultipleLocator(10)
# # 把y轴的刻度间隔设置为10，并存在变量里
# ax = plt.gca()
# # ax为两条坐标轴的实例
# ax.xaxis.set_major_locator(x_major_locator)
# # 把x轴的主刻度设置为1的倍数
# ax.yaxis.set_major_locator(y_major_locator)
# # 把y轴的主刻度设置为10的倍数
# plt.xlim(-0.5, 11)
# # 把x轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白
# plt.ylim(-5, 110)
# # 把y轴的刻度范围设置为-5到110，同理，-5不会标出来，但是能看到一点空白
# plt.show()

# import matplotlib.pyplot as plt
# import numpy as np
#
# n = 50
# x = np.arange(n)
# y = np.random.normal(size=n)
#
# plt.plot(x, y, '.-')
# plt.xticks([0, 6, 20, 36, 48], [0, 6, 20, 36, 48])
# plt.show()


# x=[pow(10,i) for i in range(0,10)]
# y=range(0,len(x))
# plt.plot(x, y, 'r')
# plt.xscale('log')#设置纵坐标的缩放
# plt.show()

"""
    plot semilogx line.
"""

'''get data ready.'''
number_of_point = 1001
x_data = range(1, number_of_point)
y_data_1 = [(99/100)**i + 0.2 for i in x_data]
y_data_2 = [(99/100)**i for i in x_data]
print(y_data_1)
print(len(y_data_2))

'''plot data'''
fig, ax = plt.subplots(figsize=(5, 4))
plt.rcParams['savefig.dpi'] = 1000       # 图片像素
plt.rcParams['figure.dpi'] = 1000        # 分辨率
ax.semilogx(x_data, y_data_1, label='decay 1', color='r', linestyle='solid', linewidth=2)
ax.semilogx(x_data, y_data_2, label='decay 2', color='g', linestyle='--', linewidth=2)
ax.set_xlabel('The index of x', fontsize=13)
ax.set_ylabel('The value of y', fontsize=13)
ax.tick_params(labelsize=13)            # 刻度字体大小
fig.legend(loc="upper right", fontsize=16, bbox_to_anchor=(1, 1), bbox_transform=ax.transAxes, ncol=1,
           columnspacing=0.1, labelspacing=0.2, markerscale=1, shadow=True, borderpad=0.2, handletextpad=0.2)
fig.set_tight_layout(tight='rect')
# plt.savefig("exponential_decay.png")
plt.show()
