import pymysql
import re
from os import path
from PIL import Image
import numpy as np
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def databasecheck(password,databasename):
    try:
        con = pymysql.connect(host='localhost', user='root', passwd=password, db=databasename)
        cur = con.cursor()
        usedatabase="use "+databasename
        cur.execute(usedatabase)
        tablecheck="SHOW TABLES"
        cur.execute(tablecheck)
        tables=cur.fetchall()
        try:
            print('当前数据库包含表：')
            for one in tables:
                onestr=str(one)
                onestr=onestr[2:]
                onestr=onestr[:-3]
                print(onestr)
            con.close()
            print('\n')
            return 0
        except:
            print('当前数据库中无表格！')
            con.close()
            return 1
    except:
        print('数据库不存在或密码输入错误！')
        return 1

def tablecheck(password,databasename,table):
    try:
        con = pymysql.connect(host='localhost', user='root', passwd=password, db=databasename)
        cur = con.cursor()
        usedatabase = "use " + databasename
        cur.execute(usedatabase)
        getuser='SELECT USER_NAME FROM %s'%(table)
        cur.execute(getuser)
        userall=cur.fetchall()
        userlist=[]
        for one in userall:
            if one not in userlist:
                userlist.append(one)
        print('当前表内记录的用户数据有：')
        for one in userlist:
            onestr=str(one)
            onestr=onestr[2:]
            onestr=onestr[:-3]
            if len(onestr) != 0:
                print (onestr)
        print('\n')
        return 0
    except:
        print('查无此表！')
        return 1

def getlist_fromsql(searchname,table,year,month,cur):
    try:
        searchname='\''+searchname+'\''
        select='SELECT * FROM %s WHERE USER_NAME = %s AND TIME_YEAR = %d AND TIME_MONTH = %d'%(table,searchname,year,month)
        cur.execute(select)
        resultlist=[]
        resultlist=cur.fetchall()
        if len(resultlist)==0:
            print('数据表内无查询信息')
            return 1
        return resultlist
    except:
        print('查询数据表失败')
        return 1

def wordcloudbuild(message,searchname,year,month):
    default_mode = jieba.cut(message)
    text = " ".join(default_mode)
    #alice_mask = np.array(Image.open(path.join("1.png")))
    with open('cn_stopwords.txt', 'r', encoding='utf-8') as stopfile1:
        stopwordss = stopfile1.readlines()
    stopwords = []
    for one in stopwordss:
        one = one[:-1]
        stopwords.append(one)
    with open('wordcloud_stopword.txt','r',encoding='utf-8') as stopfile2:
        stopwordsss=stopfile2.readlines()
    for one in stopwordsss:
        one = one[:-1]
        stopwords.append(one)

    wc = WordCloud(
        font_path=r'E:/sinacrawler/font/SimHei.ttf',
        background_color="white",
        max_words=500,
        max_font_size=80,
        min_font_size=6,
        width=600,
        height=800,
        # mask=alice_mask,
        stopwords=stopwords)
    wc.generate(text)
    yearstr=str(year)
    monthstr=str(month)
    savename=""
    savename=searchname+'_'+yearstr+'_'+monthstr+'.jpg'
    print(savename)
    savenamestr=str(savename)
    wc.to_file(path.join(savenamestr))


def wordcloudgenerator(password,databasename,table,way,searchname,year,month='13'):
    try:
        year=int(year)
        month=int(month)
        con = pymysql.connect(host='localhost', user='root', passwd=password, db=databasename)
        cur = con.cursor()
        usedatabase = "use " + databasename
        cur.execute(usedatabase)
        if way==1:
            i=1
            while i<=12:
                feedbackall=[]
                feedback=getlist_fromsql(searchname,table,year,i,cur)
                if feedback !=1:
                    #feedbackall.append(feedback)
                    message=''
                    for onetwit in feedback:
                        message += (onetwit[4] + '\n')
                    wordcloudbuild(message,searchname,year,i)
                i+=1
        if way==2:
            feedback=getlist_fromsql(searchname,table,year,month,cur)
            message=''
            for onetwit in feedback:
                message+=(onetwit[4]+'\n')
            wordcloudbuild(message,searchname,year,month)
        if way==3:
            i = 1
            while i <= 12:
                feedback=getlist_fromsql(searchname,table,year,i,cur)
                i += 1
            message=''
            for onetwit in feedback:
                message+=(onetwit[4] + '\n')
            wordcloudbuild(message,searchname,year,'全年')
        print('ok')
    except:
        print('发生未知错误！')

