s1 = " my python program  "
s2 = s1.strip()  # 去掉字符串s1首尾空格
print("去掉首尾空格后s2为：", s2)
print("将s2全部转换为大写：", s2.upper())
s3 = s2.replace(' ', ',')  # 将s2中的所有空格替换为英文逗号，赋值给s3
print(s3)
print("对s3进行正向字符串切片获取单词python：", s3[3:9])
ls = s3.split(',')  # 将s3进行分隔，返回包含三个字符串my、python、program的字符串列表
print(ls)
