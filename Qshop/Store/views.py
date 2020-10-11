from django.shortcuts import render_to_response,HttpResponse
from .forms import RegisterUser
from .forms import PersonForm
from django.shortcuts import render
from .models import *
#json与ajax测试，返回一个json格式的用户信息
from django.http import JsonResponse
#CBV class base views  基于类的视图，类视图
from django.views import View
#导入聚合模块
from django.db.models import Sum, Avg, Count, Min, Max

#导入重定向
from django.http import HttpResponseRedirect
#导入时间模块
import datetime

#密码加密
import hashlib
def SetPassword(pwd):
    md5=hashlib.md5()   #实例化一个md5对象
    md5.update(pwd.encode())  #将传入的密码进行编码
    result = md5.hexdigest()   #使用hexdigest方法进行hash加密
    return result

#登录装饰器
def LoginValid(func):
    def inner(request,*args,**kwargs):
        cooki_username=request.COOKIES.get("name")
        session_name=request.session.get('name')
        #如果cookie和session存在
        if cooki_username and session_name:

            #针对中文账号登陆问题
            # cooki_username=cooki_username.encode('ISO-8859-1').decode('utf-8')
            #查询判断是否匹配登录角色，判断用户名，用户类型
            flag=QUser.objects.filter(
                username=cooki_username,
                usertype=1
            ).exists()
            if flag:
                return func(request,*args,**kwargs)

        return HttpResponseRedirect('/store/login')
    return inner

#登录界面
from .forms import UserLogin
def login(request):
    if request.method=='POST':
        # print(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        # 校验数据
        # if username and password:
        userlogin=UserLogin(request.POST)
        if userlogin.is_valid():  #通过校验
            #判断用户名，密码，账号，用户类型是否符合
            flag = QUser.objects.filter(
                username=username, password=SetPassword(password),usertype=1).exists()
            user_id=QUser.objects.filter(username=username).first().id
            if flag:
                # 存在
                # 用户存在
                response = HttpResponseRedirect("/store/index")  # 校验成功重定向到index界面
                # cookie与session设置要依赖于响应对象
                # 设置cookie
                # username=bytes(username,'utf-8').decode('ISO-8859-1')  #解决中文账号名登陆问题
                response.set_cookie("name",username,expires=259200)
                response.set_cookie("user_id",user_id,expires=259200)

                # 设置session
                request.session["name"]=username

                # # 下发picture路径的cookie
                # userinfo = QUser.objects.filter(username=username).first()
                # if userinfo.picture:
                #     response.set_cookie("picture", userinfo.picture,expires=259200)
                return response
            else:
                message="账号密码错误"
        else:
            message = userlogin.errors

    return render(request,"store/login.html",locals())

#登出界面
def logout(request):
    # return redirect("/login")
    ##删除cookie和session
    response=HttpResponseRedirect("/store/login/")

    #删除cookie，就是重新下发一个空值覆盖掉之前的cookies
    response.delete_cookie("name")
    response.delete_cookie("user_id")
    # 删除session
    del request.session['name']

    return response


#注册界面
def register(request):
    if request.method == 'POST':
        # print(request.POST)
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        repassword=request.POST.get("repassword")
        #判断验证码是否一致
        write_captcha=request.POST.get("captcha")
        captcha=request.session['code']

        #进行账号判断
        # 校验密码是否一致
        if username and password and repassword and password == repassword\
                and captcha==write_captcha:
            # 后端校验账号是否存在
            registeruser=RegisterUser(request.POST)  #实例化对象

            #进行数据校验,数据通过
            if registeruser.is_valid():
                # 保存数据
                QUser.objects.create(
                    username=username,
                    email=email,
                    password=SetPassword(password),  #对注册的密码进行hash加密
                    usertype=1
                )
                # 重定向
                return HttpResponseRedirect("/store/login/")
            else:
                message = registeruser.errors

        elif not username:
            message = "请输入账号名"
        elif not password:
            message = "请输入密码，密码不能为空"
        elif password != repassword:
            message= "两次输入的密码不一致"
        elif captcha != write_captcha:
            message= "验证码输入不正确"

    return render(request,"store/register.html",locals())

#首页
@LoginValid
def index(request):


    return render_to_response("store/index.html",locals())

@LoginValid
#添加商品页面
def add_goods(request):
    """
    商品添加页面，进行post请求提交添加商品的信息
    :param request:请求页面 store/add_goods.html
    :return:判定可提交之后重定向到当前页面
    """
    goodstype_list=GoodsType.objects.all()
    if request.method=="POST":
        print(request.POST)

        goods_name=request.POST.get('goods_name')

        #商品类型
        goods_type=request.POST.get('goods_type')
        goods_type_id=GoodsType.objects.filter(t_name=goods_type).first().id
        # print(goods_type_id)  #拿到goods_type的id

        g_price=request.POST.get('g_price')
        g_safe_date=request.POST.get('g_safe_date')
        g_public_date=request.POST.get('g_public_date')
        #商品数量
        goods_num=request.POST.get('goods_num')

        g_description=request.POST.get('g_description')
        g_picture=request.FILES.get('g_picture')

        #添加数据
        goods=Goods()
        goods.g_name=goods_name
        goods.g_type_id=goods_type_id
        goods.g_safe_date=g_safe_date
        goods.g_public_date=g_public_date
        goods.g_num=goods_num
        goods.g_description=g_description
        goods.g_price=g_price

        #图片添加
        goods.g_picture=g_picture

        #g_number字段必填，设置为自增
        goods.g_number=1

        #店铺id关联
        cookie_name=request.COOKIES.get('name')
        #反向查询拿到store的对象
        quser_store=QUser.objects.filter(username=cookie_name).first().store
        goods.g_store_id=quser_store.id

        goods.save()


    return render(request,"store/add_goods.html",locals())

