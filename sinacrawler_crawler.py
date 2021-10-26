import requests
import json
from bs4 import BeautifulSoup
import os
import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import re


from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

px_finder=re.compile(r'<div class="vue-recycle-scroller__item-view" style="transform: translateY\(([0-9]+)px\);"')
timeall=re.compile(r'\d{4}-\d{2}-\d{2}')


class weibopassage:# class for on tiwt's message
    def __init__(self,user='',time_year=0,time_month=0,time_day=0,passage='',retweetnumber='',commentnumber='',likenumber=''):
        self.user=user
        self.time_year=time_year
        self.time_month=time_month
        self.time_day=time_day
        self.passage=passage
        self.retweetnumber=retweetnumber
        self.commentnumber=commentnumber
        self.likenumber=likenumber

def usersearch(username,pagemessage):
    lootpath = os.getcwd()
    path = lootpath + '/chromedriver.exe'
    url='https://s.weibo.com/user?q='+username+'&Refer=index'#sina user search api
    print(url)
    ran=random.uniform(5,8)
    time.sleep(ran)
    try:
        pagemessage.get(url)
        usermessage=pagemessage.page_source
        usermessageB=BeautifulSoup(usermessage,"html.parser")
        targetuser_pagemessage=usermessageB.find(class_='avator')
        targetuserurl_a=targetuser_pagemessage.find('a')
        targetuserurl='https:'+targetuserurl_a['href']
        return targetuserurl#user's homepage url
    except:
        print("用户查询失败！")
        return 0

def userweibospider(filename,username,userurl,pagemessage1,pagemessage2,searchyear,searchmonth):# main function of spider
    try:
        filerealename=filename+'.txt'
        file=open(filerealename,'a+',encoding='utf-8')
    except:
        print("文件无法正常访问")
    try:
        pagemessage1.get(userurl)
        scrollnumber = 0
        scrolltime = 0
        scroll = ''
        pxbox_number=0
        pxbox=[]#this list is used to get the loaded twits' sign(where they are at the browser)
        while (pxbox_number<30):
            pxbox.append(-1)
            pxbox_number+=1
        stopspider=0
        ran = random.uniform(5, 6)
        time.sleep(ran)
        useless_rolltime=0
        while (stopspider==0):
            scrollnumber=scrollnumber+1500
            ran=random.uniform(59,234)
            scrollnumber=ran+scrollnumber
            scrollnumberstr = str(scrollnumber)
            print('准备滚动')
            useless_rolltime+=1
            if (useless_rolltime == 6):
                print("浏览器暂时未响应，按任意键恢复")
                rolltime_reset = input()
                useless_rolltime = 0#if you rolled the scroll 6 time and still cannot find a new twit, then stop spider temporarily
            try:
                scroll = ('var q=document.documentElement.scrollTop='+scrollnumberstr)
                pagemessage1.execute_script(scroll)# roll thw scroll
                ran = random.uniform(2, 3)
                time.sleep(ran)
                userhomepage_message=pagemessage1.page_source
                userhomepage_messageB=BeautifulSoup(userhomepage_message,"html.parser")
                print('页面读取完成')
                userhomepage_message_list=userhomepage_messageB.find_all(class_='vue-recycle-scroller__item-view')
                print('messagelist读取完成')
                for one_userhomepage_message in userhomepage_message_list:#get one tiwt
                    timestart = time.time()
                    one_userhomepage_message_str=str(one_userhomepage_message)
                    one_userhomepage_message_px=px_finder.search(one_userhomepage_message_str)
                    try:
                        one_px=re.sub(r'<div class="vue-recycle-scroller__item-view" style="transform: translateY\(','',one_userhomepage_message_px.group(0))#judge if the twit have already loaded by compair their px value
                        one_px=re.sub(r'px\);"','',one_px)
                        one_px=int(one_px)
                        flag=0
                        for pxone in pxbox:
                            if (pxone==one_px):
                                flag=1#already loaded
                        if (flag==0):#unload twit
                            stopspider=tweetreader(file,username,one_userhomepage_message,searchyear,searchmonth,pagemessage2)#analyze the twit's message
                            cent=pxbox[0]
                            place=0
                            for pxone in pxbox:
                                if  cent>=pxone:
                                    cent=pxone
                                    smallpx_place=place#get the smallest px value in the pxbox in order to replace it with new px value just loaded
                                place+=1
                            pxbox[smallpx_place]=one_px#renew the pxbox
                            timeend=time.time()
                            print("耗时:",timeend-timestart)
                            printed=1#insure the twit loading successful
                    except:
                        useless=0
                if (printed==1):
                    useless_rolltime = 0
                    printed=0
                try:
                    endsignal = userhomepage_messageB.find(class_='Bottom_text_1kFLe')
                    endsignalstr = str(endsignal)
                    if (endsignalstr == '<div class="Bottom_text_1kFLe">没有更多内容了~去其他页面看看吧</div>'):
                        print("浏览器暂时未响应，按任意键恢复")
                        rolltime_reset = input()
                        useless_rolltime = 0#if you get the network error, stop the spider temporarily
                except:
                    useless = 0
            except:
                print('微博爬取出现未知异常，按任意键返回上一单元!')
                mainuiback=input()
                stopspider=1#server bug, stop the spider
            if(stopspider==1):
                file.close()
    except:
        print('无法访问此用户空间！')

