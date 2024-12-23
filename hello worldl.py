import time
import sympy
import math
import tkinter as tk

def test():
    for i in range(10):
        print(i)

    print("helllo world~")   #hello world

    str = 'abcdefgh'
    print((str + "hello") * 2)
    a = 10
    b = False
    print(a and b)
    print(a or b)

    list1 = [1,2,3,10,5,6];
    if ( a in list1 ):
        print("ok")
    if ( b in list1 ):
        print("thank you")

    magincians = ['alic', 'david', 'carolina']
    for magician in magincians:
        print(magician)

    a = ~a


def test1( mylist ):
    mylist.append([1,2,3,4])
 
mylist = [10,20,30]

a = 3 
def myfunc(a):
#    global a
    a += 2
    print("内",a)
    return a

class dog:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def prt_name(self):
        print("dog name is {self.name},mydog age is {self.age}")

def test2(name,age):
    mydog = dog(name,age)
    mydog.prt_name()
    print("mydog name is {mydog.name},mydog age is {mydog.age}")

if __name__ == "__main__":
    #test2('xt',18)
    #test()
    #test1(mylist)
    #print(mylist)
    #print(id(a))
    #a = myfunc(a)
    #print(id(a))
    print("外",a)
    '''
    time_list = []
    time_list = time.localtime()

    time_str_list = []
    time_str = time.strftime("%Y-%m-%d %H:%M:%S",time_list)
  #  time_str_list = [str for str in time_str]
    time_str_list = [time_str]

    print(time_list)
    print(type(time_list))
    print(time_str)
    print(type(time_str))
    print(time_str_list)
    print(type(time_str_list))
    '''
    print('CALC1:MEAS:DATA:SNP:PORTs:Save ' + '\'1,2\'' + ',' + '\'D:\MyData.s2p\'')
    
    

class Order_List:
    def __init__(self):
        self.list = []
    #    self.list = 'INST:LIST?'    
       
        def list(self):
            self.list.multiview_tab = 'DISPlay:ATAB ON'     #分4屏显示开
            return self.list

    

