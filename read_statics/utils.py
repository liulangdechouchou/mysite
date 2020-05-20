import datetime
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum, ReadDetail
from django.utils import timezone
from django.db.models import Sum

def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):
        # 每次打开博客，urls.py接收到了请求，再检查cookie中是否有我们设置的cookies
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        # if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
        #     # 存在记录
        #     # readnum = ReadNum.objects.get(blog = blog)
        #     readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        # else:
        #     # 不存在记录
        #     # 先示例化，再对示例中的字段赋值(直接.+字段名)
        #     readnum = ReadNum(content_type=ct, object_id=obj.pk)
        #     # 计数+1
        readnum.read_num += 1
        readnum.save()

    date = timezone.now().date()
    readDetail,_= ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.id, date=date)
    # if ReadDetail.objects.filter(content_type=ct, object_id=obj.id, date=date).count():
    #     readDetail = ReadDetail.objects.get(content_type=ct, object_id=obj.id, date=date)
    # else:
    #     readDetail = ReadDetail(content_type=ct, object_id=obj.id, date=date)
    readDetail.read_num += 1
    readDetail.save()
    return key


def get_seven_days_read_data(content_type):
    # timezone.now()是datetime的数据类型
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type,date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums


def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    # 取前七篇
    return read_details[:7]


def get_yeseterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday)\
                             .order_by('-read_num')
    return read_details[:7]


def get_last_week_hot_data(content_type):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    read_details = ReadDetail.objects.filter(content_type=content_type, date__lt=today, date__gt=date) \
                             .annotate(read_num_sum=Sum('read_num')) \
                             .order_by('-read_num_sum')
    return read_details[:7]