from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from .models import *
#导入重定向
from django.http import HttpResponseRedirect
from .render_to_render_tempalte import *

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
            #查询判断是否匹配登录角色
            flag=QUser.objects.filter(
                username=cooki_username
            ).exists()
            if flag:
                return func(request,*args,**kwargs)

        return HttpResponseRedirect('/login')
    return inner

from .forms import UserLogin
def login(request):
    if request.method=='POST':
        # print(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        # 校验数据
        # if username and password:
        userlogin=UserLogin(request.POST)
        if userlogin.is_valid():  #通过校验
            flag = QUser.objects.filter(username=username, password=SetPassword(password)).exists()
            if flag:
                # 存在
                # 用户存在
                response = HttpResponseRedirect("/index")  # 校验成功重定向到index界面
                # cookie与session设置要依赖于响应对象
                # 设置cookie
                response.set_cookie("name",username,expires=259200)

                # 设置session
                request.session["name"]=username

                # 下发picture路径的cookie
                userinfo = QUser.objects.filter(username=username).first()
                if userinfo.picture:
                    response.set_cookie("picture", userinfo.picture,expires=259200)

                return response
            else:
                message="账号密码错误"
        else:
            message = userlogin.errors

    return render(request,"login.html",locals())

#登出界面
def logout(request):
    # return redirect("/login")
    ##删除cookie和session
    response=HttpResponseRedirect("/login")
    #删除cookie，就是重新下发一个空值覆盖掉之前的cookies
    response.delete_cookie("name")
    # 删除session
    del request.session['name']

    #删除picture的cookie
    response.delete_cookie("picture")
    return response


#注册界面
from .forms import RegisterUser
def register(request):
    if request.method == 'POST':
        # print(request.POST)
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        repassword=request.POST.get("repassword")

        #进行账号判断
        # 校验密码是否一致
        if username and password and repassword and password == repassword:
            # 后端校验账号是否存在
            registeruser=RegisterUser(request.POST)  #实例化对象

            #进行数据校验,数据通过
            if registeruser.is_valid():
                # 保存数据
                QUser.objects.create(
                    username=username,
                    email=email,
                    password=SetPassword(password)  #对注册的密码进行hash加密
                )
                # 重定向
                return HttpResponseRedirect("/login/")
            else:
                message = registeruser.errors

        elif not username:
            message = "请输入账号名"
        elif not password:
            message = "请输入密码，密码不能为空"
        elif password != repassword:
            message= "两次输入的密码不一致"

    return render(request,"register.html",locals())

@LoginValid
def index(request):


    return render_to_response("index.html",locals())

@LoginValid
def add_goods(request):

    return render_to_response("add_goods.html",locals())

@LoginValid
def orders(request):

    return render_to_response("orders.html",locals())

@LoginValid
def count_goods(request):

    return render_to_response("count_goods.html",locals())

@LoginValid
def count_orders(request):

    return render_to_response("count_orders.html",locals())

@LoginValid
def store(request):

    return render_to_response("store.html",locals())



#个人中心页面
from .forms import PersonForm
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
            print(data)
            #处理，保存数据
            userinfo.nickname = data.get("nick_name")

            gender = int(request.POST.get('gender'))
            userinfo.gender = gender

            userinfo.phone = data.get("phone")
            userinfo.email = data.get("email")
            userinfo.address = data.get("address")
            #图片存在判断
            picture = request.FILES.get('picture')
            response = HttpResponseRedirect("/userinfo")
            if picture:
                userinfo.picture = picture
                # 设置图片名字的cookie
                response.set_cookie("picture", picture)
            userinfo.save()
            return response
        else:
            #False 代表校验失败
            print('error')
            errors=personform.errors
            print(errors)

    return render(request,"userinfo.html",locals())

#json与ajax测试，返回一个json格式的用户信息
from django.http import JsonResponse
import json
def jsontest(request):
    result={
        "code":"10000",
        "msg":"成功",
        "data":[

        ]

    }
    goods_list=Goods.objects.all()[:12].values("g_name","g_price","g_picutre")
    print(goods_list)
    for one in goods_list:
        result["data"].append(
            {"g_name": one["g_name"], "g_price": one["g_price"], "g_picutre": one["g_picutre"]}
        )

    return JsonResponse(result)


def ajaxdemo(request):
    res = {
        "code": "10000",
        "msg": "成功",
        "data": {

        }
    }
    person=QUser.objects.get(id=1)
    res["data"] = {
        "username": person.username,
        "password": person.password,
        "nickname": person.nickname,
        "gender": person.gender
    }

    resp=JsonResponse(res)
    resp["Access-Control-Allow-Origin"]='*'
    return resp


def vuedemo(request):

    return render(request,'vuedemo.html',locals())


#添加数据
import random
def add_goods(request):
    ## 添加店铺
    store = Store.objects.create(s_name="生鲜店", s_logo="1.jpg", s_address="北京", s_description="北京生鲜店",
                                 s_user=QUser.objects.get(id=1))
    ## 添加类型
    goodstype = GoodsType.objects.create(t_name="生鲜", t_description="生鲜店",t_img="1.jpg")
    ## 增加100 条  
    goods_name = "芹菜、西芹、菠菜、香菜、茼蒿、茴香、生菜、苋菜、莴苣、葱、香葱、分葱、胡葱、楼子葱、蒜头、洋葱头、韭菜、韭葱、黄瓜、丝瓜、冬瓜、菜瓜、苦瓜、南瓜、栉瓜、西葫芦、葫芦、瓠瓜、节瓜、越瓜、笋瓜、佛手瓜"
    goods_name = goods_name.split("、")
    address = "北京市，天津市，上海市，重庆市，河北省，山西省，辽宁省，吉林省，黑龙江省，江苏省，浙江省，安徽省，福建省，江西省，山东省，河南省，湖北省，湖南省，广东省，海南省，四川省，贵州省，云南省，陕西省，甘肃省，青海省，台湾省"
    address = address.split("，")
    for n in range(10):
        for i, j in enumerate(range(10), 1):  ## i 是索引 代表下标从1开始
            goods = Goods()
            goods.g_number = str(i).zfill(5)  ## 返回指定长度的字符串   长度是5 
            goods.g_name = random.choice(address) + random.choice(goods_name)  ###从列表中随机取一个值  
            goods.g_price = round(random.random() * 100, 2)  ## 0到1 的小数  
            goods.g_num = random.randint(1, 100)
            goods.g_safe_date = random.randint(1, 12)
            goods.g_desription = "很好"
            goods.g_picutre = "images/goods.jpg"
            goods.g_type = goodstype
            goods.g_store = store
            goods.save()
    return HttpResponse("添加数据")


#启动list页面
def list(request):

    return render(request,'list.html',locals())


#函数视图
#FBV  function base views   基于函数的视图，函数视图
def funcdemo(request):
    #处理get请求
    if request.method=="GET":
        return JsonResponse({'method':'get'})

    # 处理post请求
    if request.method == "POST":
        return JsonResponse({'method': 'post'})

    # 处理put请求
    if request.method == "PUT":
        return JsonResponse({'method': 'put'})

    # 处理delete请求
    if request.method == "DELETE":
        return JsonResponse({'method': 'delete'})

#CBV class base views  基于类的视图，类视图
from django.views import View
class GoodsView(View):
    #处理get请求
    def get(self,request):
        return JsonResponse({'method':'get'})

    #处理post请求
    def post(self,request):
        return JsonResponse({'method':'get'})

    #处理put请求
    def put(self,request):
        return JsonResponse({'method':'get'})

    #处理delete请求
    def delete(self,request):
        return JsonResponse({'method':'get'})