def twitspliter(password,databasename,table,searchname,searchtimelist,splitway,splitword='none'):
    try:
        con = pymysql.connect(host='localhost', user='root', passwd=password, db=databasename)
        cur = con.cursor()
        usedatabase = "use " + databasename
        cur.execute(usedatabase)
        timeselectresul=timebaseselector(cur,searchname,table,searchtimelist)
    except:
        print('出现未知错误！')
        return 1
    if splitway==1:
        splitedwordlist=[]
        with open ('internationalword.txt','r',encoding='utf-8') as splitwl:
            splitwordlist=splitwl.readlines()
        for oneword in splitwordlist:
            oneword=oneword[:-1]
            splitedwordlist.append(oneword)
    if splitway==2:
        splitedwordlist = []
        print('请输入您要查询的实体名称（可以是一个，也可以是多个相关实体，输入#号并回车来结束输入）')
        inputcheck=0
        while inputcheck==0:
            one=input()
            if one=='#'and len(splitedwordlist)!=0:
                inputcheck=1
            if one == '#' and len(splitedwordlist) == 0:
                print('请至少输入一个实体名称！')
            if one!='#':
                splitedwordlist.append(one)
    if splitway==3:
        splitedwordlist=['none word that will would in the tiwt']
    everydaytwityes={}
    hotlistyes=[]
    hotlistno=[]
    wordselectresult=wordbaseselector(timeselectresul,splitedwordlist)
    everydaytwityes=timebasecounter(wordselectresult[0],hotlistyes)
    everydaytwitno=timebasecounter(wordselectresult[1],hotlistno)

    graphtimeyes=[]
    graphtimeno=[]
    graphnumyes=[]
    graphnumno=[]
    for key,value in everydaytwityes.items():
        graphtimeyes.append(key)
        graphnumyes.append(value)
    for key,value in everydaytwitno.items():
        graphtimeno.append(key)
        graphnumno.append(value)
    searchtimeliststr = []
    for onetime in searchtimelist:
        onetimestr = str(onetime)
        searchtimeliststr.append(onetimestr)
    if splitway==1:
        continu=0
        if len(graphtimeyes)==len(graphtimeno) and len(graphtimeyes)!=0:
                continu=1
        if continu==0:
            return 1
        savename1 = './' + searchname + searchtimeliststr[0] + '_' + searchtimeliststr[1] + '至' + searchtimeliststr[2] + '_' + searchtimeliststr[3] +'海外新闻比例直方图'+ '.jpg'
        graph1(graphtimeyes,graphnumyes,searchname,searchtimelist,savename1)
        savename2='./' + searchname + searchtimeliststr[0] + '_' + searchtimeliststr[1] + '至' + searchtimeliststr[2] + '_' + searchtimeliststr[3] +'海内外新闻比率折线图'+'.jpg'
        graph2(graphtimeyes,graphtimeno,graphnumyes,graphnumno,searchname,searchtimelist,savename2)
        savename3='./' + searchname + searchtimeliststr[0] + '_' + searchtimeliststr[1] + '至' + searchtimeliststr[2] + '_' + searchtimeliststr[3] +'海内外新闻热度折线图'+'.jpg'
        graph3(graphtimeyes,hotlistyes,savename3)
    if splitway==2:
        continu = 0
        if len(graphtimeyes)==len(graphtimeno) and len(graphtimeyes)!=0:
                continu=1
        if continu == 0:
            return 1
        savename1='./' + searchname + searchtimeliststr[0] + '_' + searchtimeliststr[1] + '至' + searchtimeliststr[2] + '_' + searchtimeliststr[3] +splitedwordlist[0]+'新闻比例直方图'+ '.jpg'
        graph1(graphtimeyes,graphnumyes,searchname,searchtimelist,savename1)
        savename2 = './' + searchname + searchtimeliststr[0] + '_' + searchtimeliststr[1] + '至' + searchtimeliststr[2] + '_' + searchtimeliststr[3] +splitedwordlist[0]+'新闻比率折线图' + '.jpg'
        graph2(graphtimeyes, graphtimeno, graphnumyes, graphnumno, searchname, searchtimelist, savename2)
        savename3 = './' + searchname + searchtimeliststr[0] + '_' + searchtimeliststr[1] + '至' + searchtimeliststr[2] + '_' + searchtimeliststr[3] +splitedwordlist[0]+ '新闻热度折线图' + '.jpg'
        graph3(graphtimeyes, hotlistyes, savename3)
    if splitway==3:
        continu=0
        if len(graphtimeno)!=0:
            continu=1
        if continu==0:
            return 1
        savename1='./' + searchname + searchtimeliststr[0] + '_' + searchtimeliststr[1] + '至' + searchtimeliststr[2] + '_' + searchtimeliststr[3] +'总新闻数量直方图'+ '.jpg'
        graph1(graphtimeno,graphnumno,searchname,searchtimelist,savename1)
        savename3 = './' + searchname + searchtimeliststr[0] + '_' + searchtimeliststr[1] + '至' + searchtimeliststr[2] + '_' + searchtimeliststr[3]+ '总新闻热度折线图' + '.jpg'
        graph3(graphtimeno,hotlistno,savename3)

