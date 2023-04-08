import datetime

import requests

import login

Proxy = {
        'http': '182.131.17.19:80'
    }
def getCookie():
    with open("cookies.txt") as fp:
        content=fp.read()
        cookie=content[:-1]
    return cookie
def getGrade():
    # 获取成绩
    today = datetime.datetime.now()  # 获取今天时间
    start_time = int(round(today.timestamp() * 1000))
    print("===获取成绩===")
    url="https://jwxt.stbu.edu.cn/cjcx/cjcx_cxXsgrcj.html?doType=query"
    data={
    "xnm": "2021", #起始年份
    "xqm": "", # 第一学期 值3 第二学期值 12 全部 不填
    "_search": "false",
    "nd": start_time,
    "queryModel.showCount": "15",
    "queryModel.currentPage": "1",
    "queryModel.sortName": "",
    "queryModel.sortOrder": "asc",
    "time": "1"
}
    cookie=getCookie()
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62",
        "cookie":cookie
    }

    response=requests.post(url=url,data=data,headers=headers,proxies=Proxy)
    js=response.json()
    courseList=js["items"]
    kcCourse=0
    kcCount=0
    ksCourse=0
    ksCount=0
    for item in courseList:
        if 'khfsmc' in item:
            print(item["cj"],item["kcmc"],item["khfsmc"])
            if(item["khfsmc"]=="考试"):
                ksCourse+=int(item["cj"])
                ksCount+=1
            else:
                kcCourse += int(item["cj"])
                kcCount+=1
    print("考试课总成绩："+str(ksCourse))
    print("考查课总成绩:"+str(kcCourse))
    print("考试课平均成绩:"+str(ksCourse/ksCount))
    print("考查课平均成绩:"+str(kcCourse/kcCount))
    scores=(ksCourse/ksCount)*0.7+(kcCourse/kcCount)*0.3
    print("智育素质得分:"+str(scores))

#判断cookie是否可用
def cookieIsAvailable():
    today = datetime.datetime.now()  # 获取今天时间
    start_time = int(round(today.timestamp() * 1000))
    url="https://jwxt.stbu.edu.cn/xtgl/index_initMenu.html?jsdm=&_t="+str(start_time)
    cookie = getCookie()

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62",
        "cookie": cookie
    }
    response=requests.get(url=url,headers=headers,proxies=Proxy)
    if url==response.url:
        print("cookie有效")
        return True
    else:
        print("cookie失效请重新登录")
        return  False
# def getClassTable():
#     print("===获取课表====")
#     url="https://jwxt.stbu.edu.cn/kbcx/xskbcx_cxXsgrkb.html?gnmkdm=N2151&su=2020109005"
#     data={
#         "xnm":"2022",
#         "xqm":"12",
#         "kzlx": "ck",
#         "xsdm":""
#     }
#     response=session.post(url=url,headers=headers,data=data,proxies=Proxy)
#     obj = response.content.decode('utf-8')
#     print(obj)
def start():
    flag = cookieIsAvailable()
    if flag:
        getGrade()
    else:
        op = input("y/n:")
        if (op == "n"):
            exit()
        else:
            login.start()