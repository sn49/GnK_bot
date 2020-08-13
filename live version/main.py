# -*- coding: utf-8 -*- 

import sys
import os.path
import discord
from discord.ext import commands,tasks
from discord.utils import get
import random
import math
import time
import asyncio
import string
import pymysql
import hashlib
from urllib.request import urlopen
from bs4 import BeautifulSoup   
import re
import datetime
from pytz import timezone
import threading
import schedule

#region setting

version="V1.3"

members=[]


def connectsql(commit) :
    myhost="35.202.81.62"
    myuser="root"
    mypsw="fbmkkrvKHwkz4L5c"
    mydb="gnkscore"
    mycommit=commit
    return pymysql.connect(host=myhost,user=myuser,password=mypsw,database=mydb,autocommit=mycommit)

con = connectsql(True)
cur=con.cursor()
sql="select * from user_info;"
cur.execute(sql)
datas=cur.fetchall()
con.close()
for data in datas : 
    members.append(data[7])

bot = commands.Bot(command_prefix='GnK')
token = "NjYxMTc5OTgzNzAzNTcyNDkx.Xp5u9Q.ciODDc8YvlAfXS8CjW4ni6lyaHQ"
test_token="NzE1NDUwNzA4NTIyMTcyNTI3.Xs9ZZQ.sznKUWaeJ8fPTytNKM-g6LJuEXc"

mapnormal = 'WKC 코리아 서킷,쥐라기 공룡 무덤,브로디 비밀의 연구소,월드 뉴욕 대질주,쥐라기 공룡 결투장,월드 두바이 다운타운,사막 놀라운 공룡 유적지,신화 신들의 세계,비치 해변 드라이브,빌리지 고가의 질주,WKC 싱가폴 마리나 서킷,WKC 상해 서킷,월드 리오 다운힐,빌리지 익스트림 경기장,빌리지 남산,어비스 운명의 갈림길'

maphard='월드 이탈리아 피사의 사탑,WKC 브라질 서킷,네모 산타의 비밀공간,네모 강철바위 용광로,도검 구름의 협곡,대저택 은밀한 지하실,차이나 골목길 대질주,차이나 서안 병마용,황금문명 오리엔트 황금 좌표,황금문명 비밀장치의 위협,해적 로비 절벽의 전투,빌리지 만리장성,어비스 바다 소용돌이,사막 빙글빙글 공사장,공동묘지 해골성 대탐험,카멜롯 펜드래건 캐슬,카멜롯 외곽 순찰로'

mapveryhard='노르테유 익스프레스,광산 3개의 지름길,광산 위험한 제련소,광산 꼬불꼬불 다운힐,동화 이상한 나라의 문,쥐라기 공룡섬 대모험,어비스 스카이라인,어비스 숨겨진 바닷길,문힐시티 숨겨진 지하터널,공동묘지 마왕의 초대,포레스트 지그재그,팩토리 미완성 5구역,빌리지 붐힐터널'

mapitem='동화 카드왕국의 미로,차이나 빙등 축제,빌리지 두개의 관문,네모 구구 둥지,빌리지 운하,신화 빛의 길,월드 리오 다운힐,쥐라기 아슬아슬 화산 점프,비치 여객선,대저택 루이의 서재,차이나 서안 병마용,차이나 상해 동방명주,노르테유 허공의 갈림길,광산 3개의 지름길,아이스 신나는 하프파이프,사막 피라미드 탐험,포레스트 통나무,포레스트 골짜기,카멜롯 기사단 훈련장'

mapall=[]

for i in mapnormal.split(',') : 
    mapall.append(i)

for i in maphard.split(',') : 
    mapall.append(i)

for i in mapveryhard.split(',') : 
    mapall.append(i)

#endregion




@bot.event
async def on_message(ctx) :
    role = discord.utils.find(lambda r: r.name == 'Muted',ctx.guild.roles)
    tester = discord.utils.find(lambda r: r.name == '테스터',ctx.guild.roles)
    if role in ctx.author.roles :
        t1=ctx.author.id
        con=connectsql(True)
        cur=con.cursor()
        sql=f"update user_info set moa=moa-4000 where discorduserid={t1}"
        print(sql)
        cur.execute(sql)
        con.commit()
        await ctx.delete()
        await ctx.author.send(f'mute 상태에서 채팅을 쳐서 4000모아를 잃었습니다.')
        print(ctx.author.roles)
    if not tester in ctx.author.roles : 
        await bot.process_commands(ctx)
    else : 
        print("123456") 

