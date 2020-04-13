import requests 
import demjson
from lxml.html import fromstring
import re

#所有参数必须为str

USER_AGENT = r"Mozilla/5.0 (Linux; Android 5.1.1; Generic Android-x86 Build/LMY48Z) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Safari/537.36 safetreeapp/1.5.1"



def login(username,password):
    """
        此函数用于登录安全教育平台并返回userid等用户信息,
        返回类型为字典.
    """
    LOGIN_URL = r"http://appapi.safetree.com.cn/usercenter/api/v1/account/PostLogin"
    header = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Connection": "Keep-Alive",
        "Content-Type":"application/json"
    }
    data ={
        "Username": username,
        "Password": password
    }
    resp = requests.post(LOGIN_URL,data=demjson.encode(data),headers=header)
    User_information = demjson.decode(resp.text)
    return User_information


def get_homework_list(cityid,classroom,grade):
    """
        此函数将返回一个有所有作业详细信息字典的列表，
    """
    GET_HOMEWORK_URL = "https://qingdao.xueanquan.com/webapi/jt/MyHomeWork.html"
    data = {
        "grade": grade,
        "classroom": classroom,
        "cityid": cityid
    }
    _ = requests.get(GET_HOMEWORK_URL,data=data).content.decode()
    tree = fromstring(_)
    #获取作业数量
    _ = len(tree.xpath(r'//*[@id="mun_-1_1"]/tr'))
    homeworks = []
    for index in range(1,_+1):
        homework = {}
        HomeworkJsCommand = tree.xpath(rf'//*[@id="mun_-1_1"]/tr[{index}]/td[7]/a/@onclick')[0]
        HomeworkJsCommand = HomeworkJsCommand[HomeworkJsCommand.index('(')+1:HomeworkJsCommand.index(')')]
        #跳过活动项目
        _ = tree.xpath(rf'//*[@id="mun_-1_1"]/tr[{index}]/td[2]/div/a/text()')[0]
        if "https://huodong.xueanquan.com" in HomeworkJsCommand:
            continue
        if "活动" in _:
            continue
        homework["Name"] = _
        #添加作业的li和gid属性
        _ = HomeworkJsCommand.split(",")
        homework["li"] = _[0].strip()
        homework["gid"] = _[3].strip()
        _ = tree.xpath(rf'//*[@id="mun_-1_1"]/tr[{index}]/td[7]/a/@name')[0]
        homework["workId"] = _[_.index("_")+1:]
        _ = rf"https://qingdao.xueanquan.com/JiaTing/EscapeSkill/SeeVideo.aspx\?gid={homework['gid']}&li={homework['li']}"
        homework["url"] = _
        homeworks.append(homework)
    return homeworks


def finish_homework(workid,gid,li,accessCookie):
    """
        此函数用于完成指定学生的指定作业。(未验证)
    """
    URL = r"http://shandong.safetree.com.cn/CommonService.asmx/TemplateIn2"

    data = {
        "workid":workid,
        "fid":gid,
        "title":"",
        "require":"",
        "purpose":"",
        "contents":"",
        "testwanser":"0|0|0",
        "testinfo":"已掌握技能",
        "testMark":"100",
        "testReulst":"1",
        "SiteName":"",
        "SiteAddrees":"",
        "WatchTime":"",
        "CourseID":li
    }

    cookies = {
        "UserID":accessCookie,
    }

    _ = requests.get(URL,data=data,cookies = cookies).content.decode()
    return True


def get_safetips(accessToken,accessCookie ,pagesize,plainUserId):
    """
        This function will return a dictionary with the safety reminder of the input student,
        the content has the safety reminder URL, name, etc.
    """
    accessCookie = str(accessCookie)
    request_header = {
        "User-Agent": USER_AGENT,
        "Authorization": "Bearer " + accessToken,
        "X-UserId": str(plainUserId)
    }
    data = {
        "userId":accessCookie,
        "parentSortId":"2",
        "beginIndex":"0",
        "pageSize":pagesize
    }
    login_url = r"http://shandong.safetree.com.cn/safeapph5/api/noticeService/getMyReceive"
    resp = requests.get(login_url,data=data,headers=request_header)
    json = demjson.decode(resp.content.decode())
    return json


def read_safetips(tipurl,accessToken,accessCookie):
    """
        此函数用于自动阅读安全提醒
    """
    noticeId = tipurl[tipurl.index("result=")+7:tipurl.index("&host")]
    url = r"https://qingdao.safetree.com.cn/safeapph5/api/notice/getByIdNoticeMessageDetails"
    data = {
        "id":noticeId,
        "messageRead":"true"
    }
    headers = {
        "User-Agent":USER_AGENT,
        "X-UserId":accessCookie,
        "Authorization":"Bearer "+accessToken
    }
    resp = requests.get(url, headers=headers, data=data)
    return demjson.decode(resp.content.decode())
