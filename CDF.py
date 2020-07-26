import matplotlib.pyplot as plt


cdf_filename = 'datamining2.txt'
flowCDFdt = []
with open(cdf_filename, 'r') as f:
    for l in f.readlines():
        flowCDFdt.append(([float(i) for i in str.split(l)]))
# print(flowCDFdt)
flowSizesdt = []
flowWeightsdt = []
flowWdt = []
prev = 0
for size in flowCDFdt:
    flowSizesdt.append(int(size[0]))
    flowWeightsdt.append(size[2] - prev)
    flowWdt.append(size[2])
    prev = size[2]
print(flowWdt)

cdf_filename = 'websearch2.txt'
flowCDFws = []
with open(cdf_filename, 'r') as f:
    for l in f.readlines():
        flowCDFws.append(([float(i) for i in str.split(l)]))
# print(flowCDFws)
flowSizesws = []
flowWeightsws = []
flowWws = []
prev = 0
for size in flowCDFws:
    flowSizesws.append(int(size[0]))
    flowWeightsws.append(size[2] - prev)
    flowWws.append(size[2])
    prev = size[2]
# print(flowSizesws)
# print(flowWeightsws)
print(flowWws)

from matplotlib.pyplot import MultipleLocator

# plt.figure(figsize=(5, 5))
# plt.plot(flowWdt, 'g*-')
# plt.plot(flowWws, 'r.-')
x=[pow(10,i) for i in range(0, 2)]
print(x)
# plt.xticks(x)
# # plt.xticks([0, 10, 100], [0, 10, 100])
# # plt.plot(flowSizesws, flowWws, 'r+-')
# # x = [1, 10, 100, 1000, 10000, 100000]
#  #设置纵坐标以十的次幂形式展现
#
#
# # plt.xticks([0, 10, 10e1, 10e2, 10e3, 10e4])   # 设置x刻度
# plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])   # 设置y刻度
#
# plt.show()

'''plot data'''
fig, ax = plt.subplots(figsize=(6, 3))
# plt.rcParams['savefig.dpi'] = 1000      # 图片像素
# plt.rcParams['figure.dpi'] = 1000        # 分辨率
# ax.semilogx(flowSizesdt, flowWdt, label='decay 1', color='r', linestyle='solid', linewidth=2)
# ax.semilogx(flowSizesws, flowWws, label='decay 2', color='g', linestyle='--', linewidth=2)
line1, = ax.semilogx(flowSizesdt, flowWdt, 'r^-')
line2, = ax.semilogx(flowSizesws, flowWws, 'g*--')
line1.set_label("datamining")
line2.set_label("websearch")
ax.legend((line1, line2), ("datamining", "websearch"))

ax.set_xlabel('Flow Size(KB)', fontsize=13)
ax.set_ylabel('CDF', fontsize=13)
ax.tick_params(labelsize=13)            # 刻度字体大小
# fig.legend(loc="upper right", fontsize=16, bbox_to_anchor=(1, 1), bbox_transform=ax.transAxes, ncol=1,
#            columnspacing=0.1, labelspacing=0.2, markerscale=1, shadow=True, borderpad=0.2, handletextpad=0.2)
fig.set_tight_layout(tight='rect')
# plt.legend(bbox_to_anchor=(1, 1),
#            bbox_transform=plt.gcf().transFigure)
# plt.legend(bbox_to_anchor=(1,1),
#         bbox_transform=ax.transAxes)
plt.savefig('CDF.svg')
plt.savefig('CDF.png')
plt.show()