@bot.event
async def on_ready():
    print("bot login test")
    print(bot.user.name)
    print(bot.user.id)
    print("-----------")
    await bot.change_presence(status=discord.Status.online,activity=discord.Game(f'GnK봇 {version}'))
    job_thread=threading.Thread(target=luckypang)
    job_thread.start()
    bot.loop.create_task(luckypang())

async def luckypang():
    nickname2=""
    discorduser=""
    money2=0
    end2=0
    channel=bot.get_channel(713050090486366380)
    while True : 
        timenow=datetime.datetime.now(timezone('Asia/Seoul'))
        timenow_str=str(timenow)
        if timenow_str[11:21]=="12:30:00.0" or timenow_str[11:21]=="18:30:00.0" or timenow_str[11:21]=="08:20:00.0" : 
            con=connectsql(False)
            cur=con.cursor()
            sql=f"select pangprice from betstat"
            cur.execute(sql)
            datas=cur.fetchall()
            getusers=[]
            for i in datas : 
                luckym=i[0]
            for i in range(30) :
                getusers.append(random.randrange(0,len(members)))
            getuser=random.choice(getusers)
            sql=f"select nickname,moa,discorduserid from user_info where indexid='{getuser+1}'"
            cur.execute(sql)
            datas=cur.fetchall()
            for i in datas :
                nickname2=i[0]
                money2=i[1]
                discorduser=i[2]    
            end2=money2+luckym
            sql=f"update user_info set moa={end2} where indexid={getuser+1}"
            sql2=f"update betstat set pangprice=0"
            cur.execute(sql)
            cur.execute(sql2)
            con.commit()
            user=bot.get_user(int(discorduser))
            await channel.send(str(nickname2)+"님이 럭키팡에 당첨되어 "+str(luckym)+"모아를 받았습니다!")
            await user.send(str(nickname2)+"님 축하합니다! 럭키팡에 당첨되어 "+str(luckym)+"모아를 받았습니다!")
            con.close()
        elif timenow_str[11:21]=="00:00:00.0" :
            con=connectsql(True)
            cur=con.cursor()
            sql="update gnkstore set amount=40 where itemid=101"
            cur.execute(sql)
            await channel.send("상점에 있는 의문의 물건 +1의 개수가 40개가 되었습니다.")
        await asyncio.sleep(0.1)

class Map:
    def __init__(self,mapnormal,maphard,mapveryhard,mapitem):
        self.normal = mapnormal.split(',')
        self.hard = maphard.split(',')
        self.veryhard = mapveryhard.split(',')
        self.mapall=[]
        self.mapitem=mapitem.split(',')

        for i in self.normal:
            self.mapall.append(i)
        for i in self.hard :
            self.mapall.append(i)
        for i in self.veryhard:
            self.mapall.append(i)

    def getAllMap(self):
        return self.mapall

    def get_data(self,mode) :
        if self.mode==1 : 
            data= random.sample(self.normal,self.amount)
        elif self.mode==2 : 
            data= random.sample(self.hard,self.amount)
        elif self.mode==3 : 
            data= random.sample(self.veryhard,self.amount)
        elif self.mode==4 :
            data= random.sample(self.mapall,self.amount)
        elif self.mode==5 : 
            data=random.sample(self.mapitem,self.amount)
        else :
            data="1:노멀 2:하드 3:베리하드 4:전체(1~3) 5:아이템"
        return data

    def getmap(self,mode,amount=5) : 
        self.mode=list(mode)
        self.mode=self.mode[0]
        print(self.mode)
        result=[]
        data=[]
        printing=""
        self.amount=list(amount)
        self.amount=self.amount[0]
        data=self.get_data(self.mode)
        if data is list :
            for i in data : 
                printing+=(i+'\n')
            return f"```{printing}```"
        else :
            return data

maps=Map(mapnormal,maphard,mapveryhard,mapitem)

@bot.command()
async def 안녕(ctx): await ctx.send("안녕")

@bot.command()
async def 맵추첨(ctx,mode,amount) :
    await ctx.send(f"{maps.getmap({int(mode)},{int(amount)})}")

