"""安全教育平台API   暂只支持qingdao.xueanquan.com    Update Time 2020/4/28"""

import re
import requests
import demjson
from lxml.html import fromstring


API = {
    "User_Agent": "Mozilla/5.0 (Linux; Android 5.1.1; Generic Android-x86 Build/LMY48Z) AppleWebKit"\
                  "/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Safari/537.36 safetreeapp"\
                  "/1.5.1",
    "Login_URL": "http://appapi.safetree.com.cn/usercenter/api/v1/account/PostLogin",
    "Get_Homework_URL": "https://qingdao.xueanquan.com/PhoneEpt/NewMyHomeWork.aspx",
    "Finish_Homework_URL": "http://qingdao.xueanquan.com//CommonService.asmx/TemplateIn2",
    "Get_Tips_URL": "http://shandong.safetree.com.cn/safeapph5/api/noticeService/getMyReceive",
    "Read_Tips_URL": "https://qingdao.safetree.com.cn/safeapph5/api/notice/getByIdNoticeMessageDetails"
}

class User:
    """
    账户的基本信息及作业与安全提醒查询及缓存
    """
    def __init__(self, username=None, password=None, UsingCache=False, CacheFile=None):
        """
        初始化类
        username 用户名
        password 密码
        UsingCache 是否使用缓存，默认不使用
        CacheFile 若UsingCache为true则在此文件中读取用户信息
        """
        user_information = {}
        if UsingCache:
            user_information = demjson.decode_file(CacheFile)
        else:
            # 登陆并获取用户信息
            header = {
                "User-Agent": API["User_Agent"],
                "Accept": "application/json",
                "Connection": "Keep-Alive",
                "Content-Type": "application/json"
                }
            data = {
                "Username": username,
                "Password": password
                }
            _ = requests.post(API["Login_URL"], data=demjson.encode(data), headers=header).text
            try:
                user_information = demjson.decode(_)['data']
            except KeyError:
                raise RuntimeError("登录失败，请检查用户名与密码")
        self.accessToken = user_information["accessToken"]
        self.accessCookie = user_information["accessCookie"]
        self.plainUserId = str(user_information["plainUserId"])
        self.information = {
            "Grade": str(user_information["grade"]),
            "cityId": str(user_information['cityId']),
            "classroom": str(user_information['classroomId']),
            "trueName": user_information['nickName']
        }
        self.homeworks = []
        self.safetips = []
        del user_information


    def get_user_true_name(self):
        """获取用户名称"""
        return self.information["trueName"]


    def get_homework(self):
        """获取所有安全作业"""
        cookies = {
            "UserID": self.accessCookie
        }
        html = requests.get(API["Get_Homework_URL"], cookies=cookies).text
        tree = fromstring(html)
        for index in range(1, len(tree.xpath('//*[@id="setven_3"]/li'))+1):
            is_finished = False
            job_url = tree.xpath(f'//*[@id="setven_3"]/li[{index}]/a/@href')[0]
            job_name = tree.xpath(f'//*[@id="setven_3"]/li[{index}]/a/p/text()')[0]
            if tree.xpath(f'//*[@id="setven_3"]/li[{index}]/a/span[2]/text()')[0] == "已完成":
                is_finished = True
            if "【安全学习】" not in job_name:
                continue
            self.homeworks.append(Homework(job_url, job_name, is_finished))


    def get_safetips(self, pagesize):
        """
        获取安全提醒
        pagesize 获取数量
        """
        tips_url = API["Get_Tips_URL"]+f"?userId={self.accessCookie}&parentSortId=2"\
                   f"&beginIndex=0&pageSize={pagesize}"
        header = {
            "User-Agent": API["User_Agent"],
            "Authorization": "Bearer "+self.accessToken,
            "X-UserId": self.plainUserId
        }
        resp = requests.get(tips_url, headers=header)
        tips = demjson.decode(resp.text)
        if not tips["success"]:
            raise RuntimeError(tips["message"])
        for tip in tips['result']:
            self.safetips.append(Safetips(name=tip["title"], messageId=tip['messageID'], is_read=tip['isRead']))


    def write_cache(self, filepath):
        """
        写入缓存
        filepath 文件路径 e.g ~/Cache.json
        """
        file_obj = open(filepath, "w")
        data = {
            "accessToken": self.accessToken,
            "accessCookie": self.accessCookie,
            "plainUserId": self.plainUserId,
            "grade": self.information["Grade"],
            "classroomId": self.information["classroom"],
            "cityId": self.information["cityId"],
            "nickName": self.information["trueName"]
        }
        file_obj.write(demjson.encode(data))
        file_obj.close()


