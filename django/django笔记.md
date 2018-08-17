##创建项目
	1.在合适位置创建一个目录
	2.进入目录
	3.输入 （django-admin startproject --） 进行创建项目
	4.目录层级说明
		manag.py  一个命令行工具，用多种方式对Django项目进行交互
		project文件夹目录
			__init__.py  一个空文件，表示此目录是一个python包
			settings.py  项目的配置文件
			urls.py  项目的url声明
			wsgi.py  项目与wsgi兼容的web服务器入口

##基本操作
	1.设计表结构
		班级表结构
			表名：grades
			字段：
				班级名称：gname
				成立时间：gdate
				男生总数：ggirlnum
				女生总数：gboynum
				是否删除：isDelete
		学生表结构
			表名：students
			字段：
				姓名：sname
				性别：sgender
				年龄：sage
				简介：scontent
				所属班级：sgrade
				是否删除：isDelete
	2.配置数据库
		！！！注意：创建数据库是要制定编码格式！！！
		注意：Django默认使用SQLite	
		在settings.py中，通过database选项进行数据库配置
		配置MySQL
			验证MySQL版本
			在__init__.py中写入两行代码
				import pymysql
				pymysql.install_as_MySQLdb()
			在settings.py中配置数据库
			DATABASES = {
    			'default': {
        			'ENGINE': 'django.db.backends.mysql',
        			'NAME': '数据库名',
        			'USER': '用户名',
        			'PASSWORD': '数据库密码',
        			'HOST': '数据库服务器IP',
        			'PORT': '端口',
    			}
			}
	3.创建应用
		在一个项目中可以创建多个应用，每个应用进行一种业务处理
		进入项目所在目录
		执行（python manage.py startapp myapp）
		myapp目录说明
			admin.py：站点配置
			models.py：模型
			views.py：视图
	4.激活应用
		在settings.py中，将myapp应用加入到INSTALLED_APPS中
	5.定义模型
		概述：有一个数据表，就对应有一个模型
		在models.py中定义模型
			from django.db import models

			模型类要继承models.Model类
				class Grades(models.Model):
				...
				class Students(models.Model):
				...
		说明：不需要定义主键，在生成时自动添加，切会自动增加
	6.在数据库中生成数据表
		生成迁移文件
			执行（python manage.py makemigrations）
			在migrations目录下生成一个迁移文件，数据库中还没有数据表
		执行迁移
			执行（python manage.py migrate）
			相当于执行SQL语句，创建数据表
	7.测试数据操作
		进入到python shell：执行（python manage.py shell）
			引入包：
				from myapp.models import Grades,Students
				from django.utils import timezone
				from datetime import *
			查询所有数据：类名.objects.all()
			添加数据：
				本质：构建一个模型类的对象实例
				grsde1=Grades()
				grade1.gname=""
				...
			查看某个对象：类名.objects.get(pk=1)
			修改数据：模型对象.属性=新值（别忘记save）
			删除数据：模型对象.delete()（注意：物理删除，数据库中表里的数据被删除）
			关联对象：
				创建学生对象
				获得关联对象的集合：grade1.students_set.all()
				直接添加到班级：stu3=grase1.students_set.create(sname=u"",...)
					使用中文前面要加u进行转码
	8.启动服务器
		格式：python manage.py runserver ip:port
			说明：ip默认为本机ip；端口号默认8000
			纯python写的轻量级web服务器，用于开发测试
	9.Admin站点管理
		概述：
			内容发布：添加、修改、删除内容
			公告访问：
		配置Admin应用：
			在settings.py中INSTALLED_APPS中添加'django.contrib.admin',
		创建管理员用户：
			执行（python manage.py createsuperuser）然后按提示操作
			name：chen； pwd：qq1234567890
		汉化：settings.py中LANGUAGE_CODE = 'zh-hans'  TIME_ZONE = 'Asia/Shanghai'
		管理数据表：
			修改admin.py文件
				# 注册
				admin.site.register(Grades)
				admin.site.register(Students)
			自定义管理页面：
				列表页属性：
					list_display 显示字段
				    list_filter 过滤字段
				    search_fields 搜索字段
				    list_per_page 分页
				添加、修改页属性：
					fields 规定属性的先后顺序
    				fieldsets 给属性分组
    					注意：fields与fieldsets不能同时使用
		    			fieldsets = [
					        ('num',{'fields':['ggirlnum','gboynum']}),
					        ('base',{'fields':['gname','gdate','isDelete']}),
					    ]
                关联对象：需求，创建班级时自动添加几个学生
                    class StudentsInfo(admin.TabularInline):
                        model = Students
                        extra = 2
                    class GradesAdmin(admin.ModelAdmin):
                        inlines = [StudentsInfo]
                        ...
                布尔值显示问题：
                        def gender(self):
                            if self.sgender:
                                return '男'
                            else:
                                return '女'
                设置页面列的名称:
                    gender.short_description = '性别'
                执行动作位置：
                    actions_on_top = False
                    actions_on_bottom = True
            使用装饰器完成注册：
                @admin.register(Students)
                class StudentsAdmin(admin.ModelAdmin):
                    ...
    10.视图的基本使用
        概述：
            在django中，视图对web请求进行回应
            就是一个python函数，在views.py中定义
        定义视图：
            from django.http import HttpResponse
            def index(request):
                return HttpResponse('sunck is a good man...')
        配置url：
            修改project目录下的urls.py
                url(r'^', include('myapp.urls')),
            创建并修改myapp目录下的urls.py
                from django.conf.urls import url
                from . import views
                urlpatterns=[
                    url(r'^$', views.index)
                ]
    11.模板的基本使用
        概述：
            模板是HTML页面，可以根据视图中传递过来的数据进行填充
        创建模板目录：
            创建templates目录，在目录下创建对应的模板目录（project/templates/myapp）
        配置模板路径：
            修改settings.py中的TEMPLATES
                'DIRS': [os.path.join(BASE_DIR, 'templates')],
        定义grades.html和students.html两个模板：
            模板语法：
                {{输出值：可以是变量，也可以是对象.属性}}
                {%执行代码%}
        写模板（templates/myapp）-定义视图(views)-配置url(projects/myapp/urls)
        点击班级显示对应的学生列表

