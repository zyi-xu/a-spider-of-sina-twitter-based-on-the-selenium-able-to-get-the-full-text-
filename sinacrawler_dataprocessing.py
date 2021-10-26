import pymysql
import re

class singledata():
    def __init__(self):
        self.user = ''
        self.time_year = 0
        self.time_month = 0
        self.time_day = 0
        self.passage = ''
        self.retweetnumber = 0
        self.commentnumber = 0
        self.likenumber = 0
    def loadin(self,text):
        usercomp=re.compile(r'\*@!user:.*,\d{4}:\d{2}:\d{2},')
        timecomp=re.compile(r',\d{4}:\d{2}:\d{2},')
        timeyearcomp=re.compile(r'\d{4}')
        timemonthcomp=re.compile(r':\d{2}:')
        passagecomp=re.compile(r',\d{4}:\d{2}:\d{2},.*,!@\*')
        numbercomp=re.compile(r',!@\*retweet= .* ,comment= .* ,like=.*')
        User=''
        Timeyear=0
        Timemonth=0
        Timeday=0
        Passage=''
        Retweetnumber=0
        Commentnumber=0
        Likenumber=0
        try:
            Usergroup=re.search(usercomp,text)
            User=str(Usergroup.group(0))
            User=re.sub(r'\*@!user:','',User)
            User=re.sub(r',\d{4}:\d{2}:\d{2},','',User)
        except:
            User=''
        try:
            Timegroup=re.search(timecomp,text)
            Time=str(Timegroup.group(0))
            Time=Time[1:]
            Time=Time[:-1]
            Timeyeargroup=re.search(timeyearcomp,Time)
            Timeyearstr=str(Timeyeargroup.group(0))
            Timeyear=int(Timeyearstr)
            Timemonthgroup=re.search(timemonthcomp,Time)
            Timemonthstr=str(Timemonthgroup.group(0))
            Timemonthstr=Timemonthstr[1:]
            Timemonthstr=Timemonthstr[:-1]
            Timemonth=int(Timemonthstr)
            Time=re.sub(r'\d{4}:\d{2}:','',Time)
            Timedaystr=Time
            Timeday=int(Timedaystr)
        except:
            Timeyear=0
            Timemonth=0
            Timeday=0
        try:
            passagegroup=re.search(passagecomp,text)
            Passage=str(passagegroup.group(0))
            Passage=re.sub(',\d{4}:\d{2}:\d{2},','',Passage)
            Passage=re.sub(',!@\*','',Passage)
            Passage=re.sub('↓','',Passage)
            Passage=re.sub('  ','',Passage)
            Passage=re.sub('的微博视频','',Passage)
            ribpassage1='微博官方唯一抽奖工具微博抽奖平台'
            if (Passage.find(ribpassage1)!=-1):
                Passage=''
            ribpassage2='31个省（自治区、直辖市）和新疆生产建设兵团报告新增确诊病例'
            if (Passage.find(ribpassage2)!=-1):
                Passage=''
        except:
            Passage=''
        try:
            numbgroup=re.search(numbercomp,text)
            numb=str(numbgroup.group(0))
            Retweetnumberstr=re.sub(',!@\*retweet= ','',numb)
            Retweetnumberstr=re.sub(' ,comment= .* ,like=.*','',Retweetnumberstr)
            if(Retweetnumberstr.find('万')!=-1):
                Retweetnumberstr=Retweetnumberstr[:-1]
                if(Retweetnumberstr.find('.')!=-1):
                    Retweetnumberstrlist=[]
                    Retweetnumberstrlist=Retweetnumberstr.split('.')
                    Retweetnumber1=int(Retweetnumberstrlist[0])
                    Retweetnumber1=Retweetnumber1*10000
                    Retweetnumber2=int(Retweetnumberstrlist[1])
                    Retweetnumber2=Retweetnumber2*1000
                    Retweetnumber=Retweetnumber1+Retweetnumber2
                else:
                    Retweetnumber=int(Retweetnumberstr)
                    Retweetnumber=Retweetnumber*10000
            else:
                if(Retweetnumberstr==' 转发 '):
                    Retweetnumberstr='0'
                Retweetnumber=int(Retweetnumberstr)
            Commentnumberstr=re.sub(',!@\*retweet= .* ,comment= ','',numb)
            Commentnumberstr=re.sub(' ,like=.*','',Commentnumberstr)
            if (Commentnumberstr.find('万') != -1):
                Commentnumberstr = Commentnumberstr[:-1]
                if (Commentnumberstr.find('.') != -1):
                    Commentnumberstrlist=[]
                    Commentnumberstrlist = Commentnumberstr.split('.')
                    Commentnumber1 = int(Commentnumberstrlist[0])
                    Commentnumber1 = Commentnumber1 * 10000
                    Commentnumber2 = int(Commentnumberstrlist[1])
                    Commentnumber2 = Commentnumber2 * 1000
                    Commentnumber = Commentnumber1 + Commentnumber2
                else:
                    Commentnumber = int(Commentnumberstr)
                    Commentnumber = Commentnumber * 10000
            else:
                if (Commentnumberstr==' 评论 '):
                    Commentnumberstr='0'
                Commentnumber = int(Commentnumberstr)
            Likenumberstr=re.sub(',!@\*retweet= .* ,comment= .* ,like=','',numb)
            if (Likenumberstr.find('万') != -1):
                Likenumberstr = Likenumberstr[:-1]
                if (Likenumberstr.find('.') != -1):
                    Likenumberstrlist=[]
                    Likenumberstrlist = Likenumberstr.split('.')
                    Likenumber1 = int(Likenumberstrlist[0])
                    Likenumber1 = Likenumber1 * 10000
                    Likenumber2 = int(Likenumberstrlist[1])
                    Likenumber2 = Likenumber2 * 1000
                    Likenumber = Likenumber1 + Likenumber2
                else:
                    Likenumber = int(Likenumberstr)
                    Likenumber = Likenumber * 10000
            else:
                if(Likenumberstr=='点赞'):
                    Likenumberstr='0'
                Likenumber = int(Likenumberstr)
        except:
            Retweetnumber=0
            Commentnumber=0
            Likenumber=0
        self.user=User
        self.time_year=Timeyear
        self.time_month=Timemonth
        self.time_day=Timeday
        self.passage=Passage
        self.retweetnumber=Retweetnumber
        self.commentnumber=Commentnumber
        self.likenumber=Likenumber
    def printsingle(self):
        print('user=',self.user,'\ntime=',self.time_year,self.time_month,self.time_day,'\npassage=',self.passage,'\nnumber=',self.retweetnumber,self.commentnumber,self.likenumber)
    def timelableget(self):
        timelable=self.time_year*10000+self.time_month*100+self.time_day
        return timelable
    def checkpassage(self,text):
        if text==self.passage:
            return 1
        if text=='':
            return 1
        return 0
    def writeinsql(self,cur,tablename,con):
        try:
            insert="INSERT INTO %s(USER_NAME,TIME_YEAR, TIME_MONTH, TIME_DAY, PASSAGE, RETWEET_NUMBER, COMMENT_NUMBER, LIKE_NUMBER)VALUES ('%s',%d,%d,%d,'%s',%d,%d,%d)"\
                   % (tablename,self.user,self.time_year,self.time_month,self.time_day,self.passage,self.retweetnumber,self.commentnumber,self.likenumber)
            cur.execute(insert)
            con.commit()
            return 1
        except:
            return 0

