from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

# Create your models here.

class Category(models.Model):
    """文章分类"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """文章标签"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    """文章数据库表"""
    # 标题
    title = models.CharField(max_length=70)
    # 正文
    body = models.TextField()
    # 创建时间
    created_time = models.DateTimeField()
    # 最新修改时间
    modified_time = models.DateTimeField()
    # 文章摘要，第二个属性设置意为可以不写摘要
    excerpt = models.CharField(max_length=200, blank=True)
    # 定义文章分类一对多关系
    category = models.ForeignKey(Category)
    # 定义文章与标签多对多关系
    tags = models.ManyToManyField(Tag, blank=True)
    # 文章作者
    author = models.ForeignKey(User)
    # 记录阅读量
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time']

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        # 若没有写摘要
        if not self.excerpt:
            # 首先实例化一个markdown类，用于渲染body文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将markdown文本渲染成HTML文本，用strip_tags去掉HTML标签，然后提取前60个字符
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        # 调用父类的save方法将数据保存
        super(Post, self).save(*args, **kwargs)
