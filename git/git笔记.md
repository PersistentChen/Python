####配置：
	用户名：git config --global user.name "PersistentChen"
	邮箱：git config --global user.email "178766869@qq.com"
####版本库：仓库，文件目录
	创建版本库：
		在合适地方创建一个目录，并cd进入该目录使用git init
		使用git init 命令使此目录成为Git管理的仓库
		注意：不能手动修改.git目录里面的文件
	把文件添加到版本库：
		在仓库目录创建...txt文件
		git add ...txt
		git commit -m "提交信息"
####命令：
	git status：查看仓库的当前状态		
	git diff：查看修改内容
	git log：查看提交日志
	
####版本回退：
	回退到上一版本：git reset --hard HEAD^
	回退到上上版本：git reset --hard HEAD^^
	回退到上100个版本：git reset --hard HEAD~100
	回退到具体版本：git reset --hard 具体版本号
	git relog：记录每一次命令
####工作区和版本库：
	git add ...：添加到工作区
	git commit ...：添加到版本库
	工作区：仓库所在目录
	版本库：.git目录
		暂存区（state）
		自动创建的一个分支（master）
		指向master的指针（HEAD）
	git checkout --fileName：
		如果fileName修改后还没有放到暂存区，现在撤销修改会回到和版本库一样的状态
		如果fileName文件已经添加到暂存区，又做了修改，撤销修改会回到添加到暂存区后的状态
		总之，就是让fileName回到最后一次git commit或者git add的状态
####远程仓库：
	创建SSH key：
		ssh-keygen -t rsa -C "178766869@qq.com"
		记录.ssh目录位置
		输入GitHub注册密码
		进入该目录.ssh
			id_rsa 私钥
			id_rsa.pub 公钥
	添加公钥：
		登录GitHub官网
		验证公钥：
			ssh -T git@github.com
	创建远程仓库：

	关联远程仓库：
		git remote add origin 远程仓库地址
	删除远程关联：
		git remote rm origin
	推送本地到远程：
		git push origin master 
		注意：需要先把远程仓库内容拉到本地，否则会出错
		忽略特殊文件：.gitignore
			需要忽略的文件名写入.gitignore
	拉取远程到本地：
		git pull origin master （--allow-unrelated-histories）
	从零开发：
		先有远程仓库
		从远程库克隆：
			git clone 远程库地址
		本地修改：
		git add
		git commit 
		git push origin master
####分支管理：
	master主分支：
	创建分支：git branch 分支名
	切换分支：git checkout 分支名
	创建与切换同时执行：git checkout -b 分支名
	查看分支：git branch   当前所在分支前会有*号