###登录mysql
    # 启动MySQL服务
    server mysql start
    
    # 链接MySQL
    mysql -u root -p
    
###数据库基本操作
    # 创建数据库
    create database 数据库名 charset=utf8;
    
    # 删除数据库
    drop database 数据库名;
    
    # 切换数据库
    use 数据库名;
    
    # 查看当前选择的数据库
    select database();
    
    # 显示所有数据库
    show databases;
    
###表操作
    # 查看当前数据库中所有表
    show tables;
    
    # 创建表
    create table 表名(id int auto_increment primary key, name varchar(20) not null, age int not null, gender bit default 1, isDelete bit default 0 );
    
    # 删除表
    drop table 表名;
    
    # 查看表结构
    desc 表名;
    
    # 查看建表语句
    show create table 表名;
    
    # 重命名表
    rename table 原表名 to 新表名
    
    # 修改表
    alter table 表名 add|change|drop 列名 类型;
      
###数据操作
####增加数据
    # 全列插入,根据表结构插入数据，id通常使用0占位
    insert into 表名 values(...);
    
    #缺省插入
    insert into 表名(列1， 列2， ...) values(值1， 值2， ...);
    
    # 同时插入多条数据
    insert into 表名 values(...), (...), ... ;
    
####删除数据
    # 根据条件删除数据，若无条件则删除整个表 
    delete from 表名 where 条件;
    
####修改数据
    # 根据条件修改数据，若无条件则整列修改
    update 表名 set 列1=值1， 列2=值2， ... where 条件;
    
####查询数据
    # 查询表中所有数据
    select * from 表名;
    
###查询（重点掌握）
####基本语法
    # *表示在结果集中显示所有列，可以为列名，列名之间用,分隔
    select * from 表名;
        
####消除重复行    
    # 在select后面列前面使用distinct可以消除重复行
    select distinct * from 表名;
    
####条件查询
    # 语法
    select * from 表名 where 条件;
    
    # 比较运算符
    等于          =
    大于          >
    小于          <
    大于等于       >=
    小于等于       <=
    不等于         !=或<>
    
    # 逻辑运算符
    and         并且 
    or          或者
    not         非
    
    # 模糊查询
    select * from 表名 where name like "...%"
    % 表示任意多个任意字符
    _ 表示一个任意字符
    
    # 范围查询
    select * from 表名 where id in (2, 3, 6) ;
    in 表示在一个非连续的范围内
    select * from 表名 where id between 2 and 6 ;
    between...and... 表示在一个连续的范围内
    
    # 空判断
    select * from 表名 where ... is null;
    is null 判断空
    select * from 表名 where ... is not null;
    is not null 判断非空
        null 和 " " 是不一样的
       
    # 优先级
    小括号 > not > 比较运算符 > 逻辑运算符
    and 比 or 优先级高
    
####聚合
    为了快速统计数据，提供了5个聚合函数
    
    # 表示计算总行数,小括号内可以写*或者列名
    select count(*) from 表名;
    
    # 求此列最大值
    select max(列名) from 表名 where 条件;
    
    # 求此列最小值
    select min(列名) from 表名 where 条件;
    
    # 求此列的和
    select sum(列名) from 表名;
    
    # 求此列平均值
    select avg(列名) from 表名;
####分组
    按照字段分组，表示此字段相同的数据会存放在同一个集合
    分组后只能查询出相同的数据列，有差异的数据列无法在结果中集中显示
    可以对分组后的数据进行统计，做聚合运算
    
    # 语法
    select 列1， 列2， 聚合... from 表名 group by 列1， 列2， ... 
    例：select gender count(*) from student group by gender;
    
    分组后的数据筛选
    select 列1， 列2， 聚合... from 表名 group by 列1， 列2， ... having 列1， ... 聚合...
    例：select gender, count(*) from student group by gender having gender ;
    
    where和having的区别：where是对from后面指定的表进行筛选，是对原始数据的筛选；having是对group by的结果进行筛选
    
####排序
    # 语法
    select * from 表名 order by 列1 asc|desc, 列2 asc|desc, ...;
    例：select * from student order by age, id;
    
    将数据按照列1进行排序，若某些列1的值相同，按照列2进行排序，...
    默认按照升序排列
    asc 升序
    desc 降序