#api接口拿商品数据，使用drf-djangorestframerwork
#从http://127.0.0.1:8000/store/api/morelist/?type_id=1接口拿数据
#serializer数据在Store应用中

@LoginValid
def orders(request):

    return render_to_response("store/orders.html",locals())

@LoginValid
def count_goods(request):

    return render_to_response("store/count_goods.html",locals())


#编写首页echarts的api接口
def echarts_api():
    result={
       "data":[]
    }
    goods_list=Goods.objects.all()


    return result

@LoginValid
def count_orders(request):

    return render_to_response("store/count_orders.html",locals())

#店铺管理
@LoginValid
def store(request):
    username=request.COOKIES.get("name")

    if request.method=='POST':
        user_storeinfo = QUser.objects.filter(username=username).first().store
        # print(request.POST)
        s_name=request.POST.get('s_name')
        s_address=request.POST.get('s_address')
        s_description=request.POST.get('s_description')
        s_logo=request.FILES.get('s_logo')


        user_storeinfo.s_address=s_address
        user_storeinfo.s_description=s_description
        if s_logo:  #判断是否上传了图片
            user_storeinfo.s_logo=s_logo

        #进行店铺名修改时间校验
        data_now = datetime.datetime.now()
        # data=data.timestamp()
        # print(data_now)
        #判断是否存在datetime类型的数据
        #存在，进行时间差判断
        if user_storeinfo.s_changed_datetime:
            data_old=user_storeinfo.s_changed_datetime  #获取数据库的更新名称时间
            time_diff=data_now-data_old   #当前时间与数据库时间的时间差
            int_secondes_time_diff=int(time_diff.total_seconds())

            #30天---2592000秒
            # print(int_secondes_time_diff)
            #时间差超过30天的秒数，进行店铺名更新和时间值更新
            if int_secondes_time_diff>2592000:
                #修改店铺名并更新时间
                user_storeinfo.s_name = s_name
                user_storeinfo.s_changed_datetime=data_now

        #不存在datetime表示第一次修改，直接修改名称并且写入时间
        else:
            #修改店铺名并更新时间值
            user_storeinfo.s_name = s_name
            user_storeinfo.s_changed_datetime = data_now

        user_storeinfo.save()

    if username:
        user_store_info = QUser.objects.filter(username=username).first().store

        #拿到店铺名称写入时间的时间戳
        change_datetime=int(user_store_info.s_changed_datetime.timestamp())
        # print(change_datetime)

    return render(request,"store/store.html",locals())



#个人中心页面
@LoginValid
def userinfo(request):
    u_name=request.COOKIES.get('name')
    userinfo=QUser.objects.filter(username=u_name).first()

    if request.method=='POST':

        #进行后端校验
        personform=PersonForm(request.POST)
        if personform.is_valid():  #进行数据校验
            #True代表通过
            # print('success')
            #处理数据，获取通过校验器之后的数据
            data=personform.cleaned_data
            # print(data)
            #处理，保存数据
            userinfo.nickname = data.get("nick_name")

            gender = int(request.POST.get('gender'))
            userinfo.gender = gender

            userinfo.phone = data.get("phone")
            userinfo.email = data.get("email")
            userinfo.address = data.get("address")

            picture = request.FILES.get('picture')
            response = HttpResponseRedirect("/store/userinfo")
            # 图片存在判断
            if picture:
                userinfo.picture = picture
            userinfo.save()
            return response
        else:
            #False 代表校验失败
            print('error')
            errors=personform.errors
            print(errors)

    return render(request,"store/userinfo.html",locals())

#后台用户头像
class UserinfoView(View):
    def get(self,request):
        result={
            "img":""
        }

        username=request.session.get('name')
        quser=QUser.objects.filter(username=username).first()
        img=quser.picture  #拿到用户图片
        result["img"]=str(img)

        #抛出result
        return JsonResponse(result)


#类视图获取后台商品数量统计echarts的数据
class GoodsView(View):
    def __init__(self):
        self.result = {
            "code": "200",
            "msg": "success",
            "data": [],
            "methods": "get"
        }
    # 处理 get 请求，获取不同类型商品的总量
    def get(self,request):
        self.result["methods"] = "get"
        user_id = request.COOKIES.get("user_id")

        # 处理有id，拿到店铺id
        store_id = Store.objects.filter(s_user_id=user_id).first().id
        # 拿到店铺内对应的商品
        # goods_list=Goods.objects.filter(g_store_id=store_id).all()
        goods_list=Goods.objects.filter(g_store_id=store_id).values("g_type_id").annotate(Sum("g_num"))

        for one in goods_list:
            goodstype=GoodsType.objects.filter(id=one['g_type_id']).first()
            self.result["data"].append(
                {"type":goodstype.t_name,"num":one['g_num__sum']}
            )


        return JsonResponse(self.result)


#验证码视图
from Store.polls.util import *
from Store.polls.captcha import *

def captcha(request):

    code_text = gen_verify_code() # 随机生成4位数字
    request.session['code'] = code_text # 在服务器中以session形式保存
    image_data = Captcha.instance().generate(code_text)

    # print(image_data)
    # print(request.session['code'])
    # print(code_text)
    return HttpResponse(image_data, content_type='image/png') # 返回图片对象