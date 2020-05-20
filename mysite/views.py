from django.shortcuts import render, redirect
from read_statics.utils import get_seven_days_read_data, get_today_hot_data,\
    get_yeseterday_hot_data, get_last_week_hot_data
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.core.cache import cache
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .forms import LoginForm
from django.contrib import auth


def home(request):
    """首页的视图"""
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    # 获取7天热门博客的缓存数据
    last_week_hot_data = cache.get('last_week_hot_data')
    if last_week_hot_data is None:
        last_week_hot_data = get_last_week_hot_data(blog_content_type)
        # 加入缓存，有效期1小时（3600s）
        cache.set('last_week_hot_data', last_week_hot_data, 3600)

    today_hot_data = get_today_hot_data(blog_content_type)
    yesterday_hot_data = get_yeseterday_hot_data(blog_content_type)
    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['last_week_hot_data'] = last_week_hot_data
    return render(request, 'home.html', context)


def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 经过验证
            user = LoginForm.cleaned_data['user']
            # 登录
            auth.login(request, user)
            # 登录后跳转到进入登录页面前的那个页面，如果没有获取到从哪个页面进来到，则默认跳转到首页home
            return redirect(request.GET.get('from', reverse('home')))

    else:
        login_form = LoginForm()
    context = {'login_form': login_form}
    return render(request, 'login.html', context)