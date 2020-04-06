import requests
import demjson
from lxml.html import fromstring

"""This module is a safety education platform SDK packaged using the mobile version of the safety education platform Api"""

USER_AGENT = r'Mozilla/5.0 (Linux; Android 5.1.1; Generic Android-x86 Build/LMY48Z) ' \
             r'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Safari' \
             r'/537.36 safetreeapp/1.5.1'


class LoginError(Exception):
    """This Error will raise when user can't login"""
    def __init__(self):
        Exception.__init__(self, "Wrong username or password")


class GetHomeWorkError(Exception):
    """This Error will raise when can't get user's homework"""
    def __init__(self, data):
        super().__init__(self, data)
        self.data = data

    def __str__(self):
        return " UserId: " + self.data + "-> Can't get this user's Homework"


class HomeworkError(Exception):
    """This Error will raise when can't finish user's homework"""
    def __init__(self, data):
        Exception.__init__(self, data)
        self.data = data

    def __str__(self):
        return " UserId: " + self.data[0] + "-> Can't finish this user's" \
                                            " SafeTips,Result :" + self.data[1]


class GetTipsError(Exception):
    """this Error will raise when can't get user's Safetips"""
    def __init__(self, data):
        super().__init__(self, data)
        self.data = data

    def __str__(self):
        return " UserId: " + self.data + "-> Can't get this user's SafeTips"


class ReadSafeTipsError(Exception):
    """This Error will raise when can't read User's safetip"""
    def __init__(self, data):
        super().__init__(self, data)
        self.data = data

    def __str__(self):
        return " UserId: " + self.data[0] + "-> Can't read this user's SafeTip," \
                                            "Return StateCode:" + self.data[1]


def login(username,password):
    """Return User's all Information,Such as UserId,TureName and so on
       Need User's Name and Password,please using type str
    """
    data = {
        "Username": username,
        "Password": password
    }
    Headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Connection": "Keep-Alive"
    }
    # Send request to server to get User info
    login_url = r"http://appapi.safetree.com.cn/usercenter/api/v1/account/PostLogin"
    jsonText = requests.get(login_url, data=data,headers=Headers).text
    # Make String to Dict
    jsonDict = demjson.decode(jsonText)
    if jsonDict['err_code'] or jsonDict['err_desc']:
        raise LoginError
    return jsonDict


#def GetAllStudentInforamtion():
    #return [1, 2, 3]


def get_homework_list(userid,classroom,grade,cityid):
    """This function will return a list with job name and URL dictionary
        e.g : [{"WorkId":workId,"Name":Name,"Link":Link,"li":li,"gid":Gid}]
    """
    GetHomeWorkURL = "https://qingdao.xueanquan.com/webapi/jt/MyHomeWork.html"
    data = {
        "grade": grade,
        "classroom": classroom,
        "cityid": cityid
    }
    tree = fromstring(requests.get(GetHomeWorkURL, data).content.decode())
    number_of_jobs = len(tree.xpath(r'//*[@id="mun_-1_1"]/tr'))
    if not number_of_jobs:
        raise GetHomeWorkError(userid)
    Homeworks = []
    for index in range(1, number_of_jobs + 1):
        _ = tree.xpath(rf'//*[@id="mun_-1_1"]/tr[{index}]/td[7]/a/@onclick')[0]
        _ = _[_.index('(') + 1:_.index(')')]
        if "https://huodong.xueanquan.com" in _:
            continue
        Name = tree.xpath(rf'//*[@id="mun_-1_1"]/tr[{index}]/td[2]/div/a/text()')[0]
        if '活动' in Name:
            continue
        _ = _.split(',')
        li, gid = (_[0], _[3])
        li = li.strip()
        gid = gid.strip()
        workId = tree.xpath(rf'//*[@id="mun_-1_1"]/tr[{index}]/td[7]/a/@name')[0]
        workId = workId[workId.index('_') + 1:]
        _ = {
            "WorkId" : workId,
            "Name" : Name,
            "li" : li,
            "gid" : gid
        }
        Homeworks.append(_)
    return Homeworks


def finish_homework(homework_information,student_information):
    """
        This function will complete the specified safety assignment for the specified student.
        If it fails, it will trigger HomeworkError
    """
    homework_finish_api_url = r"http://shandong.safetree.com.cn/CommonService.asmx/TemplateIn2"
    data = {
        "workid": homework_information["workid"],
        "fid": homework_information["gid"],
        "title": "",
        "require": "",
        "purpose": "",
        "contents": "",
        "testwanser": "0|0|0",
        "testinfo": "已掌握技能",
        "testMark": "100",
        "testReulst": "1",
        "SiteName": "",
        "SiteAddrees": "",
        "WatchTime": "",
        "CourseID": homework_information["li"]
    }
    cookies = {
        "UserID": student_information["userid"],
        "RecordLoginInput_-1": student_information["usertruename"],
        "_UCodeStr": {
            "Grade": student_information["grade"],
            "ClassRoom": student_information["usertruename"],
            "CityCode": student_information["citycode"]
        }
    }
    if demjson.decode(requests.get(homework_finish_api_url, data, cookies=cookies).content.decode()) != "1":
        raise HomeworkError


def get_safetips(authorization,userid ,pagesize):
    """
        This function will return a dictionary with the safety reminder of the input student,
        the content has the safety reminder URL, name, etc.
    """
    request_data = {
        "userId" : userid,
        "parentSortId" : "2",
        "beginIndex" : "0",
        "pageSize" : pagesize
    }
    request_header = {
        "User-Agent": USER_AGENT,
        "Authorization": "Bearer " + authorization,
        "X-UserId": userid
    }
    login_url = r"http://shandong.safetree.com.cn/safeapph5/api/noticeService/getMyReceive"
    resp = requests.get(login_url, data=request_data, headers=request_header)
    json = demjson.decode(resp.content.decode())
    if json["success"] == 0:
        raise GetTipsError([userid, json["message"]])
    return json


def read_safetips(tipurl,userid):
    """
        This function will read the specified security reminder for the specified student account
    """
    request_cookies = {"UserId": userid}
    request_headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "com.jzzs.ParentsHelper", "Connection": "Keep-alive",
        "Accept-Language": "zh-CN,en-US;q=0.8"
    }
    resp = requests.get(tipurl, headers=request_headers, cookies=request_cookies)
    if resp.status_code != 200:
        raise ReadSafeTipsError([userid, resp.status_code])