def timebaseselector(cur,searchname,table,searchtimelist):
    searchtimelisted=[]
    for onetime in searchtimelist:
        searchtimelisted.append(onetime)
    stopgettwit = 0
    twitlist = []
    count = 0
    while stopgettwit == 0:
        twitlist.append(getlist_fromsql(searchname, table, searchtimelisted[0], searchtimelisted[1], cur))
        if searchtimelisted[1] == 12:
            searchtimelisted[0] = searchtimelisted[0] + 1
            searchtimelisted[1] = 1
        else:
            searchtimelisted[1] = searchtimelisted[1] + 1
        if searchtimelisted[0] > searchtimelisted[2]:
            stopgettwit = 1
        if searchtimelisted[0] == searchtimelisted[2] and searchtimelisted[1] > searchtimelisted[3]:
            stopgettwit = 1
    resultlist = []
    for one in twitlist:
        for oneone in one:
            resultlist.append(oneone)
            count += 1
    print('总数为：', count)
    return resultlist

def wordbaseselector(twitlist,splitedwordlist):
    resultcount = 0
    yesresult = []
    noresult = []
    for one in twitlist:
        stopsearch = 0
        for oneword in splitedwordlist:
            if oneword in one[4] and stopsearch == 0:
                yesresult.append(one)
                stopsearch = 1
                resultcount += 1
        if stopsearch==0:
            noresult.append(one)
    print('筛选后总数为', resultcount)
    result=[yesresult,noresult]
    return result

def timebasecounter(twitlist,hotlist):
    timelist = []
    timelable = 0
    everydaytwit = {}
    count=-1
    for one in twitlist:
        timelable = one[1] * 10000 + one[2] * 100
        if timelable in timelist:
            timelablestr = str(timelable)
            everydaytwit[timelablestr] += 1
            hotlist[count][0]+=one[5]
            hotlist[count][1]+=one[6]
            hotlist[count][2]+=one[7]

        if timelable not in timelist:
            timelist.append(timelable)
            timelablestr = str(timelable)
            everydaytwit[timelablestr] = 1
            onemonthhot = [0, 0, 0]
            hotlist.append(onemonthhot)
            count+=1


    return everydaytwit


def graph1(xstr,numlist,searchname,searchtimelist,savename):
    x=[]
    a=1
    xtick=[]
    for onestr in xstr:
        onestr=onestr[:-2]
        one=a
        xtick.append(onestr)
        a+=4
        x.append(one)
    figsizex=len(x)+5
    plt.figure(figsize=(figsizex, 10))
    plt.bar(x,numlist,width=2,color='red',label='tweetnumber')
    for a, b in zip(x, numlist):
        plt.text(a, b, '%.0f' % b,ha='center', fontsize=22)
    plt.xticks(x,xtick)
    #params = {'figure.figsize': '12, 4'}
    #plt.rcParams.update(params)
    plt.legend()
    plt.savefig(savename)
    #plt.show()

def graph2(x1str,x2str,numlist1,numlist2,searchname,searchtimelist,savename):
    count=0
    ratelist=[]
    for num1 in numlist1:
        rate=num1/(num1+numlist2[count])
        rate=rate*100
        rateint=int(rate)
        ratelist.append(rateint)
        count+=1
    x = []
    a = 1
    xtick = []
    for onestr in x1str:
        onestr = onestr[:-2]
        one = a
        xtick.append(onestr)
        a += 4
        x.append(one)
    figsizex = len(x) + 5
    plt.figure(figsize=(figsizex, 10))
    plt.ylim((0,100))
    plt.plot(x,ratelist,linewidth=4,label='released tweet rate')
    for a, b in zip(x, ratelist):
        plt.text(a, b, '%.0f' % b,ha='center', fontsize=10)
    plt.xticks(x, xtick)
    plt.legend()
    plt.savefig(savename)

def graph3(x2str,hotlistyes,savename):
    rt = []
    get = 0
    for one in hotlistyes:
        get = one[0]
        rt.append(get)
    co = []
    for one in hotlistyes:
        get = one[1]
        co.append(get)

    li = []
    for one in hotlistyes:
        get = one[2]
        li.append(get)

    x = []
    a = 1
    xtick = []
    for onestr in x2str:
        onestr = onestr[:-2]
        one = a
        xtick.append(onestr)
        a += 4
        x.append(one)
    figsizex = len(x) + 5
    plt.figure(figsize=(figsizex, 10))
    plt.plot(x,rt,linewidth=3,label='retweet')
    plt.plot(x,co,linewidth=3,label='comment')
    plt.plot(x,li,linewidth=3,label='like')
    plt.yscale('log')
    plt.xticks(x, xtick)
    plt.legend()
    plt.savefig(savename)