async def all_list(ctx,mode) : 
    if mode==1 : 
        await ctx.send(("```"+mapnormal.replace(",","\n")+"```"))
    elif mode==2 : 
        await ctx.send("```"+maphard.replace(",","\n")+"```")
    elif mode==3 : 
        await ctx.send("```"+mapveryhard.replace(",","\n")+"```")
    elif mode==4 :
        data=""
        for i in mapall : 
            data=data+i+"\n"
        await ctx.send('```'+data+'```')
    else :
        await ctx.send("```"+mapitem.replace(",","\n")+"```")

@bot.command()
async def 리스트(ctx,mode=None):
    if int(mode)>0 and int(mode)<=5 :
        all_list(ctx,int(mode))
    else :
        await ctx.send("1:노멀 2:하드 3:베리하드 4:전체(1~3) 5:아이템") 

@bot.command()
async def 버전(ctx):
    await ctx.send(version)

@bot.command()
async def 킹오hi(ctx): await ctx.send("킹오야 안녕")

@bot.command()
async def 욕해줘(ctx): await ctx.send("ㅅㅂ")

@bot.command()
async def 아잉련아(ctx): await ctx.send("?????????")

@bot.command()
async def 새벽(ctx): await ctx.send("에도 켜져있음")

@commands.cooldown(1, 5, commands.BucketType.default)
@bot.command()
async def 가입(ctx,nickname=None) : 
    nicknames=[]
    con=pymysql.connect(host="35.202.81.62",user="root",password="fbmkkrvKHwkz4L5c",database="gnkscore",autocommit=True)
    cur=con.cursor()
    if len(nickname)>3 and len(nickname)<11 : 
        if not ctx.author.id in members : 
            string_pool=string.ascii_letters+string.digits
            result1=""
            for i in range(20) : 
                result1=result1+random.choice(string_pool)
            num_user=0
            sql="select * from count_user;"
            sql2="insert into user_info (indexid,nickname,discorduserid,login_string) values (%s,%s,%s,%s)"
            sql3="select nickname from user_info;"
            sql4=f"update count_user set num_user = num_user+1"
            cur.execute(sql)
            datas=cur.fetchall()
            for data in datas :
                num_user=data[0]
            cur.execute(sql3)
            datas=cur.fetchall()
            nicks=str(nickname).lower()
            for data in datas : 
                temp=str(data[0]).lower()
                nicknames.append(temp)
            if not nickname in nicknames : 
                salt="R9Wf2PN%qk9!Jn*Sd$PeB10iJ"
                hasing=hashlib.sha512()
                hasing.digest()
                result=hashlib.sha512((result1+salt).encode('utf-8')).hexdigest()
                val = (str(num_user+1),str(nickname),str(ctx.author.id),str(result))
                cur.execute(sql2,val)
                cur.execute(sql4)
                con.close()
                members.append(ctx.author.id)
                await ctx.author.send(f"가입 성공! 당신의 로그인 문자열은 {result1}입니다.")
            else : 
                await ctx.author.send("사용할수 없는 닉네임입니다.")
        else :
            await ctx.author.send("이미 가입이 되어 있습니다.")
    else : 
        await ctx.author.send("닉네임 제한 4~10, 한글3 영어1")


@commands.cooldown(1, 1, commands.BucketType.default)
@bot.command()
async def 모아(ctx,nickname=None) : 
    con=connectsql(False)
    cur=con.cursor()
    nick=""
    money=0
    if nickname==None : 
        t1 = ctx.author.id
        sql=f"select nickname,moa from user_info where discorduserid='{t1}'"
        cur.execute(sql)
        datas=cur.fetchall()
        for i in datas : 
            nick=i[0]
            money=i[1]
        await ctx.author.send(f'{nick}님의 모아는 {money}모아 입니다.')
    else : 
        sql=f"select moa from user_info where nickname='{nickname}'"
        cur.execute(sql)
        data = cur.fetchall()
        for i in data :
            money=i[0]
        await ctx.send(f'{nickname} 님의 모아는 {money}모아 입니다.')
    con.close()

def get_chance_multiple(mode) :
    if mode==1 : 
        chance=80
        multiple=1.2
    if mode==2 : 
        chance=64
        multiple=1.6
    if mode==3 : 
        chance=48
        multiple=2.2
    if mode==4 : 
        chance=32
        multiple=3
    if mode==5 : 
        chance=16
        multiple=4       
    return chance,multiple