def DataProcessing(databasename,password,tablename,filename):
    try:
        con = pymysql.connect(host='localhost', user='root', passwd=password, db=databasename)
        cur = con.cursor()
        usedatabase="use "+databasename
        cur.execute(usedatabase)
    except:
        try:
            con = pymysql.connect(host='localhost', user='root', passwd=password,charset='utf8')
            cur=con.cursor()
            databasecreat="create database "+databasename+" character set utf8"
            cur.execute(databasecreat)
            usedatabase="use "+databasename
            cur.execute(usedatabase)
        except:
            print('数据库访问失败,任意键返回上一单元')
            return 1
    try:
        creattable="""CREATE TABLE %s (
         USER_NAME  TEXT NOT NULL,
         TIME_YEAR  INT,
         TIME_MONTH INT,  
         TIME_DAY INT,
         PASSAGE MEDIUMTEXT,
         RETWEET_NUMBER INT,
         COMMENT_NUMBER INT,
         LIKE_NUMBER INT)"""%(tablename)
        cur.execute(creattable)
    except:
        conti=0
        while conti==0:
            print('数据表已存在，是否在已有表的基础上添加新数据\n1.是  2.否')
            tableinsert=input()
            if tableinsert=='2':
                return 1
            if tableinsert=='1':
                useless=0
                conti=1

    try:
        filename=filename+'.txt'
        readin=0
        numberoftime=[]
        twitterdata=[[]]
        twitnumber=0
        txtnumber=0
        with open(filename,'r+',encoding='utf-8') as file:
            for line in file:
                line=line.encode('utf-8','ignore')
                line=line.decode('utf-8','ignore')
                onemessage=singledata()
                onemessage.loadin(line)
                #onemessage.printsingle()
                txtnumber+=1
                time1=0
                timecheck=0
                for onetimelable in numberoftime:
                    if onemessage.timelableget()==onetimelable:
                        timecheck=1
                        time2=0
                        for onetwitterlist in twitterdata:
                            if time1==time2:
                                check=0
                                for singletwitter in onetwitterlist:
                                    checkreturn=singletwitter.checkpassage(onemessage.passage)
                                    if checkreturn==1:
                                        check=1
                                if check==0:
                                    onetwitterlist.append(onemessage)#this 2d list like [[twit(from 2021/01/01))],[twit(from(2021/01/02)],[twit(from(2021/01/03)]......]
                                    print('加载一项数据')
                            time2+=1
                    time1+=1
                if timecheck==0:
                    numberoftime.append(onemessage.timelableget())
                    oonetwitterlist=[onemessage]
                    twitterdata.append(oonetwitterlist)
                    print('——————————————加载新的一天的数据—————————————————————')
            print('载入中。。。')
            for onelist in twitterdata:
                for oneme in onelist:
                    twitnumber+=oneme.writeinsql(cur,tablename,con)
            readsql="SELECT * FROM %s"%(tablename)
            cur.execute(readsql)
            backvalue=cur.fetchall()
            for onesqlmessage in backvalue:
                print('user=',onesqlmessage[0],'time=',onesqlmessage[1],':',onesqlmessage[2],':',onesqlmessage[3],'\npassage=',onesqlmessage[4],'\nretweetnumber=',onesqlmessage[5],' commentnumber=',onesqlmessage[6],' likenumber=',onesqlmessage[7])
            print("总载入数=", txtnumber, ",入库数=", twitnumber)
        file.close()
        con.close()
        return 0


    except:
        print("文件访问失败")
        return 1

