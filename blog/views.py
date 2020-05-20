from django.shortcuts import render, get_object_or_404

from .models import Blog, BlogType
from read_statics.utils import read_statistics_once_read
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Count
# Create your views here.
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment


def get_blog_list_common_data(request, blogs_all_list):
    # 每5页进行分页
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)
    # request.GET 是一个字典 .get方法是查询键为'page'对应的值，若没有，则默认为1
    # 获取url的页面参数，GET请求（？的形式）
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    # 获取当前页码
    current_page_num = page_of_blogs.number
    # 获取总页数
    total_page_num = paginator.num_pages
    # 获取当前页码前后各两页的页码范围
    page_range = [x for x in range(current_page_num - 2, current_page_num + 3) if 0 < x <= paginator.num_pages]
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if total_page_num - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != total_page_num:
        page_range.append(total_page_num)

    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year = blog_date.year,
                                         created_time__month = blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    context = {}
    context['current_page_num'] = current_page_num
    context['total_page_num'] = total_page_num
    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['every_page_counts'] = page_of_blogs.object_list.count()
    context['blog_count'] = Blog.objects.all().count()
    # 这里看不懂可以看第16节
    context['blog_types'] = BlogType.objects.annotate(blog_count = Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return context


def blog_list(request):
    # 获取所有博客
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_id):
    context = {}
    blog = get_object_or_404(Blog, id=blog_id)
    read_cookie_key = read_statistics_once_read(request, blog)

    # ContentType再研究
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk)

    context['blog_types'] = BlogType.objects.all()
    # 筛选出上一篇博客
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    # 筛选出下一篇博客
    # 这里用[0]和first是一样的，filter获取到的是一个查询结果的列表
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()

    context['blog'] = blog
    context['comments'] = comments
    # 响应
    response = render(request, 'blog/blog_detail.html', context)
    # 阅读cookie标记
    response.set_cookie(read_cookie_key, 'true',)
    return response


def blog_with_type(request, blog_with_type):
    # id等价于pk，数据库中默认存在的一列
    blog_type = get_object_or_404(BlogType, id=blog_with_type)
    blogs_type_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_type_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blog_with_type.html', context)


def blog_with_date(request, year, month):
    blogs_type_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    # 每5页进行分页
    context = get_blog_list_common_data(request, blogs_type_list)
    context['blogs'] = blogs_type_list
    context['blog_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blog_with_date.html', context)