def get_stats1(stat,money,moa) :
    if money>=10000000 : 
        return_stat=int(stat)+math.floor(moa*0.6)
    elif money>=5000000 :
        return_stat=int(stat)+math.floor(moa*0.35)
    elif money>=4000000 : 
        return_stat=int(stat)+math.floor(moa*0.3)
    elif money>=3000000 : 
        return_stat=int(stat)+math.floor(moa*0.25)
    elif money>=2000000 : 
        return_stat=int(stat)+math.floor(moa*0.2)
    elif money>=1000000 : 
        return_stat=int(stat)+math.floor(moa*0.15)
    elif money>=500000 : 
        return_stat=int(stat)+math.floor(moa*0.1)
    else : 
        return_stat=int(stat)+math.floor(moa*0.05)
    return return_stat


@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command()
async def 베팅(ctx,moa=None,mode=None,repeat=None) :
    if repeat==None : 
        repeat=1
    if int(repeat)<=10 and int(repeat)>0 : 
        total_profit,start=0,0
        stats=[]
        for num in range(int(repeat)) : 
            con = connectsql(True)
            cur=con.cursor()
            sql=f"select * from betstat"
            cur.execute(sql)
            datas=cur.fetchall()
            for i in datas : 
                stats.append(i[0])
                stats.append(i[1])
            role = discord.utils.find(lambda r: r.name == 'Muted',ctx.guild.roles)
            if not role in ctx.author.roles :
                end,lose,chance,profit,money,multiple=0,0,0,0,0,0
                t1 = ctx.author.id
                nick=""
                sql=f"select nickname,moa from user_info where discorduserid='{t1}'"
                cur.execute(sql)
                datas = cur.fetchall()
                for i in datas : 
                    nick=i[0]
                    money=i[1]
                    if num==0 : 
                        start=i[1]
                if money<int(moa) or int(moa)<0 : 
                    await ctx.author.send(nick+"님 보유량보다 많거나 0원 미만으로 베팅하실 수 없습니다.")
                    return
                elif moa==None : 
                    await ctx.author.send("GnK베팅 거실돈 모드\n(모드 종류 : 1 80% 1.4배, 2 64% 1.8배, 3 48% 2.2배, 4 32% 2.6배, 5 16% 3배)")
                    return
                else :
                    lose=int(moa)
                    chance,multiple=get_chance_multiple(int(mode))      
                if int(mode)<6 and int(mode)>0 : 
                    result=random.randrange(0,100)
                    if result<chance : 
                        profit=math.floor(multiple*int(moa))
                        end=money-lose+profit
                        total_profit=total_profit-lose+profit
                        sql=f"update user_info set moa={end} where discorduserid='{t1}'"
                        sql3=f"insert into userbetstat (nickname,moa,mode,result) values ('{nick}',{int(moa)},{int(mode)},'success')"
                        cur.execute(sql)
                        cur.execute(sql3)                   
                    else :
                        total_profit=total_profit-lose
                        end=money-lose
                        stats[0]=int(stats[0])+1
                        stats[1]=get_stats1(int(stats[1]),money,int(moa))
                        sql2=f"update user_info set moa={end} where discorduserid='{t1}'"
                        sql=f"update betstat set betcount=betcount+1, pangprice='{stats[1]}'"
                        sql3=f"insert into userbetstat (nickname,moa,mode,result) values ('{nick}',{int(moa)},{int(mode)},'fail')"
                        cur.execute(sql)
                        cur.execute(sql2)
                        cur.execute(sql3)
                        if stats[0]<=700 : 
                            await ctx.send(str(stats[0])+"번째 실패")
                        else : 
                            await ctx.send("700회를 넘겨서 실패 횟수를 알려주지 않습니다.")
                    if stats[0]>=1000 : 
                        stats[0]=0
                        sql=f"update user_info set moa=moa+100000 where discorduserid='{t1}'"
                        cur.execute(sql)
                        await ctx.send(f"총 1000번째로 실패하여 {nick}님이 100000모아를 받았습니다! 다시 0회부터 시작합니다.")
                    sql=f"update betstat set betcount={stats[0]}, pangprice={stats[1]}"
                    cur.execute(sql)
                else : 
                    await ctx.author.send("모드를 선택해주세요. 1 80% 1.2배, 2 64% 1.6배, 3 48% 2.2배, 4 32% 3배, 5 16% 4배")
                    break
            else : 
                ctx.author.send("구걸 상태라 베팅을 할 수 없습니다.")
                break
    else : 
        await ctx.author.send("1~10회만 반복 가능합니다.")
    con.close()
    if total_profit>=0 :
        await ctx.author.send(f"{nick}님 {str(start)}모아에서 {str(start+total_profit)}모아가 되었습니다. {total_profit}모아를 벌었습니다!")
    else : 
        await ctx.author.send(f"{nick}님 {str(start)}모아에서 {str(start+total_profit)}모아가 되었습니다. {total_profit}모아를 잃으셨습니다...")