class Homework:
    """
    安全作业类
    用于完成作业与查询作业基本信息
    """
    def __init__(self, url, name, is_finish):
        """
        url 安全作业URL
        name 安全作业名称
        is_finish 作业完成状态
        """
        result = re.findall(r"gid=(.+?)&li=(.+?)\b", url)[0]
        self.gid = result[0]
        self.li = result[1]
        self.name = name
        self.is_finish = is_finish


    def get_name(self):
        """获取安全作业名称"""
        return self.name


    def finish_homework(self, user_info):
        """
        完成作业
        user_info User类
        """
        if self.is_finish:
            print("It already Finished.")
            return True
        cookies = {
            "UserID": user_info.accessCookie
        }
        URL = f"https://qingdao.xueanquan.com/PhoneEpt/SkillQuestionList.aspx?course={str(self.li)}&from="
        html = requests.get(URL, cookies=cookies).content.decode()
        #替换特殊字符以便后期查找workID
        js_command = fromstring(html).xpath('/html/head/script[10]/text()')[0]
        js_command = js_command[js_command.index("data: {"):]
        js_command = js_command[:js_command.index("}")]
        js_command = js_command.replace("\\n", "").replace("\\r", "").replace("\r", "").replace("\n", "")
        workid = re.findall("workid:(.+?),", js_command)[0]
        data = {
            "workid": str(workid),
            "fid": str(self.gid),
            "title": "",
            "require": "",
            "purpose": "",
            "contents": "",
            "testwanser": "0|0|0",
            "testinfo": "已掌握技能",
            "testMark": "100",
            "testReulst": "1",
            "SiteAddrees": "",
            "SiteName": "",
            "watchTime": "",
            "CourseID": self.li
        }
        #教育平台这个POST估计是遗留问题。。。。
        #之前应该用的是GET，现在POST必须在URL里写data并POSTdata，
        #否则在Postman里报错了？？？？？？？
        URL = API["Finish_Homework_URL"]+f"?workid={str(workid)}&fid={str(self.gid)}&title=&require=&"\
              f"purpose=&contents=&testwanser=0|0|0&testMark=100&testinfo=已掌握技能&testReulst=1&SiteAddrees"\
              f"=&SiteName=&watchTime=&CourseID={self.li}"
        return demjson.decode(requests.post(URL, data=data, cookies=cookies).text)
        #可将此行替换为:
        #requests.post(URl,data=data,cookies=cookies)


class Safetips:
    """安全提醒"""
    def __init__(self, name, messageId, is_read):
        """
        name 名称
        is_read 阅读状态
        """
        self.messageId = messageId
        self.name = name
        self.is_read = is_read
    def read_tips(self, user_info):
        """阅读安全提醒"""
        if self.is_read:
            print("It already read")
            return True
        URL = API["Read_Tips_URL"]+f"?id={self.messageId}&messageRead=true"
        header = {
            "User-Agent": API["User_Agent"],
            "X-UserId":user_info.accessCookie,
            "Authorization": f"Bearer {user_info.accessToken}"
        }
        resp = requests.get(URL, headers=header)
        return demjson.decode(resp.text)
    def get_name(self):
        """获取安全提醒名称"""
        return self.name
