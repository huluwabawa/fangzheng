import datetime
import random

import ddddocr
from PyRsa.pyb64 import Base64
from PyRsa.pyrsa import RsaKey
from lxml import etree

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62",

}
def getProxy():
    proxy_list=[]
    with open("./proxy.txt","r",encoding="utf-8") as fp:
        for item in fp:
            item = eval(item)
            proxy_list.append(item)
    if len(proxy_list)>0:
        Proxy = random.choice(proxy_list)
    else:
        Proxy=None
    return Proxy


def getPublicKey(session):
    today = datetime.datetime.now()  # 获取今天时间
    start_time = int(round(today.timestamp()*1000))
    end_time= int(round((today.timestamp()+100000)*1000))
    url="https://jwxt.stbu.edu.cn/xtgl/login_getPublicKey.html?time="+str(start_time)+"&_="+str(end_time)
    print(url)
    Proxy=getProxy()
    response=session.get(url=url,headers=headers,proxies=Proxy)
    obj =  response.json()
    return obj['modulus'],obj['exponent']


def ocrddd(session):
    today = datetime.datetime.now()  # 获取今天时间
    start_time = int(round(today.timestamp()*1000))
    url="https://jwxt.stbu.edu.cn/kaptcha?time="+str(start_time)
    Proxy=getProxy()
    response=session.get(url=url,headers=headers,proxies=Proxy)
    img=response.content
    orc=ddddocr.DdddOcr()
    res= orc.classification(img)
    print(res)
    return res
def jiami(modulus,exponent,psw ):
    rsakey = RsaKey()
    rsakey.set_public(Base64().b64tohex(modulus), Base64().b64tohex(exponent))
    en_psw = Base64().hex2b64(rsakey.rsa_encrypt(psw))
    return en_psw
def login(yhm,en_pwd,yzm,session):
    today = datetime.datetime.now()  # 获取今天时间
    start_time = int(round(today.timestamp() * 1000))
    url="https://jwxt.stbu.edu.cn/xtgl/login_slogin.html?time="+str(start_time)
    data={
            "csrftoken": "8f8a1149-c13c-48ff-a480-882cc9251325,8f8a1149c13c48ffa480882cc9251325",
            "language": "zh_CN",
            "yhm": yhm,
            "mm": en_pwd,
            "mm":en_pwd,
            "yzm": yzm
    }
    Proxy=getProxy()
    response=session.post(url=url,headers=headers,data=data,proxies=Proxy)
    html=response.content.decode('utf-8')
    tree=etree.HTML(html)
    dangerMsg=tree.xpath("//div[@id='home']/p[@id='tips']/text()")
    if len(dangerMsg) != 0:
        print("登录失败:"+str(dangerMsg[1]))
    else:
        print("登录成功")
        print(session.cookies)
        with open("cookies.txt","w",encoding="utf-8") as fp:
            for item in session.cookies:
                fp.write(item.name+"="+item.value+";")
import requests
def getSession():
    session = requests.session()
    today = datetime.datetime.now()  # 获取今天时间
    start_time = int(round(today.timestamp() * 1000))
    Proxy=getProxy()
    url="https://jwxt.stbu.edu.cn/xtgl/login_slogin.html?time="+str(start_time)
    requests.get(url=url,headers=headers,proxies=Proxy)
    return session
def start():
    # 1.准备session
    session = getSession()
    modulus, exponent = getPublicKey(session=session)
    yzm = ocrddd(session=session)
    username = input("请输入账号:")
    psw = input("请输入密码:")
    en_pwd = jiami(modulus, exponent, psw)
    login(yhm=username, en_pwd=en_pwd, yzm=yzm, session=session)


