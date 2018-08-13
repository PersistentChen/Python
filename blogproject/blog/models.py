from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time']
