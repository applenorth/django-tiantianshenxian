from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from .models import StoreUser
def add_info(request):
    # storeuser = StoreUser()
    # storeuser.username = "admin"
    # storeuser.password = "1111"
    # storeuser.nick_name = "管理员"
    # storeuser.save()
    data = StoreUser.objects.create(
        username="李嗨涛",
        password="11111",
        nick_name="李九一")
    print(data)
    return HttpResponse('add_success')

#查找
def select_info(request):
    data=StoreUser.objects.filter(gender=1)
    # print("filter方法的结果：{}".format(data))
    # print("all方法的结果：{}".format(data.all()))
    # print("first方法的结果：{}".format(data.first()))
    # print("first方法后使用属性的结果：{}".format(data.first().username))
    #
    # print(data.values)
    # data1=data.values()
    # print(data1)
    #
    # for keys in data1:
    #     print(keys)
    print(data.values_list())
    #
    for j in data.values_list():
        print(j)
    #聚合查询，得到的是一个字典，可以修改key的值
    # from django.db.models import Max,Min,Count,Avg,Sum
    # data= StoreUser.objects.all()
    #
    # data=StoreUser.objects.aggregate(Avg('id'),Sum('age'))
    # print(data)

    # #F对象
    # from django.db.models import F
    # #F对象，比较同一个模型中两个字段的值
    # data=StoreUser.objects.filter(age__gt=F("id")).all()
    # print(data)
    #
    # #Q对象，逻辑关系，and，or，not
    # #and-且，在filter后面，有多个条件，使用&
    # #or   使用 |
    # #not   使用 ~
    # from django.db.models import Q
    # data=StoreUser.objects.filter(~Q(gender=0))
    # print(data)
    return HttpResponse('select_success')