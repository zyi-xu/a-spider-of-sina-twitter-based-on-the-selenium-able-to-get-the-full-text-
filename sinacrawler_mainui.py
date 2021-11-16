import requests
import json
from bs4 import BeautifulSoup
import os
import selenium
from selenium import webdriver
import time
import re
import random
import datetime
from sinacrawler_crawler import usersearch
from sinacrawler_crawler import userweibospider
from sinacrawler_dataprocessing import DataProcessing

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from sinacrawler_data_analysis import databasecheck
from sinacrawler_data_analysis import tablecheck
from sinacrawler_data_analysis import wordcloudgenerator
from sinacrawler_data_analysis import twitspliter

def spiderui():
    keyback=0
    lootpath = os.getcwd()
    path = lootpath + '/chromedriver.exe'
    url = 'http://weibo.com'
    print(url)
    try:
        pagemessage1 = webdriver.Chrome(path)
        des = DesiredCapabilities.CHROME
        des["pageLoadStrategy"] = "none"
        pagemessage2 = webdriver.Chrome(path)
        #pagemessage2.implicitly_wait(4)
        pagemessage1.get(url)#first page for getting the sina twit list
        pagemessage1.set_window_size(1500,1000)
        pagemessage2.get(url)#second page for getting the long text twit
        print('请在浏览器中完成登录操作，完成后按任意键继续')
        keycrawlerui = input()
        os.system('cls')
    except:
        print('浏览器驱动缺失！,任意键返回上一单元')
        keycrawlerui = input()
        keyback=1
        os.system('cls')
        return 0
    print("输入txt文件名，不需要带末尾的.txt")
    filename=input()

    os.system('cls')

    while(keyback==0):
        print('1:爬取用户列表\n2.爬取单个用户\n3.返回上一级菜单')
        keynumber=input()
        os.system('cls')
        if (keynumber=='1'):
            searchtimelist = searchtimeget()#get the time of spider's ending
            print("爬取", searchtimelist[0], searchtimelist[1], "之后的微博")
            localusernamelist="username.txt"
            print('正在爬取列表用户')
            try:#load in the user list
                userlisttxt=open(localusernamelist,'r+',encoding='utf-8',errors='ignore')
                userlist=userlisttxt.readlines()
                n = 0
                for oneusername in userlist:
                    oneusername=oneusername.strip()
                    userlist[n]=oneusername
                    n+=1
                n=0
                userurllist=[]
                usernamelist=[]
                for oneusername in userlist:#get everyone's homepage url in the userurllist
                    print('正在爬取',oneusername,'\n')
                    userurl=usersearch(oneusername,pagemessage1)
                    if userurl!=0:
                        userurllist.append(userurl)
                        usernamelist.append(oneusername)
                i=0
                for oneuserurl in userurllist:
                    oneusername=usernamelist[i]#get the url's user name
                    i+=1
                    userweibospider(filename,oneusername,oneuserurl,pagemessage1,pagemessage2,searchtimelist[0],searchtimelist[1])#get one user's twits
                print('用户列表查询完毕')
                print('按任意键返回')
                keycrawlerui = input()
                os.system('cls')
            except:
                print('读取文件失败\n')
                print('按任意键返回')
                keycrawlerui=input()
                os.system('cls')
        if(keynumber=='2'):
            print('输入要爬取的用户名：')
            username=input()
            print("要爬取到哪年哪月？（输入示例：2018/09）")
            searchtimelist=searchtimeget()
            print("爬取", searchtimelist[0], searchtimelist[1], "之后的微博")
            print('正在爬取',username,'\n')
            userurl=usersearch(username,pagemessage1)#get one user's homepage url in the userurllist
            if userurl!=0:
                print('用户查询成功')
                userweibospider(filename,username,userurl,pagemessage1,pagemessage2,searchtimelist[0],searchtimelist[1])#get one user's twits
            print('按任意键返回')
            keycrawlerui = input()
            os.system('cls')
        if(keynumber=='3'):
            keyback=1

def searchtimeget():
    timeget = 0
    while (timeget == 0):
        searchtime = input()
        try:
            check = re.compile(r'\d{4}/\d{2}')#insure that the input time is legal
            timelocalyearstr = datetime.datetime.now().strftime('%Y')
            timelocalyear=int(timelocalyearstr)
            timelocalmonthstr = datetime.datetime.now().strftime('%m')
            timelocalmonth=int(timelocalmonthstr)
            searchtime_r = check.search(searchtime)
            searchtime = searchtime_r.group(0)
            yearcompile=re.compile(r'\d{4}')
            searchyearrecen = yearcompile.search(searchtime)
            searchyearstr=searchyearrecen.group(0)
            searchyear=int(searchyearstr)
            searchmonthstr = re.sub(r'\d{4}/','', searchtime)
            searchmonth=int(searchmonthstr)
            if timelocalyear > searchyear and searchyear >= 2010 and 0<searchmonth<13:
                timeget = 1
            if timelocalyear == searchyear:
                if timelocalmonth >= searchmonth and searchmonth>0:
                    timeget = 1
        except:
            print("时间输入错误请重新输入！")
    if searchmonth != 1:#the spider will stop after it got the twit released at 2020/12/31 if the user input '2021/01'
        searchmonth = searchmonth - 1
    else:
        searchmonth = 12
        searchyear = searchyear - 1
    searchtimelist=[searchyear,searchmonth]
    return searchtimelist