##模型
    django对各种数据库都提供了很好的支持，为这些数据库提供了统一的调用API，可以根据不同的业务需求选择数据库
    配置数据库：
        工程目录下的__init__.py文件添加：
            import pymysql
            pymysql.install_as_MySQLdb()
        修改settings.py文件：
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': 'kaige',
                    'USER': 'root',
                    'PASSWORD': '123456',
                    'HOST': 'localhost',
                    'PORT': '3306',
                }
            }
    开发流程：
        配置数据库
        定义模型类：一个模型类在数据库中对应一张表
        生成迁移文件
        执行迁移生成数据表
        使用模型类进行增删改查操作
    ORM：
        对象-关系-映射
        任务：
            根据对象类型生成表结构
            将对象、列表的操作转换成sql语句
            将sql语句查询到的结果转换为对象、列表
        优点：极大减轻开发人员的工作量，不需要面对因数据库的变更修改代码的问题
    定义模型：
        模型-属性-表-字段 --> 之间的关系
            一个模型类在数据库中对应一张表，在模型类中定义的属性，对应该模型对应表中的字段
        定义属性：

        创建模型类：

        元选项：
            在模型类中定义Meta类，用于设置元信息
                db_table 定义数据表名，推荐使用小写字母，默认为项目名小写.类名小写
                ordering 对象的默认排序字段，获取对象的列表时使用
                    注意：排序会增加数据库开销
    模型成员：
        类属性：
            objects：
                是manager类型的一个对象，作用是与数据库进行交互
                定义模型类时没有指定管理器，则diango为模型创建一个名为objects的管理器
            自定义管理器：
                class Students(models.Model):
                    # 自定义模型管理器，之后django就不会再生成objects管理器
                    stuObj = models.Manager()
            自定义管理器Manager类：
                模型管理器是django的模型与数据库进行交互的接口，一个模型可以有多个模型管理器
                作用：
                    向管理器类中添加额外的方法
                    修改管理器返回的原始查询集--重写get_queryset()方法

                    class StudentsManager(models.Manager):
                        def get_queryset(self):
                            return super(StudentsManager, self).get_queryset().filter(isDelete=False)
                    class Students(models.Model):
                        # 自定义模型管理器，则objects将不再存在
                        # stuObj1 = models.Manager()
                        # stuObj2 = StudentsManager()
        创建对象：
            目的：向数据库添加数据
            创建对象时，django不会对数据库进行读写操作，当调用save()方法时才与数据库交互，将对象保存在数据库中
            注意：__init__方法已经在父类models.Model中使用，在自定义的模型中无法使用
            方法：
                在模型类中增加一个类方法
                    class Students(models.Model):
                        @classmethod
                        def createStudent(cls, name, age, gender, contend, grade, lastT, createT, isD=False):
                            stu = cls(sname =name, sage = age, sgender = gender, scontend = contend, sgrade = grade, lastTime= lastT, createTime = createT, isDelete = isD)
                            return stu
                在自定义管理器中添加一个方法
                    class StudentsManager(models.Manager):
                        def createStudent(self, name, age, gender, contend, grade, lastT, createT, isD=False):
                            stu = self.model()
                            stu.sname = name
                            stu.sage = age
                            stu.sgender = gender
                            stu.contend = contend
                            stu.sgrade = grade
                            stu.lastTime = lastT
                            stu.createTime = createT
                            return stu
    模型查询：
        概述：
            查询集：表示从数据库中获取的对象的集合
            查询集可以有多个过滤器
            过滤器就是一个函数，是基于所给的参数限制查询集结果
            从sql角度来说，查询集和select语句等价过滤器就像where条件
        查询集：
            在管理器上调用过滤方法返回查询集
            查询集经过过滤器筛选后返回新的查询集，所以可以写成链式调用
            惰性执行：创建查询集不会带来任何数据库的访问，直到调用数据时
            直接访问数据的情况：
                迭代
                序列化
                与if合用
            返回查询集的方法称为过滤器：
                all()  返回查询集中的所有数据
                filter()：返回符合条件的数据
                    filter(键=值,键=值)
                    filter(键=值).filter(键=值)
                exclude()  过滤掉符合条件的数据，返回不符合条件的
                order_by()  排序
                values()  一条数据是一个字典，返回一个包含字典的列表
            返回单个数据：
                get()  返回一个满足条件的对象
                    注意：如果没有找到符合条件的对象，会引发模型类.DoesNotExist异常；
                          如果找到多个对象，会引发模型类.MultipleObjectsReturned异常
                count()  返回当前查询集中的对象个数
                first()  返回查询集中的第一个对象
                last()  返回查询集中的最后一个对象
                exist()  判断查询集中是否有数据，有则返回True
            限制查询集：
                查询集返回列表，可以使用下标的方法进行限制，等同于sql中的limit
                注意：下标不能是负数
            查询集的缓存：
                概述：每个查询集都包含一个缓存，以减少对数据库的访问
                      在新建的查询集中，缓存首次为空，第一次对查询集求值，会发生数据缓存，
                      django会将查询出来的数据做一个缓存，以后的查询会直接访问查询集的缓存
            字段查询：
                概述：
                    实现了sql中的where语句，作为方法filter(),exclude(),get()的参数
                    语法：属性名称__比较运算符=值
                    外键：属性名_id
                    转义：类似sql中的like语句，
                          like语句中使用%是为了匹配占位，匹配数据中的%（where like \%）


                比较运算符：
                    exact--判断，区分大小写
                    contains--是否包含，区分大小写
                    startswith、endswith--以value开头或结尾，区分大小写
                    以上若在前面加i，就不再区分大小写
                    isnull、isnotnull--是否为空
                    in--是否包含在范围内
                    gt、gte、lt、ltre--大于、大于等于、小于、小于等于
                    year、month、day、week_day、hour、minute、second--时间
                    跨关联查询：
                        处理join查询：语法---模型类名__属性名__比较运算符

                    查询快捷：pk==主键
                聚合函数：
                    使用aggregate()返回聚合函数的值
                    需要引入：from django.db.models import Avg, ...
                    Avg
                    Count
                    Max
                    Min
                    Sum
                F对象：
                    可以使用模型的A属性与B属性进行比较（找出女生数大于男生数的班级）
                    支持F对象的算术运算
                Q对象：
                    概述：过滤器的方法中的关键字参数，条件为And模式
                    需求：进行or查询
                    解决：使用Q对象
                    注意：只有一个Q对象时，用于匹配
                    Q对象前面加～表示取反