@bot.command()
async def 구걸(ctx) : 
    role = discord.utils.find(lambda r: r.name == 'Muted',ctx.guild.roles)
    con=connectsql(False)
    cur=con.cursor()
    if not role in ctx.author.roles :
        hour=7
        minute,second,money,end=0,0,0,0
        nick=""
        t1 = ctx.author.id
        sql=f"update user_info set moa=moa+30000 where discorduserid='{t1}'"
        sql2=f"select nickname from user_info where discorduserid={t1}"
        cur.execute(sql2)
        datas=cur.fetchall()
        for i in datas : 
            nick=i[0]
        cur.execute(sql)
        con.commit()
        member = ctx.message.author
        await member.add_roles(get(ctx.guild.roles,name="Muted"))
        await ctx.send(f'{nick}님이 구걸 하기 위해 {hour}시간 {minute}분 {second}초 뮤트 되어 30000모아를 지급하였습니다. 뮤트상태에서 채팅을 치면 4000모아를 뺏깁니다.')
        end=money+30000
        await asyncio.sleep(hour*60*60+minute*60+second)
        await member.remove_roles(get(ctx.guild.roles,name="Muted"))
    else : 
        await ctx.author.send("이미 구걸 중입니다.")
    con.close()

@commands.cooldown(1, 5, commands.BucketType.default)
@bot.command()
async def 기부(ctx,nickname2=None,moa=None) : 
    con=connectsql(False)
    cur=con.cursor()
    role = discord.utils.find(lambda r: r.name == 'Muted',ctx.guild.roles) 
    if not role in ctx.author.roles :
        end,money1,money2,user=0,0,0,0
        nickname1=""
        t1 = ctx.author.id
        sql=f"select moa,nickname from user_info where discorduserid={t1}"
        sql4=f"select discorduserid,nickname from user_info where nickname='{str(nickname2)}'"
        cur.execute(sql)
        datas=cur.fetchone()
        money1=datas[0]
        nickname1=datas[1]
        cur.execute(sql4)
        datas=cur.fetchone()
        user=bot.get_user(int(datas[0]))
        nickname2=datas[1]
        sql2=f"update user_info set moa=moa-{moa} where discorduserid={t1}"
        sql3=f"update user_info set moa=moa+truncate({moa}*0.9,0) where nickname='{str(nickname2)}'"
        if money1<int(moa) or int(moa)<0 : 
            await ctx.author.send(nickname1+"님 보유량보다 많거나 0원 미만으로 기부할수 없습니다.")
            return
        elif nickname1==str(nickname2) : 
            await ctx.author.send("자기 자신한테 기부할수 없습니다.")
        elif moa==None : 
            await ctx.author.send("기부할 돈을 입력해주세요.")
            return
        else :          
            cur.execute(sql2)
            cur.execute(sql3)
            con.commit()
            end=money2+math.floor(int(moa)*0.9)
            await user.send(f'{nickname1}님이 {moa}모아를 기부하셔서 수수료 10%를 뺀 {money2}모아에서 {end}모아가 되었습니다!')
            await ctx.author.send(f"{nickname1}님, {nickname2}님에게 {moa}모아를 기부해서 {money1}모아에서 {money1-int(moa)}모아가 되었습니다!")                         
    else : 
        ctx.author.send("구걸 상태라 기부 할 수 없습니다.")


