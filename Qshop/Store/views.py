from django.shortcuts import render_to_response
from .forms import RegisterUser
from .forms import PersonForm
from django.shortcuts import render
from .models import *
#json与ajax测试，返回一个json格式的用户信息
from django.http import JsonResponse
#CBV class base views  基于类的视图，类视图
from django.views import View

#导入重定向
from django.http import HttpResponseRedirect

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

        return HttpResponseRedirect('/store/login')
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
                response = HttpResponseRedirect("/store/index")  # 校验成功重定向到index界面
                # cookie与session设置要依赖于响应对象
                # 设置cookie
                response.set_cookie("name",username,expires=259200)

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
                return HttpResponseRedirect("/store/login/")
            else:
                message = registeruser.errors

        elif not username:
            message = "请输入账号名"
        elif not password:
            message = "请输入密码，密码不能为空"
        elif password != repassword:
            message= "两次输入的密码不一致"

    return render(request,"store/register.html",locals())

@LoginValid
def index(request):


    return render_to_response("store/index.html",locals())

@LoginValid
#添加商品页面
def add_goods(request):

    return render_to_response("store/add_goods.html",locals())

#api接口拿商品数据，使用drf-djangorestframerwork
#从http://127.0.0.1:8000/store/api/morelist/?type_id=1接口拿数据
#serializer数据在Store应用中


@LoginValid
def orders(request):

    return render_to_response("store/orders.html",locals())

@LoginValid
def count_goods(request):

    return render_to_response("store/count_goods.html",locals())

@LoginValid
def count_orders(request):

    return render_to_response("store/count_orders.html",locals())

@LoginValid
def store(request):

    return render_to_response("store/store.html",locals())



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