##视图
	概述：
	    作用：接收web请求，并响应web请求
		本质：python函数
		响应内容：
		    网页：
		        重定向
		        错误视图：404、500、400
		    json数据
		过程：

	url配置：
	    配置流程：制定根级url配置文件（settints.py-ROOT_URLCONF）
	        urlaptterns： 一个url实例对象的列表
	            参数：正则、视图名称、名称
	            url匹配正则的注意事项：
	                如果想要从url中获取一个值，需要对正则加小括号
	                匹配正则前方不需要加反斜杠
	                正则前需要加r，表示字符串不转义
		引入其他url配置
		    在应用中创建urls.py文件，定义本应用的url配置，在工程urls.py中使用include方法
		        url(r'^', include('myapp.urls'))
		    匹配过程

		url反向解析
		    概述：如果在视图、模板中使用了硬编码的链接，在url配置发生改变时，动态生成链接的地址	
		    解决：在使用链接时，通过url配置的名称动态生成url地址
		    作用：使用url模板
	视图函数：
	定义视图：本质是一个函数
		参数:
			request  一个Httprequest的实例对象
			通过正则获取的参数
		位置：一般在views.py中
		错误视图：
			404  找不到网页时返回的（url匹配不成功）
				 可以自定义：在templates目录下定义404.html
				 配置settings.py：
				 	DEBUG 为True永远不会调用404.html
				 	ALLOWED_HOSTS=['*'] 允许访问
			500  在视图代码中出现错误（服务器内部）
			400  错误出现在客户的操作
	HttpRequest对象：
		概述：服务器接收http请求后，会根据报文创建HttpRequest对象
			 视图的第一个参数就是HttpRequest对象
			 Django创建的，之后调用时传递给视图
		属性：path 请求的完整路径（不包括域名和端口）
			 method 请求的方式，GET\POST
			 encoding 浏览器提交数据的编码方式，一般为utf-8
			 GET 类似字典的对象，包含get请求的所有参数
			 	获取浏览器传递给服务器的数据
				 	requst.GET.get
				 	requst.GET.getlist
			 POST 类似字典的对象，包含post请求的所有参数
			 	使用表单提交实现post请求
				 	request.POST.get
				 	request.POST.getlist
			 	关闭csrf
			 FILES 类似字典的对象，包含所有上传的文件
			 COOKIES 字典，包含所有cookie
			 session 类似字典的对象，表示当前会话
		方法：is_ajax() 如果是通过XMLHttpRequest发起的，返回True
		QueryDict对象：request对象中的GET\POST都属于QueryDict对象
			方法：get() 根据键获取值（单值）
				 getlist() 将键的值以列表的形式返回（多个值）
	HttpResponse对象：
		概述：
			作用：给浏览器返回数据
			HttpRequest对象是由Django创建的，HttpResponse对象是由程序员创建的
		返回用法：
			不调用模板，直接返回数据：return HttpResponse('')
			调用模板：
				使用render()方法：render(request, templateName[context])
					作用：结合数据和模板，返回完整的HTML页面
					参数：request 请求体对象
						 templateName 模板路径
						 context 传递给需要渲染的
		属性：
			content：表示返回的内容
			charset：编码格式
			status_code：响应的状态码------200、304、404
			content-type：指定输出的MIME类型
		方法：
			init：使页面内容实例化HttpResponse对象
			write(content)：以文件的形式写入
			flush()：以文件的形式输出缓冲区
			set_cookie(key, value='', max_age=None, exprise=None)：
			delete_cookie(key)：删除cookie，若不存在，无影响
		子类HttpResponseRedirect：
			功能：重定向，服务器端的跳转
			简写：redirect(src) 重定向到src
				src推荐使用反向解析
		子类JsonResponse：
			返回json数据，一般用于异步请求
			__init__(self.date)---date 字典对象
				注意：content-type类型为application/json
	状态保持：
		概述：
			http协议是无状态的，每次请求都是一次新的请求
			客户端与服务器的一次通信就是一次会话
			实现状态保持，在客户端或者福区段存储有关会话的数据
			存储方式：
				cookie：所有的数据都存在客户端，不要存储敏感的数据
				session：所有的数据存储在服务端，在客户端用cookie存储session_id
			目的：在一段时间内跟踪请求者的状态，可以实现跨页面访问当前的请求者的数据
			注意：不同的请求者之间不会共享数据，与请求者一一对应
		启用session：
			settings.py中INSTALLED_APPS默认启用
						 MIDDLEWARE默认启用
		使用session：
			启用session后，每个HttpRequest对象都有一个session属性，是一个类似字典的对象
			get(key,default=None)：获取session值
			clear()：清空所有会话  request.session.clear()
			flush()：删除当前的会话并删除会话的cookie  request.session.flush()
			推荐使用：logout(request)
			设置过期时间：set_expiry(value)  单位是秒  默认时间为两个星期
						可以制定具体时间  
						0表示关闭浏览器时就失效
						None表示永久存储
			存储session的位置：
				数据库：默认位置
				缓存：只存储在本地内存中，如果丢失不能找回，比数据库快
				数据库和缓存：优先从本地缓存中读取，没有再从数据库获取
			使用Redis缓存session：
				pip install django-redis-sessions