def tweetreader(file,username,tweet,searchyear,searchmonth,pagemessage2):
    usertweet = weibopassage()
    usertweet.user=username
    tweet_timeclass=tweet.find(class_='woo-box-flex woo-box-alignCenter woo-box-justifyCenter head-info_info_2AspQ')
    tweet_time_a=tweet_timeclass.find('a')
    tweet_time_str=str(tweet_time_a['title'])
    longtexturl=str(tweet_time_a['href'])
    try:
        time_all=timeall.search(tweet_time_str)#get the twit's release time
        tweet_time_str=time_all.group(0)
        tweet_time=re.split('-',tweet_time_str)
        print(tweet_time)
        usertweet.time_year=int(tweet_time[0])
        usertweet.time_month=int(tweet_time[1])
        usertweet.time_day=int(tweet_time[2])
        tweet_textclass=tweet.find(class_='detail_wbtext_4CRf9')
        tweet_text=str(tweet_textclass.get_text())
        if (tweet_text.find('.展开')==-1):#if the twit do not has long text
            tweet_text=re.sub('【','',tweet_text)
            tweet_text=re.sub('#','',tweet_text)
            tweet_text=re.sub('】',' ',tweet_text)
            tweet_text=re.sub('@','',tweet_text)
            tweet_text=re.sub('↓','',tweet_text)
            tweet_text = riblast(tweet_text)
            print('推文=',tweet_text)
            usertweet.passage=tweet_text
        else:
            try:#if the twit has long text
                print('L')
                times=time.time()
                pagemessage2.get(longtexturl)
                locator1 = (By.CLASS_NAME, 'detail_wbtext_4CRf9')
                locator2 = (By.CLASS_NAME,'expand')
                WebDriverWait(pagemessage2, 4, 0.5).until(EC.presence_of_element_located(locator1))
                time.sleep(0.5)#wait for text loading
                WebDriverWait(pagemessage2, 4, 0.5).until_not(EC.presence_of_element_located(locator2))
                time.sleep(0.5)#wait for thw whole text loading
                longtextmessage=pagemessage2.page_source
                timee=time.time()
                print("网页耗时",timee-times)#calculate the time spend on loading long text
                longtextmessageB=BeautifulSoup(longtextmessage,"html.parser")
                longtextmessageclass=longtextmessageB.find(class_="detail_wbtext_4CRf9")
                longtext=str(longtextmessageclass.get_text())
                longtext=re.sub('【','',longtext)
                longtext=re.sub('#','',longtext)
                longtext=re.sub('】',' ',longtext)
                longtext=re.sub('@','',longtext)
                longtext=re.sub('↓','',longtext)
                longtext=riblast(longtext)
                print("推文L=",longtext)
                usertweet.passage=longtext#get the long text
            except:#if cannot get the long text, get the short version of it
                tweet_text = re.sub('【', '', tweet_text)
                tweet_text = re.sub('#', '', tweet_text)
                tweet_text = re.sub('】', ' ', tweet_text)
                tweet_text = re.sub('@', '', tweet_text)
                tweet_text = re.sub('↓','',tweet_text)
                tweet_text = re.sub('...展开$', '', tweet_text)
                print('推文=', tweet_text)
                usertweet.passage = tweet_text
        try:
            tweet_react=tweet.find(class_='woo-box-flex woo-box-alignCenter toolbar_left_2vlsY toolbar_main_3Mxwo')
            tweet_reacts=tweet_react.find_all(class_='toolbar_num_JXZul')
            retweetnumber=tweet_reacts[0].get_text()
            commentnumber=tweet_reacts[1].get_text()
            tweet_like=tweet_react.find(class_='woo-like-count')
            likenumber=tweet_like.get_text()
            print('retweet=',retweetnumber,'comment=',commentnumber,'like=',likenumber)
            usertweet.retweetnumber=retweetnumber
            usertweet.commentnumber=commentnumber
            usertweet.likenumber=likenumber
        except:
            retweetnumber=' 0 '
            commentnumber=' 0 '
            likenumber='0'
    except:
        return 0
    if searchyear == usertweet.time_year:
        if searchmonth >= usertweet.time_month:
            return 1
    str_retweetnumber=str(retweetnumber)
    str_commentnumber=str(commentnumber)
    str_likenumber=str(likenumber)
    write_string='*@!user:'+usertweet.user+','+tweet_time[0]+':'+tweet_time[1]+':'+tweet_time[2]+','+usertweet.passage+',!@*retweet='+str_retweetnumber+',comment='+str_commentnumber+',like='+str_likenumber+'\n'
    print(write_string)
    file.write(write_string)#write twit in txt
    print('OK')
    return 0

def riblast(text):#insure the twit's passage end with a legal punctuation
    text1 = text
    text2 = text
    try:
        long=len(text)
        one=''
        lethal=0
        ribplace=long
        while (lethal == 0):
            one=text[ribplace-1]
            ribplace-=1
            if one=='。'or one=='？'or one=='”'or one=='！':
                lethal=1
        text1 = text[0:ribplace+1]
        return(text1)
    except:
        return text2