####分页
    # 语法 start:索引从0开始 count:每页显示多少数据
    select * from 表名 limit start, count;

###关联表
####建表
    # 创建班级表
    create table class(id int quto_increment primary key, name varchar(20) not null, stuNum int not null)
    
    # 创建学生表并关联班级
    create table students(id int auto_increment primary key, name vaychar(20) not null, gender bit default 1, classid int not null, foreign key(classid) references class(id))
    
####关联查询
    select students.name, class.name from class inner join students on class.id=students.classid;
    select students.name, class.name from class left join students on class.id=students.classid;
    select students.name, class.name from class right join students on class.id=students.classid;    
    
####分类
    # 表A和表B匹配的行会出现在结果集中
    表A inner join 表B;
    
    # 表A和表B匹配的行会出现在结果集中，外加表A中独有的数据，为对应的数据用null填充
    表A left join 表B;
    
    # 表A和表B匹配的行会出现在结果集中，外加表B中独有的数据，为对应的数据用null填充
    表A right join 表B;
    
###PyMySQL
```python
import pymysql

# 连接数据库
# 参数1 mysql服务所在主机的ip
# 参数2 数据库用户名
# 参数3 数据库密码
# 参数4 数据库名
db = pymysql.connect('localhost', 'root', '123456', 'students')

# 创建一个cursor对象
cursor = db.cursor()

# 需要执行的SQL语句
sql = 'select version()'

# 执行SQL语句
cursor.execute(sql)

# 获取返回的信息
data = cursor.fetchone()

# 断开
cursor.close()
db.close()
```
```python
import pymysql

# 创建数据库表

# 连接数据库
db = pymysql.connect('localhost', 'root', '123456', 'students')

# 创建一个cursor对象
cursor = db.cursor()

# 检查表是否存在，存在则删除
cursor.execute('drop table if exists bandcard')

# 建表
sql = 'create table 表名(id int auto_increment primary key, name varchar(20) not null, age int not null, gender bit default 1, isDelete bit default 0 )'

# 执行SQL语句
cursor.execute(sql)

# 断开
cursor.close()
db.close()
```
```python
import pymysql

# 操作数据

# 连接数据库
db = pymysql.connect('localhost', 'root', '123456', 'students')

# 创建一个cursor对象
cursor = db.cursor()

# 检查表是否存在，存在则删除
# cursor.execute('drop table if exists bandcard')

# 插入数据
# sql = 'insert into bandcard(0, 100)'

# 更改数据
# sql = 'update bandcard set money=1000000 where id=1'

# 删除数据
# sql = 'delete from bandcard where money=100'

# 查询
# fetchone():获取下一个查询结果，结果是一个对象
sql = 'select * from bandcard where money>100'
try:
    cursor.execute(sql)
    reslist = cursor.fetchall()
    for row in reslist:
        print(row[0], row[1])

# fetchall():接收全部的返回行


# rowcount:是一个只读属性，



try:
    # 执行SQL语句
    cursor.execute(sql)
    db.commit()
except:
    # 若提交失败，回滚到上次数据
    db.rollback()



# 断开
cursor.close()
db.close()
```
####python与mysql交互函数封装
```python
import pymysql

class SunSql():
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        
    def connet(self):
        self.db = pymysql.connect(self.host, self.user, self.password, self.db)
        self.cursor = self.db.cursor
    
    def close(self):
        self.cursor.close()
        self.db.close()
        
    def get_one(self, sql):
        res = None
        try:
            self.connet()
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            self.close()
        except:
            print('查询失败')
        return res
        
    def get_all(self, sql):
        res = ()
        try:
            self.connet()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.close()
        except:
            print('查询失败')
        return res
    
    def insert(self, sql):
        return self.__edit(sql)
    
    def update(self, sql):
        return self.__edit(sql)
    
    def delete(self, sql):
        return self.__edit(sql)
    
    def __edit(self, sql):
        count = 0
        try:
            self.connet()
            count = self.close().execute(sql)
            self.db.commit()
            self.close()
        except:
            print('提交失败')
            self.db.rollback()
```        