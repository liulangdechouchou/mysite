from django.shortcuts import render,redirect
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

# Create your views here.


def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    user = request.user
    # 数据检查
    if not user.is_authenticated:
        return render(request, 'error.html', {'message': '用户未登陆', 'redirect_to': referer})
    text = request.POST.get('text', '').strip()
    # 前端判断不可信
    if text == '':
        return render(request, 'error.html', {'message': '评论内容为空', 'redirect_to': referer})
    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except:
        return render(request, 'error.html', {'message': '评论对象不存在', 'redirect_to': referer})

    # 检查通过，保存数据
    comment = Comment()
    comment.user = user
    comment.text = text
    comment.content_object = model_obj
    comment.save()
    # 获取是哪个网页发来的评论请求，然后重定向到这个网页

    return redirect(referer)