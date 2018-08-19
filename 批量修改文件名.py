import os
print('批量修改目标目录下的所有文件名。')
print('命名方式：前缀+序号+文件后缀。')
print('请确认目标目录下所有文件后缀名一致。')
path=input('请输入文件路径(结尾加上/)：')
pre = input('请输入文件名前缀：')
bac = input('请输入文件名后缀：')


#获取该目录下所有文件，存入列表中
f=os.listdir(path)

n=0
for i in f:
    
    #设置旧文件名（就是路径+文件名）
    oldname=path+f[n]
    
    #设置新文件名
    newname=path+pre+str(n+1)+'.'+bac
    
    #用os模块中的rename方法对文件改名
    os.rename(oldname,newname)
    print(oldname,'======>',newname)
    
    n+=1