##模板：
	定义模板：
		变量：视图传递给模板的数据
			 要遵守标识符规则
			 语法：{{var}}
			 注意：如果使用的变量不存在，则插入的是空字符串
			 在模板中使用.语法  首先当做字典 其次属性或方法 最后数字索引
			 在模板中调用对象的方法  不能传递参数
		标签：
			语法：{% tag %}
			作用：在输出中创建文本，控制逻辑、循环
			if：
				格式 {% if 表达式 %}		
						语句
					{% endif %}
			for：
				格式 {% for 变量 in 列表 %}
						语句--{{ forloop.counter }}  显示循环到第几次
					{% empty %}
						语句    		列表为空或不存在时执行
					{% endfor %}
						
			comment：注释多行
				格式：{% comment %}
					 	注释的内容
					 {% endcomment %}
			ifequel/ifnotequel：判断是否相等或者不相等
				格式：{% ifequel 值1 值2 %}
					 	语句		如果值1等于值2则执行语句
					 {% endifequel %}
			include：加载模板并以标签内的参数渲染
				格式：{% include '模板目录' 参数1 参数2 %}
			url：方向解析
				格式：{% url'namespace:name' p1 p2 %}
			scrf_token：用于跨站请求伪造保护
				格式：{% csrf_token %}
			block/extends：模板继承
			autoescape：HTML转义
		过滤器：
			语法：{{var|过滤器}}
			作用：在变量显示前修改显示效果，不会改变变量的值
			lower
			upper
			可以传递参数，用引号引起来
				join：列表|join:'#'	用#连接列表的元素
			如果一个变量不存在或者值为false、空，可以使用默认值
				default：{{var|default:''}}
			根据给定格式转换日期为字符串
				date：{{date|date:'y-m-d'}}
			HTML转义
				escape：
			加减乘除
				{{num|add:需要加减的数字}}
				{% widthratio num 1 5 %}	num乘以5
				{% widthratio num 5 1 %}	num除以5
		注释：
			单行注释：{# 注释内容 #}
	反向解析：

	模板继承：
		作用：可以减少页面内容的重复定义，实现页面的重用
		block标签：在父模板中预留区域，子模板去填充
			{% block 标签名 %}
				预留区
			{% endblock 标签名%}
		extends标签：继承模板，需要写在模板文件的第一行
			{% extends '父模板路径' %}
			{% block main %}
				填充
			{% endblock main %}
	HTML转义：
		{{code|escape}}
		{{code|safe}}
		{% autoescape off %}
			{{code}}
		{% endautoescape %}
	CSRF：跨站请求伪造  	
		某些恶意的网站包含链接、表单、按钮、js、利用登陆的用户在浏览器中认证，从而攻击服务
		防止CSRF：
			settings.py中MIDDLEWARE增加
			表单中添加{% csrf_token %}
	验证码：
		作用：在用户注册、登录页面的时候使用，为了防止暴力请求，减轻服务器压力，还是防止CSRF
			的一种方式
##高级扩展：
	静态文件：css、js、图片、json文件、字体文件等
		project目录下创建static目录，用来存放静态文件
			static目录下创建对应项目的文件目录
				对应项目的文件目录下一般包括css、image、js等
		配置settings.py：
			STATIC_URL='/static/'
			STATICFILES_DIRS=[
				os.path.join(BASE_DIR,'static')
			]
	中间件：
		概述：一个轻量级、底层的插件，可以介入Django的请求和响应
		本质：一个python类
		方法：
			__init__：
				不需要传参，服务器响应第一个请求的时候自动调用，用于确定是否启用该中间件
			process_request(self, request)：
				在执行视图之前被调用（分配url匹配视图之前），每个请求上都会调用，返回None或者HttpReqsponse对象
			process_view(self, request, view_args, view_kwargs)：
				调用视图之前执行，每个请求上都会调用，返回None或者HttpReqsponse对象
			process_template_response(self, request, response)：
				在视图刚好完调用，每个请求上都会调用，返回None或者HttpReqsponse对象
				使用render
			process_response(self, request, response)：
				所有响应返回浏览器之前调用，每个请求上都会调用，返回HttpReqsponse对象
			process_exception(self, request,exception)：
				当视图抛出异常时调用，返回HttpReqsponse对象
		执行位置：

		自定义中间件：
			工程目录下创建middleware/myapp/python文件，文件中定义中间件
				from django.utils.description import MiddleWareMixin
				class MyMiddle(MiddleWareMixin):
					...
		使用中间件：
			在settings.py中添加
		上传图片：
			概述：文件上传时，文件数据存储在request.FILES属性中
				 注意：form表单要上传文件需要加entype='multipart/form-data'
			存储路径：
				在static目录下创建upfile目录用于存储接收上传的文件
			上传文件路径：settings.py中配置
				MDEIA_ROOT=os.path.join(BASE_DIR,r'static/upfile')
