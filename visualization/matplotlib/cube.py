import matplotlib.pyplot as plt

# x_value = [1, 2, 3, 4, 5]
# y_value = [1, 8, 27, 64, 125]

x_value = list(range(1, 5001))
y_value = [x * x * x for x in x_value]

# 设置图标并指定颜色映射
plt.scatter(x_value, y_value, c=y_value, cmap=plt.cm.Reds, s=20)

# 设置图表标题并给坐标轴加上标签
plt.title("Cube Numbers", fontsize=24)
plt.xlabel('Value', fontsize=14)
plt.ylabel('Cube of Value', fontsize=14)

# 设置刻度标记的大小
plt.tick_params(axis="both", which='major', labelsize=14)

# 设置每个坐标轴的取值范围
plt.axis([0, 5100, 0, 130000000000])

plt.show()
