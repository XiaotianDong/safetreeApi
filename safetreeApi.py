import requests,demjson,re
from lxml.html import fromstring


API = {
    "User_Agent": "Mozilla/5.0 (Linux; Android 5.1.1; Generic Android-x86 Build/LMY48Z) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Safari/537.36 safetreeapp/1.5.1",
    "Login_URL": "http://appapi.safetree.com.cn/usercenter/api/v1/account/PostLogin",
    "Get_Homework_URL": "https://qingdao.xueanquan.com/PhoneEpt/NewMyHomeWork.aspx",
    "Finish_Homework_URL": "http://qingdao.xueanquan.com//CommonService.asmx/TemplateIn2",
    "Get_Tips_URL": "http://shandong.safetree.com.cn/safeapph5/api/noticeService/getMyReceive",
    "Read_Tips_URL": "https://qingdao.safetree.com.cn/safeapph5/api/notice/getByIdNoticeMessageDetails"
}

class user:
    def __init__(self,username=None,password=None,UsingCache=False,CacheFile=None):
        User_information = {}
        if UsingCache:
            User_information = demjson.decode_file(CacheFile)
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
            _ = requests.post(API["Login_URL"],data=demjson.encode(data),headers=header).text
            try:
                User_information = demjson.decode(_)['data']
            except KeyError:
                raise RuntimeError("登录失败，请检查用户名与密码")
        self.accessToken = User_information["accessToken"]
        self.accessCookie = User_information["accessCookie"]
        self.plainUserId = str(User_information["plainUserId"])
        self.Grade = str(User_information["grade"])
        self.cityId = str(User_information['cityId'])
        self.classroom = str(User_information['classroomId'])
        self.trueName = User_information['nickName']
        del User_information


    def get_user_true_name(self):
        return self.trueName


    def get_homework(self):
        cookies = {
            "UserID":self.accessCookie
        }
        html = requests.get(API["Get_Homework_URL"],cookies=cookies).text
        tree = fromstring(html)
        self.homeworks = []
        for index in range(len(tree.xpath('//*[@id="setven_3"]/li'))):
            Is_finished = False
            url = tree.xpath(f'//*[@id="setven_3"]/li[{index}]/a/@href')[0]
            name = tree.xpath(f'//*[@id="setven_3"]/li[{index}]/a/p/text()')[0]
            if tree.xpath(f'//*[@id="setven_3"]/li[{index}]/a/span[2]'):
                Is_finished = True
            if "【安全学习】" not in name:
                continue
            self.homeworks.append(homework(url,name,Is_finished))


    def get_safetips(self,pagesize):
        URL = API["Get_Tips_URL"]+f"?userId={self.accessCookie}&parentSortId=2&beginIndex=0&pageSize={pagesize}"
        header={
            "User-Agent": API["User_Agent"],
            "Authorization": "Bearer "+self.accessToken,
            "X-UserId": self.plainUserId
        }
        resp = requests.get(URL,headers=header)
        tips = demjson.decode(resp.text)
        self.safetips = []
        if not tips["success"]:
            raise RuntimeError(tips["message"])
        for tip in tips['result']:
           self.safetips.append(safetips(name=tip["title"],messageId=tip['messageID'],Is_read=tip['isRead']))
    def write_Cache(self,filepath):
        f = open(filepath,"w")
        data = {
            "accessToken": self.accessToken,
            "accessCookie": self.accessCookie,
            "plainUserId": self.plainUserId,
            "grade": self.Grade,
            "classroomId": self.classroom,
            "cityId": self.cityId,
            "nickName": self.trueName
        }
        f.write(demjson.encode(data))
        f.close()


class homework:
    def __init__(self,url,name,Is_finish):
        result = re.findall("gid=(.+?)&li=(.+?)",url)
        self.gid = result[0]
        self.li = result[1]
        self.name = name
        self.Is_finish = Is_finish


    def finish_homework(self,user):
        if self.Is_finish:
            print("It already Finished.")
            return True
        URL = f"https://qingdao.xueanquan.com/PhoneEpt/SkillQuestionList.aspx?course={str(self.li)}&from="
        html = requests.get(URL).text
        workid = re.findall("workid:(.?+),", html)[0]
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
        cookies = {
            "UserID": user.accessCookie
        }
        #教育平台这个POST估计是遗留问题。。。。
        #之前应该用的是GET，现在POST必须在URL里写data并POSTdata，
        #否则在Postman里报错了？？？？？？？
        URL = API["Finish_Homework_URL"]+f"?workid={str(workid)}&fid={str(self.gid)}&title=&require=&"\
              f"purpose=&contents=&testwanser=0|0|0&testMark=100&testinfo=已掌握技能&testReulst=1&SiteAddrees"\
              f"=&SiteName=&watchTime=&CourseID={self.li}"
        return demjson.decode(requests.post(URL, data=data, cookies=cookies).text)
        #可将此行替换为:
        # # requests.post(URl,data=data,cookies=cookies)


class safetips:
    def __init__(self,name,messageId,Is_read):
        self.messageId = ""
        self.name = ""
        self.Is_read = Is_read


    def ReadTips(self,user):
        if self.Is_read:
            print("It already read")
            return True
        URL = API["Read_Tips_URL"]+f"?id={self.messageId}&messageRead=true"
        header = {
            "User-Agent": API["User_Agent"],
            "X-UserId":user.accessCookie,
            "Authorization": f"Bearer {user.accessToken}"
        }
        resp = requests.get(URL,headers=header)
        return demjson.decode(resp.text)
