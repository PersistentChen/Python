from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm

# Create your views here.

def post_comment(request, post_pk):
    # 首先获取要评论的文章
    post = get_object_or_404(Post, pk=post_pk)

    # 只有请求方式为post时才需要处理表单数据
    if request.method == 'POST':
        # 用户提交的数据存在request.POST中，这是一个类字典对象
        form = CommentForm(request.POST)
        # 检查表单数据是否符合格式要求
        if form.is_valid():
            # 若符合要求，用save方法保存
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment = form.save(commit=False)
            # 将评论和文章关联起来
            comment.post = post
            # 最终将评论保存进数据库
            comment.save()
            # 重定向到post详情页，redirect会调用模型实例的get_absolute_url进行重定向
            return redirect(post)
        else:
            # 不符合要求，重新渲染详情页并显示表单的错误
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'commen_list': comment_list,
            }
            return render(request, 'blog/index.html', context=context)
    # 不是post请求，重定向到文章详情页
    return redirect(post)