import re
import requests
import demjson
from lxml.html import fromstring

User_Agent = "Mozilla/5.0 (Linux; Android 5.1.1; Generic Android-x86 Build/LMY48Z)"\
             "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 "\
             "Safari/537.36 safetreeapp/1.5.1"

DEBUG = False


def set_Debug_state(state):
    global DEBUG
    DEBUG = True

def url_stitching(url, args):
    """用于拼接URL，e.g : url_stiching("baidu.com",{"q":"test"})"""
    _ = list(args.items())
    url += f"?{_[0][0]}={_[0][1]}"
    del _[0]
    loop_num = 0
    while loop_num <= len(_)-1:
        url += f"&{_[loop_num][0]}={_[loop_num][1]}"
        loop_num +=1
    return url


class User:
    homeworks = []
    safetips = []
    def __init__(self, username=None, password=None):
        LOGIN_URL = "http://appapi.safetree.com.cn/usercenter/api/v1/account/PostLogin"
        self.user_information = dict()
        header = {
            "User-Agent": User_Agent,
            "Accept": "application/json",
            "Connection": "Keep-Alive",
            "Content-Type": "application/json"
        }
        data = {
            "Username": username,
            "Password": password
        }
        try:
            self.user_information = demjson.decode(requests.post(LOGIN_URL, data=demjson.encode(data), headers=header).text)['data']
        except:
            if DEBUG:
                with open("DebugLog.txt",'w+') as f:
                    f.write("ERROR:\t Body Message:")
                    f.write(requests.post(LOGIN_URL, data=demjson.encode(data), headers=header).text)
                    f.write("\n at Login time \n")
            raise RuntimeError("登录失败")



    def get_homeworks(self):
        GET_HOMEWORK_URL = "https://qingdao.xueanquan.com/PhoneEpt/NewMyHomeWork.aspx"
        cookies = {
            "UserID": self.user_information["accessCookie"]
        }
        tree = fromstring(requests.get(GET_HOMEWORK_URL, cookies=cookies).text)
        for index in range(1, len(tree.xpath('//*[@id="setven_3"]/li'))+1):
            is_finished = False
            job_url = tree.xpath(f'//*[@id="setven_3"]/li[{index}]/a/@href')[0]
            job_name = tree.xpath(f'//*[@id="setven_3"]/li[{index}]/a/p/text()')[0]
            if tree.xpath(f'//*[@id="setven_3"]/li[{index}]/a/span[2]/text()')[0] == "已完成":
                is_finished = True
            if "【安全学习】" not in job_name:continue
            homework = {
                "Name": job_name,
                "URL": job_url,
                "State": is_finished
            }
            self.homeworks.append(homework)


    def get_safetips(self, pagesize=10):
        GET_SAFETIPS_URL = "http://shandong.safetree.com.cn/safeapph5/api/noticeService/getMyReceive"
        url_argvs = {
            "userId": self.user_information["accessCookie"],
            "parentSortId": "2",
            "beginIndex": "0",
            "pageSize": pagesize
        }
        tips_url = url_stitching(GET_SAFETIPS_URL, url_argvs)
        headers = {
            "User-Agent": User_Agent,
            "Authorization": "Bearer "+self.user_information["accessToken"],
            "X-UserId": str(self.user_information["plainUserId"])
        }
        tips = demjson.decode(requests.get(tips_url, headers=headers).text)
        if not tips['success']:
            if DEBUG:
                with open("DebugLog.txt",'w+') as f:
                    f.write(f"Error:\t{tips['message']} at get_safetips()")
            raise RuntimeError(f"ERROR: {tips['message']}")
        for tip in tips['result']:
            tip_information ={
                "Name": tip["title"],
                "MessageID": tip['messageID'],
                "State": tip['isRead'],
                "SortID": tip["sortId"]
            }
            self.safetips.append(tip_information)
        return True


    def finish_Homework(self, homework):
        FINISH_HOMEWORK_URL = "https://qingdao.xueanquan.com/PhoneEpt/SkillQuestionList.aspx"
        gid, li = re.findall(r"gid=(.+?)&li=(.+?)\b", homework['URL'])[0]
        if homework['State']:
            return True
        cookies = {
            "UserID": self.user_information["accessCookie"]
        }
        url_argvs = {
            'course': li,
            "from": ""
        }
        Final_URL = url_stitching(FINISH_HOMEWORK_URL, url_argvs)
        html = requests.get(Final_URL, cookies=cookies).content.decode()
        #替换特殊字符以便后期查找workID
        js_command = fromstring(html).xpath('//script[11]/text()')[0]
        js_command = js_command[js_command.index("data: {"):]
        js_command = js_command[:js_command.index("}")]
        js_command = js_command.replace("\\n", "").replace("\\r", "").replace("\r", "")
        js_command = js_command.replace("\n", "")
        workid = re.findall("workid:(.+?),", js_command)[0]
        data = {
            "workid": str(workid),
            "fid": str(gid),
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
            "CourseID": str(li)
        }
        #教育平台这个POST估计是遗留问题。。。。
        #之前应该用的是GET，现在POST必须在URL里写data并POSTdata，
        #否则在Postman里报错了？？？？？？？
        url_argvs = {
            "workid": str(workid),
            "fid": str(gid),
            "title": " ",
            "require": " ",
            "purpose": " ",
            "contents": " ",
            "testwanser": "0|0|0",
            "testMark": "100",
            "testinfo": "已掌握技能",
            "testReulst": "1",
            "SiteAddrees": " ",
            "SiteName": " ",
            "watchTime": " ",
            "CourseID": str(li)
        }
        get_homework_url = url_stitching(FINISH_HOMEWORK_URL, url_argvs)
        homework['State'] = True
        return requests.post(get_homework_url, data=data, cookies=cookies)


    def read_tips(self, tip):
        # API Error ,researching New API
        pass


u = User("dongxiaotian","123456qw")
u.get_homeworks()
u.homeworks[0]['State'] = False
u.finish_Homework(u.homeworks[0])