from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from Store.models import *
from Buyer.models import OrderInfo,PlaceOrder
#json与ajax测试，返回一个json格式的用户信息
from django.http import JsonResponse
# Create your views here.


#密码加密
from Store.views import SetPassword

#登录装饰器
def LoginValid(func):
    def inner(request,*args,**kwargs):
        """
        获取cookie和session的信息:
            cookie:b_name，b_user_id
            session:b_user_id
        """
        cookie_username=request.COOKIES.get("b_name")
        cookie_userid=request.COOKIES.get("b_user_id")
        session_id=request.session.get('b_id')

        #如果cookie和session存在
        if cookie_userid and session_id:

            #针对中文账号登陆问题
            # cooki_username=cooki_username.encode('ISO-8859-1').decode('utf-8')
            """
            查询匹配内容：
                username：用户名
                id：用户id
                usertype：用户类型
            """
            flag=QUser.objects.filter(
                username=cookie_username,
                id=session_id,
                usertype=0
            ).exists()
            if flag:
                return func(request,*args,**kwargs)

        return HttpResponseRedirect('/buyer/login')
    return inner


#注册，用户注册，与后台的用户同用一张用户表
def register(request):
    if request.method=='POST':
        user_name=request.POST.get("user_name")
        user_pwd=request.POST.get("user_pwd")
        user_cpwd=request.POST.get("user_cpwd")
        user_email=request.POST.get("user_email")
        user_allow=request.POST.get("user_allow")

        #判断用户名是否存在，密码是否一致并符合要求，用户协议是否同意
        flag=QUser.objects.filter(username=user_name).exists()
        if not flag:
            if user_pwd==user_cpwd and user_allow=="on":
                QUser.objects.create(
                    username=user_name,
                    password=SetPassword(user_pwd),
                    email=user_email

                )
                return HttpResponseRedirect('/buyer/login')
            else:
                print('校验没通过')
        else:
            print("用户名存在")

    return render(request,'buyer/register.html',locals())


#登录，购物用户登录
def login(request):

    if request.method=='POST':
        user_name=request.POST.get('user_name')
        user_pwd=request.POST.get('user_pwd')

        flag = QUser.objects.filter(
            username=user_name, password=SetPassword(user_pwd), usertype=0).exists()
        user_id = QUser.objects.filter(username=user_name).first().id
        if flag:

            # 校验成功重定向到index界面
            response = HttpResponseRedirect("/buyer/index")

            """
            下发cookie和session:
                cookie:name，user_id
                session:user_id
            """
            response.set_cookie("b_name", user_name, expires=259200)
            response.set_cookie("b_user_id", user_id, expires=259200)
            request.session["b_id"] = user_id

            return response
        else:
            print("账号密码不正确")



    return render(request,'buyer/login.html',locals())


#登出视图
def logout(request):
    # 删除
    resp = HttpResponseRedirect("/buyer/index/")
    resp.delete_cookie("b_name")
    resp.delete_cookie("b_user_id")
    del request.session["b_id"]
    return resp

#缓存
from django.views.decorators.cache import cache_page
#首页
# @cache_page(3*60)    #设置3分钟的缓存
def index(request):

    goods_list_bh3=Goods.objects.filter(g_type_id=5).all()[:5]   #goods为崩坏系列

    goods_list_sq=Goods.objects.filter(g_type_id=4).all()[:5]   #goods为少前系列

    goods_list_ark=Goods.objects.filter(g_type_id=1).all()[:5]    #明日方舟

    goods_list_gi=Goods.objects.filter(g_type_id=2).all()[:5]    #原神


    goods_list_azur=Goods.objects.filter(g_type_id=3).all()[:5]   #碧蓝航线

    goods_list_pcr=Goods.objects.filter(g_type_id=6).all()[:5]     #公主连结


    return render(request,'buyer/index.html',locals())

#购物车
@LoginValid
def cart(request):
    goods_id = request.GET.get("id")  # 商品id
    goods_count = request.GET.get("count")  # 商品数量
    userid = request.session.get("b_id")
    print(goods_id)
    print(goods_count)
    print(userid)
    return render(request,'buyer/cart.html',locals())


##修改购物地址
@LoginValid
def edit_address(request):

    return render(request,'buyer/edit-address.html',locals())

##修改用户信息
@LoginValid
def edit_user(request):

    return render(request,'buyer/edit-user.html',locals())


##我的订单
@LoginValid
def myorders(request):

    return render(request,'buyer/myorders.html',locals())

#detail界面立刻购买生成订单
import time
@LoginValid
def place_order(request):
    goods_id=request.GET.get("id")        #商品id
    goods_count=request.GET.get("count")  #商品数量
    userid=request.session.get("b_id")

    goods=Goods.objects.filter(id=int(goods_id)).first()
    #先生成placeorder的信息
    porder=PlaceOrder()
    porder.order_num = str(time.time()).replace(".","")    #用time.time作为订单编号
    porder.type_number =int(goods_count)
    porder.total_price =goods.g_price*int(goods_count)
    porder.user_id_id =userid
    porder.save()

    #再生成orderinfo的信息
    orderinfo=OrderInfo()
    orderinfo.goods_name = goods.g_name
    orderinfo.goods_price = goods.g_price
    orderinfo.goods_num = int(goods_count)
    orderinfo.goods_picture = goods.g_picture
    orderinfo.goods_total = goods.g_price*int(goods_count)
    orderinfo.goods_status = 0
    orderinfo.store = goods.g_store
    orderinfo.order = porder
    orderinfo.save()
    return render(request,"buyer/place_order.html",locals())

#用户中心个人信息
@LoginValid
def usercenterinfo(request):

    return render(request,'buyer/user-center-info.html',locals())


#list界面
@LoginValid
# @cache_page(3*60)    #设置3分钟的缓存
def list(request):

    # 新品推荐商品
    goods_new = Goods.objects.all()[::-1][:2]

    return render(request,'buyer/list.html',locals())

#detail界面，商品详细信息
@LoginValid
def detail(request,goods_id):
    # print(goods_id)  #119
    #传入商品的id
    goods_detail=Goods.objects.filter(id=goods_id).first()

    #新品推荐商品
    goods_new=Goods.objects.all()[::-1][:2]

    return render(request,'buyer/detail.html',locals())