@bot.command()
async def 상점(ctx,item=None) : 
    con = connectsql(False)
    cur=con.cursor()
    count=0
    have=0
    end=0
    money=0
    need=0
    amount=0
    nickname=""
    name=""
    if item==None : 
        sql=f"select * from gnkstore"
        cur.execute(sql)
        datas=cur.fetchall()
        for i in datas : 
            count=count+1
            await ctx.send(f"{i[0]}    {i[1]}    {i[2]}모아  남은 개수 : {i[3]}")
        con.close()
    elif int(item)>=1 or int(item)<=count : 
        nickname=""
        sql=f"select name,price,amount from gnkstore where itemid={int(item)}"
        cur.execute(sql)
        datas=cur.fetchall()
        for i in datas : 
            name=i[0]
            need=i[1]
            amount=i[2]
        if int(amount)<0 :
            await ctx.author.send(f"{name}은 매진되었습니다.")
            return
        if int(item)>100 :
            sql=f"select nickname,moa,unknown_level,discorduserid from user_info where discorduserid={ctx.author.id}"
        else : 
            sql=f"select nickname,moa,item{int(item)},discorduserid from user_info where discorduserid={ctx.author.id}"
        cur.execute(sql)
        datas = cur.fetchall()
        for i in datas : 
            nickname=i[0]
            money=i[1]
            have=i[2]
        if money>=int(need) : 
            if int(item)>100 : 
                c_reinforce=0
                sql=f"select unknown_level from user_info where discorduserid={ctx.author.id}"
                cur.execute(sql)
                data=cur.fetchone()
                c_reinforce=int(data[0])
                if(c_reinforce>0) :
                    await ctx.author.send(f"의문의 물건은 1개만 구입할수 있습니다.")
                    return
                sql=f"update user_info set unknown_level = {int(item)-100}, moa=moa-{int(need)} where discorduserid={ctx.author.id}"
                sql2=f"update gnkstore set amount=amount-1 where itemid='{int(item)}'"
            else :
                sql=f"update user_info set item{int(item)} = item{int(item)}+1, moa=moa-{int(need)} where discorduserid={ctx.author.id}"
                sql2=f"update gnkstore set amount=amount-1 where itemid='{int(item)}'"
            cur.execute(sql)
            cur.execute(sql2)
            await ctx.author.send(f"{name}을 구입하는데 성공했습니다!")
            if int(item)>100 :
                await ctx.send(f"{nickname}님이 {name}을 구입하였습니다!")
            else :
                await ctx.send(f"{nickname}님이 {name}을 구입하였습니다! 현재 {nickname}님의 보유 개수는 {have+1}개 입니다.")
        else : 
            await ctx.author.send(f"모아가 부족합니다!")
    con.commit()
    con.close()



@commands.cooldown(1, 2, commands.BucketType.default)
@bot.command()
async def 럭키팡(ctx) : 
    con = pymysql.connect(host="35.202.81.62",user="root",password="fbmkkrvKHwkz4L5c",database="gnkscore")
    cur=con.cursor()
    sql=f"select pangprice from betstat"
    cur.execute(sql)
    datas = cur.fetchall()
    for i in datas : 
        moa=i[0]
    await ctx.send(f"누적 모아 : {moa}")


@bot.command()
async def 리그에결(ctx) : 
    ace=[]
    webpage=urlopen("http://gin7174.dothome.co.kr/recommand1v1.html")
    soup=BeautifulSoup(webpage,"html.parser")
    div=soup.find_all('a')
    print(div)
    for i in div : 
        ace.append(f"{i['href']}   {re.sub('<.+?>','',str(i),0).strip()}")
    await ctx.send(random.choice(ace))

@bot.command()
async def 경제규모(ctx) : 
    economy=0
    con=pymysql.connect(host="35.202.81.62",user="root",password="fbmkkrvKHwkz4L5c",database="gnkscore",autocommit=True)
    cur=con.cursor()
    sql=f"select sum(moa) from user_info;"
    cur.execute(sql)
    datas= cur.fetchall()
    for i in datas : 
        economy=i[0]
    await ctx.send(f"현재 GnK경제규모는 {economy}모아입니다!")
        
