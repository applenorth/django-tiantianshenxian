#-*- coding:utf-8 -*-
"""
@Time:2020/10/216:51
@Auth:DaiXvWen
@File:study_class.py
"""


class Employee:
    '所有员工的基类'
    empCount = 0

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.empCount += 1

    def displayCount(self):
        print("Total Employee %d" % Employee.empCount)

    def displayEmployee(self):
        print("Name : ", self.name, ", Salary: ", self.salary)

# a=Employee('李嗨涛','100')  #实例化一个对象
# a.age=7
# print(a.age)
# print(a.displayCount)
# print(a.empCount)
# b=Employee('姜雨','90')
# a.displayEmployee()
#
# b.displayEmployee()
# c=Employee('姜雨1','901')

# print("Employee.__doc__:",Employee.__doc__)         #类的文档字符串
# print("Employee.__name__:",Employee.__name__)       #类的名字
# print("Employee.__module__:",Employee.__module__)   #类定义所在的模块
# print("Employee.__bases__:",Employee.__bases__)     #类的所有父类构成元素（包含了一个由所有父类组成的元祖）
# print("Employee.__dict__:",Employee.__dict__)       #类的属性（包含一个字典，由类的数据属性组成）


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __del__(self):
        class_name = self.__class__.__name__
        print(class_name, "销毁")


pt1 = Point()
pt2 = pt1
pt3 = pt1
print(id(pt1), id(pt2), id(pt3))  # 打印对象的id

