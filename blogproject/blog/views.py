import markdown
from markdown.extensions.toc import TocExtension
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from django.db.models import Q

from .models import Post, Category, Tag

from comments.forms import CommentForm


# Create your views here.

class IndexView(ListView):
    # 表明要获取的模板是Post
    model = Post
    # 指定这个视图渲染的模板
    template_name = 'blog/index.html'
    # 指定获取的模型列表数据保存的变量名
    context_object_name = 'post_list'
    # 指定paginate_by属性后开启分页功能
    paginate_by = 3

    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过render函数的context参数传递一个字典实现的
        这里传递一个{'post_list': post_list}字典给模板
        在类视图中，这个需要传递的模板变量字典是通过get_context_data 获得的
        所以覆写该方法，以便插入自定义模板变量
        """
        # 首先获得父类生成的传递给模板的字典
        context = super().get_context_data(**kwargs)
        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        # 调用自己写的pagination_data方法获得显示分页导航条需要的数据
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        # 将分页导航条的模板变量更新到context中，注意pagination_data返回的也是一个字典
        context.update(pagination_data)
        # 将更新后的context返回，此时context字典中已有显示分页导航所需的数据
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 若没有分页，就无须显示导航条，返回空字典
            return {}
        # 当前页左边连续的页码号，初始值为空
        left = []
        # 当前页右边连续的页码号，初始值为空
        right = []
        # 标识第一页页码后是否需要显示省略号
        left_has_more = False
        # 标识最后一页页码后是否需要显示省略号
        right_has_more = False
        # 标识是否需要显示第一页的页码号
        # 若当前页面左边的连续页号码中含有第一页的号码，就不需要再显示第一页
        # 其他情况下第一页号码是要始终现实的
        first = False
        # 最后一页是否显示原理同上
        last = False
        # 获得用户请求的页码
        page_number = page.number
        # 获得分页后的总页数
        total_pages = paginator.num_pages
        # 获得整个分页页码列表
        page_range = paginator.page_range
        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]
            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True
            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True
            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]
            # 是否需要显示第一页和第一页后的省略号
            if left[0] > 2:
                right_has_more = True
            if left[0] > 1:
                first = True
            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return data


# request参数是Django封装好的http请求
# def index(request):
#     post_list = Post.objects.all()
#     return render(request, 'blog/index.html', context={
#         'post_list': post_list,
# #     })

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        """
        覆写get方法是因为文章每被访问一次，阅读量+1
        get返回一个HttpResponse实例
        只有调用get方法之后，才有self.object属性
        """
        response = super(PostDetailView, self).get(request, *args, *kwargs)
        # 将文章阅读量+1
        self.object.increase_views()
        # 视图必须返回一个HttpResponse对象
        return response

    def get_object(self, queryset=None):
        # 覆写get_object方法是为了对post的body值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        # post.body = markdown.markdown(post.body,
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        # 覆写get_context_data方法是为了将post传递给模板外（DetailView 已经帮我们完成）
        # 还要把评论表单、post下的评论列表传递给模板
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.increase_views()
#     post.body = markdown.markdown(post.body,
#                                   extensions=[
#                                       'markdown.extensions.extra',
#                                       'markdown.extensions.codehilite',
#                                       'markdown.extensions.toc',
#                                   ])
#     form = CommentForm()
#     # 获取这篇post下的全部评论
#     comment_list = post.comment_set.all()
#
#     # 将文章、表单以及文章下的评论作为模板变量传给detail.html模板
#     context = {'post': post,
#                'form': form,
#                'comment_list': comment_list,
#     }
#     return render(request, 'blog/detail.html', context=context)

class ArchivesView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month)


# def archives(request, year, month):
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month)
#     return render(request, 'blog/index.html', context={'post_list': post_list})

class CategoryView(IndexView):
    # model = Post
    # template_name = 'blog/index.html'
    # context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     # post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     post_list = Post.objects.filter(category=cate)
#     return render(request, 'blog/index.html', context={'post_list': post_list})

class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = '请输入关键字'
        return render(request, 'blog/index.html', {'error_msg': error_msg})
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})