@bot.command()
async def 문의(ctx):
    count=0
    nickname=""
    con=connectsql(False)
    cur=con.cursor()
    sql = f"select count(*) from gnkquestion"
    cur.execute(sql)
    datas=cur.fetchone()
    print(datas)
    for i in datas :
        count=i+1
    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True,send_messages=True),
    }
    sql=f"select nickname from user_info where discorduserid='{ctx.author.id}'"
    sql2=f"insert into gnkquestion values('{count}','{nickname}')"
    await guild.create_role(name="문의 "+str(count))
    cate = discord.utils.get(guild.categories,name="문의")
    server = ctx.guild
    user = ctx.message.author
    channel = await guild.create_text_channel("문의 "+str(count), overwrites=overwrites,category=cate)
    owner = bot.get_user(382938103435886592) 
    cur.execute(sql)
    datas=cur.fetchone()
    for i in datas : 
        nickname=i
    cur.execute(sql2)
    con.commit()
    con.close()
    await owner.send("문의가 들어왔습니다!")
    await ctx.author.send("문의-"+str(count)+" 게시판이 만들어졌습니다! 이 게시판에서 문의를 해주세요!")

@bot.command()
async def 재발급(ctx) : 
    salt="R9Wf2PN%qk9!Jn*Sd$PeB10iJ"
    con=pymysql.connect(host="35.202.81.62",user="root",password="fbmkkrvKHwkz4L5c",database="gnkscore")
    cur=con.cursor()
    t1 = ctx.author.id
    string_pool=string.ascii_letters+string.digits
    result1=""
    for i in range(20) : 
        result1=result1+random.choice(string_pool)
    hasing=hashlib.sha512()
    hasing.digest()
    result=hashlib.sha512((result1+salt).encode('utf-8')).hexdigest()
    sql=f"update user_info set login_string='{result}' where discorduserid='{t1}'"
    cur.execute(sql)
    con.commit()
    con.close()
    await ctx.author.send(f"재발급 된 로그인 문자열은 {result1}입니다.")

@bot.command()
async def 점수(ctx,nick=None) : 
    score=0
    con=pymysql.connect(host="35.202.81.62",user="root",password="fbmkkrvKHwkz4L5c",database="gnkscore")
    cur=con.cursor()
    if nick==None : 
        sql=f"select score from user_info where discorduserid={ctx.author.id}"
        cur.execute(sql)
        datas=cur.fetchall()
        for i in datas : 
            score=i[0]
        await ctx.author.send(f"당신의 GnK내전 점수는 {score}점 입니다.")
    else : 
        sql=f"select score from user_info where nickname='{nick}'"
        cur.execute(sql)
        datas=cur.fetchall()
        for i in datas : 
            score=i[0]
            await ctx.send(f"{nick}의 GnK내전 점수는 {score}점 입니다.")
    con.close()

def get_fail(level):
    temp=0
    for i in range(level) :
        if i==0:
            temp=0
        else :
            temp+=0.1*i

    return temp

def get_need(level):
    temp=[0,0,0,0,0,0]
    temp2=0
    for i in range(level):
        if i<3 :
            temp[i]=1
            temp2=1
        elif i<6 :
            temp[i]=2
            temp2=2
        else :
            temp2=sum(temp)
            temp[0]=temp[1]
            temp[1]=temp[2]
            temp[2]=temp[3]
            temp[3]=temp[4]
            temp[4]=temp[5]
            temp[5]=temp2
    return temp2
        
@commands.cooldown(1, 5, commands.BucketType.default)
@bot.command()
async def 판매(ctx) :
    level=0
    before=0
    after=0
    change=0
    con=connectsql(True)
    cur=con.cursor()
    sql=f"select moa,unknown_level,nickname from user_info where discorduserid={ctx.author.id}"
    cur.execute(sql)
    data=cur.fetchone()
    before=int(data[0])
    level=int(data[1])
    nickname=str(data[2])

    pricebuy,pricesell=get_price(level)

    if level<1 :
        await ctx.author.send(f"의문의 물건을 판매할 수 없거나 가지고 있지 않습니다.")
        return

    

    sql=f"update user_info set moa=moa+{pricesell}, unknown_level=0 where discorduserid={ctx.author.id}"
    cur.execute(sql)

    if level==30 :
        order=0
        file="complete_30_list.txt"
        sql=f"update user_info set complete30=complete30+1 where discorduserid={ctx.author.id}"
        cur.execute(sql)
        if not os.path.isfile(file) :
            order=0
            f=open(file,"w")
            timenow=datetime.datetime.now(timezone('Asia/Seoul'))
            timenow_str=str(timenow)
            f.write(f"{'%03d'%order}   {'%13s'%nickname}    {timenow_str[0:21]}\n")
            f.close()
        else :
            f=open(file,"r")
            order=len(f.readlines())
            f.close()
            f=open(file,"a")
            f.write(f"{'%03d'%order}   {'%13s'%nickname}    {timenow_str[0:21]}\n")
            f.close()
        await ctx.send(f"{nickname}님이 의문의 물건 +30을 판매해 {order}번째로 명예의 전당에 오르게 되었습니다.")
        return

    sql=f"select EXISTS (select * from gnkstore where itemid={1}{'%02d'%level}) as success"
    cur.execute(sql)
    data=cur.fetchone()
    print(sql)
    print(data)
    success=int(data[0])
    if success==0 :
        sql=f"insert into gnkstore values ({1}{'%02d'%level},'의문의 물건 +{level}',{pricebuy},1)"
    else :
        sql=f"update gnkstore set amount=amount+1 where itemid={1}{'%02d'%level}"
    print(sql)
    cur.execute(sql)
    con.close()
    await ctx.send(f"의문의 물건 +{level}이 판매되었습니다.")