def DataProcessingUi():
    EndDataProcessing=0
    while(EndDataProcessing==0):
        os.system('cls')
        print('1.开始数据入库,2.返回上一级菜单')
        keynumber = input()
        if (keynumber=='1'):
            inputfinish=0
            while inputfinish==0:
                print('请输入数据库名')#库叫sina
                databasename=input()
                print('请输入sql数据库密码')
                password=input()
                print('请输入表名')
                tablename=input()
                print('请输入要入库的文件名(不需要结尾的.txt)')
                filename=input()
                print('是否确认？\n1.是\n2.否')
                check=input()
                if check=='1':
                    inputfinish=1
                else:
                    inputfinish=0
                    os.system('cls')

            k=DataProcessing(databasename,password,tablename,filename)
            if k==0:
                print('入库完成！按任意键继续')
            returnkey=input()
        if (keynumber=='2'):
            EndDataProcessing=1

def DataAnalysisUi():
    databasecheckresult=1
    while databasecheckresult==1:
        print('请输入sql数据库密码')
        password=input()
        print('请输入您想要访问的数据库')
        database=input()
        databasecheckresult=databasecheck(password,database)
    endcheck=0
    while endcheck==0:
        print('请选择您希望的查询方式\n1.词云生成\n2.海内外博文相关数据查询\n3.用户总体博文发布特征查询\n4.返回上级菜单')
        searchcheck=input()
        if searchcheck=='1':
            ciyunend = 0
            while ciyunend==0:
                print('1.批量生成词云 2.指定月份生成词云 3.指定年份生成词云 4.返回上一级菜单')
                ciyuncheck=input()
                if ciyuncheck=='1':
                    table=tableinput(password,database)
                    print('请输入要生成词云的用户名')
                    username=input()
                    print('请输入要生成的年份（批量按月生成词云）')
                    year=input()
                    wordcloudgenerator(password,database,table,1,username,year)
                    print('生成完毕！')
                if ciyuncheck=='2':
                    table = tableinput(password, database)
                    print('请输入要生成词云的用户名')
                    username=input()
                    print('请输入要查询的年份月份')
                    searchtimelist=[]
                    searchtimelist = searchtimeget()
                    if searchtimelist[1]==12:
                        searchtimelist[0]+=1
                        searchtimelist[1]=1
                    else:
                        searchtimelist[1]+=1
                    wordcloudgenerator(password,database,table,2,username,searchtimelist[0],searchtimelist[1])
                    print('生成完毕！')
                if ciyuncheck=='3':
                    table = tableinput(password, database)
                    print('请输入要生成词云的用户名')
                    username=input()
                    print('请输入要查询的年份')
                    year=input()
                    wordcloudgenerator(password,database,table,3,username,year)
                    print('生成完毕！')
                if ciyuncheck=='4':
                    ciyunend=1
                os.system('cls')
        if searchcheck=='2':
            check=0
            while check==0:
                print('1.查询海内外推文发布数量，比例与热度\n2.查询海内外推文正负面比率\n3.查询涉及特定实体的推文热度，正负面比率\n4.返回上一级菜单')
                foreigncheck=input()
                if foreigncheck=='1':
                    table = tableinput(password, database)
                    print('请输入您要查询的用户名')
                    username=input()
                    longsearchtimelist=timeinput()
                    splitsignal=twitspliter(password,database,table,username,longsearchtimelist,1)
                    if splitsignal==1:
                        print('图表生成失败！')
                if foreigncheck=='2':
                    print('ok')
                if foreigncheck=='3':
                    table = tableinput(password, database)
                    print('请输入您要查询的用户名')
                    username = input()
                    longsearchtimelist = timeinput()
                    splitsignal = twitspliter(password, database, table, username, longsearchtimelist, 2)
                    if splitsignal==1:
                        print('图表生成失败！')
                if foreigncheck=='4':
                    check=1
                os.system('cls')
        if searchcheck=='3':
            table = tableinput(password, database)
            print('请输入您要查询的用户名')
            username = input()
            longsearchtimelist = timeinput()
            totalsignal=twitspliter(password,database,table,username,longsearchtimelist,3)
            if totalsignal==1:
                print('图表生成失败！')

        if searchcheck=='4':
            endcheck=1
        else :
            endcheck=0
            os.system('cls')
    return 0

def tableinput(password,database):
    print('请输入您要访问的表')
    check = 1
    while check == 1:
        table = input()
        check = tablecheck(password, database, table)
    return table

def timeinput():
    timecheck = 0
    while timecheck == 0:
        print('请输入要查询的起始时期（例2020/01）')
        starttimelist = []
        starttimelist = searchtimeget()
        if starttimelist[1] == 12:
            starttimelist[0] += 1
            starttimelist[1] = 1
        else:
            starttimelist[1] += 1
        print('请输入要查询的终止时期（例2020/01）')
        endtimelist = []
        endtimelist = searchtimeget()
        if endtimelist[1] == 12:
            endtimelist[0] += 1
            endtimelist[1] = 1
        else:
            endtimelist[1] += 1
        if starttimelist[0] < endtimelist[0]:
            timecheck = 1
        if starttimelist[0] == endtimelist[0] and starttimelist[1] <= endtimelist[1]:
            timecheck = 1
        if timecheck == 0:
            print('查询时期输入错误！')
        num1=int(starttimelist[0])
        num2=int(starttimelist[1])
        num3=int(endtimelist[0])
        num4=int(endtimelist[1])
    returntimelist=[num1,num2,num3,num4]
    return returntimelist

def uisystem():#User Interface
    while(1):
        print("新浪微博推文爬取系统：v1.0\n")
        print('1:爬取目标用户推文\n2.读取本地推文数据库\n3.推文数据分析工具\n')
        keynumber = input()
        os.system('cls')
        if (keynumber == '1'):
            spiderui()
        if (keynumber == '2'):
            DataProcessingUi()
        if (keynumber == '3'):
            DataAnalysisUi()