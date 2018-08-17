import matplotlib.pyplot as plt

# plt.scatter(2, 4, s=200)

# x_value = [1, 2, 3, 4, 5]
# y_value = [1, 4, 9, 16, 25]

x_value = list(range(1, 1001))
y_value = [x**2 for x in x_value]

# c用来设定数据点的颜色，edgecolors设置数据点轮廓
# 颜色映射突出数据规律
plt.scatter(x_value, y_value, c=y_value, cmap=plt.cm.Blues, edgecolors='none', s=40)

# 设置图表标题并给坐标轴加上标签
plt.title('Square Numbers', fontsize=24)
plt.xlabel('Value', fontsize=14)
plt.ylabel('Square of Value', fontsize=14)

# 设置刻度标记的大小
plt.tick_params(axis='both', which='major', labelsize=14)

plt.axis([0, 1100, 0, 1100000])

# 自动保存图表，参数一设置保存文件名，参数二设置裁剪图标多余空白区
# plt.savefig('squares_plot.png', bbox_inches='tight')

plt.show()