def get_price(level) :
    temp=[0,0,0,0]
    temp_buy=0
    temp_sell=0
    for i in range(level) :
        if i<4 :
            temp[i]=i+1
            temp_sell=i+1
        else :
            temp_sell=sum(temp)
            temp[0]=temp[1]
            temp[1]=temp[2]
            temp[2]=temp[3]
            temp[3]=temp_sell
    for i in range(level) :
        if i<4 :
            temp[i]=i+2
            temp_buy=i+2
        else :
            temp_buy=sum(temp)
            temp[0]=temp[1]
            temp[1]=temp[2]
            temp[2]=temp[3]
            temp[3]=temp_buy
    return temp_buy,temp_sell




@bot.command()
async def 강화(ctx) :
    con=connectsql(True)
    cur=con.cursor()
    level = 1
    cri_success=0.0
    success=0.0
    not_change=0.0
    fail=0.0
    destroy=0.0
    result=0.0
    change=0

    sql=f"select moa,unknown_level from user_info where discorduserid={ctx.author.id}"
    cur.execute(sql)
    data=cur.fetchone()
    print(data)
    moa=int(data[0])
    level=int(data[1])

    need=get_need(level)
    if need>moa :
        ctx.author.send(f"{need-moa}모아가 부족합니다.")
    if level == 30 :
        await ctx.author.send("이미 의문의 물건 +30을 가지고 있습니다.")
        return
    elif level == 0 :
        await ctx.author.send("의문의 물건을 가지고 있지 않습니다.")
        return

    if level !=29 :
        cri_success=0.05*(30-level)
    else :
        cri_success=0.0

    if level==1 :
        destroy=0.0
    else :
        destroy=0.73*(level-29)+20

    success=100-3.2*level
    fail=get_fail(level)

    not_change=100 - cri_success - success - fail - destroy

    result=random.random()*100

    print(result)

    if result<cri_success :
        print(f"{result}  {cri_success}")
        change=2        
    elif result<cri_success + success :
        print(f"{result}  {cri_success+success}")
        change=1
    elif result<cri_success+success + not_change :
        print(f"{result}  {cri_success+success+ not_change}")
        change=0
    elif result < cri_success + success + not_change + fail :
        print(f"{result}  {cri_success+success+ not_change+ fail}")
        change=-1
    else :
        change=-10
    
    print(change)

    if change!=-10 :
        sql=f"update user_info set unknown_level=unknown_level+{change},moa=moa-{need} where discorduserid={ctx.author.id}"
        if change>0 :
            await ctx.send(f"강화 레벨 {level}에서 {change} 상승! 현재 레벨 : {level+change}")
        elif change<0 :
            await ctx.send(f"강화 레벨 {level}에서 {-change} 감소! 현재 레벨 : {level+change}")
        else :
            await ctx.send(f"강화 레벨 {level}에서 변동 없음! 현재 레벨 : {level}")      
    else :
        sql=f"update user_info set unknown_level=0,moa=moa-{need} where discorduserid={ctx.author.id}"
        await ctx.send(f"의문의 물건 +{level} 파괴...")
    
    cur.execute(sql)
    con.close()


@bot.command()
async def 내전(ctx) : 
    webpage=urlopen("http://gin7174.dothome.co.kr/inclubgame.html")
    soup=BeautifulSoup(webpage,"html.parser")
    div=str(soup.find('div'))
    div=re.sub('<.+?>','',div,0).strip()
    await ctx.send(div)



bot.run(token)