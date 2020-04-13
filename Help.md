# 帮助文档

## 所有函数的参数都必须为str
## 本文档全部基于from safetreeApi import *

# 登录
    
### login(username,password)

### 返回值
    
    {'data': 
      {'userId': str,
        'userName': str,
        'refreshToken': str,
        'accessToken': str,
        'expire': int,
        'accessCookie': str,
        'userType': int,
        'comefrom': ,
        'webUrl': str,
        'nickName': str,
        'wxNickName': ,
        'gender': int,
        'avatar': str,
        'isBandPhone': bool,
        'isBandWx': bool,
        'isBandCseeAccount': bool,
        'gesturePassword': None,
        'bandPhone': str,
        'regionalName': str,
        'areaName': str,
        'schoolName': str,
        'classroomName': str,
        'regionalAuthority': int,
        'prvId': int,
        'cityId': int,
        'countyId': int,
        'schoolId': int,
        'grade': int,
        'classroomId': int,
        'townsId': int,
        'townsName': str,
        'indexUrl': str,
        'discoveryUrl': str,
        'signarlConnect': int,
        'schoolYearData': str,
        'longPollInterval': [int, int, int, int],
        'xgAccount': str,
        'plainUserId': int,
        'accountType': int,
        'verifyResult': int,
        'msg': None,
        'loginRedrect': str,
        'relationId': str,
        'boolName': str,
        'relationUserIds': []},
       'err_code': int,
       'err_desc': str}

# 获取作业

### get_homework_list(cityid,classroom,grade)

#### 所有值都位于login()返回的dict中

## 返回值
    [{'Name': '让孩子学习如何与朋友相处',
    'li': '948',
    'gid': '493',
    'workId': '1639449',
    'url': 'https://qingdao.xueanquan.com/JiaTing/EscapeSkill/SeeVideo.aspx\\?gid=493&li=948'},
    {'Name': '让孩子知道如何应对重大传染病疫情',
    'li': '947',
    'gid': '493',
    'workId': '1638469',
    'url': 'https://qingdao.xueanquan.com/JiaTing/EscapeSkill/SeeVideo.aspx\\?gid=493&li=947'},
    {'Name': '帮助孩子了解并预防亚健康',
    'li': '946',
    'gid': '493',
    'workId': '1544469',
    'url': 'https://qingdao.xueanquan.com/JiaTing/EscapeSkill/SeeVideo.aspx\\?gid=493&li=946'},
    {'Name': '学习预防性伤害的技巧',
    'li': '945',
    'gid': '493',
    'workId': '1532142',
    'url': 'https://qingdao.xueanquan.com/JiaTing/EscapeSkill/SeeVideo.aspx\\?gid=493&li=945'}]

# 完成作业

## 此功能暂未验证！

### finish_homework(workid,gid,li,accessCookie)

#### workid、li、gid位于get_homework_list返回的list中，accessCookie位于login()返回的dict中

# 获取安全提醒

## get_safetips(accessToken,accessCookie ,pagesize,plainUserId)

#### plainUserId,accessCookie,accessToken位于login()返回的dict中,pagesize为需要请求的条数,从最新一条开始

### 返回值

    {
      "success": true,
      "result": [
         {
            "messageID": 53686700,
            "sortId": 10,
            "sortName": "周末提醒",
            "sortIcon": "http://file.safetree.com.cn/AppNotice/NavIco/AppNotice/I201703021912203329.jpg",
            "title": "4月第2周 防溺无小事 家长须警惕（2020.4.7-4.12）",
            "createUserName": "   ",
            "createUserUnit": "   ",
            "sendCount": 0,
            "readCount": 0,
            "sendTime": "2020-04-10 09:13:17",
            "constraintAffirm": false,
            "isRead": true,
            "isShowDetail": true,
            "redirectUrl": "https://file.safetree.com.cn/apph5/html/WarningNoticeDetial_v2_0.html?currentRT=1&currentUserRegion=0&PrvCode=26&SortId=10&result=53686700&host=https://qingdao.safetree.com.cn"
        },
        {
            "messageID": 53173611,
            "sortId": 11,
            "sortName": "节假日提醒",
            "sortIcon": "http://file.safetree.com.cn/AppNotice/NavIco/AppNotice/I201703021913011372.jpg",
            "title": "【开学】开学季·安全记 安全防范要牢记",
            "createUserName": "   ",
            "createUserUnit": "   ",
            "sendCount": 0,
            "readCount": 0,
            "sendTime": "2020-04-05 12:20:23",
            "constraintAffirm": false,
            "isRead": true,
            "isShowDetail": true,
            "redirectUrl": "https://file.safetree.com.cn/apph5/html/WarningNoticeDetial_v2_0.html?currentRT=1&currentUserRegion=0&PrvCode=26&SortId=11&result=53173611&host=https://qingdao.safetree.com.cn"
        },
        {
            "messageID": 53112553,
            "sortId": 11,
            "sortName": "节假日提醒",
            "sortIcon": "http://file.safetree.com.cn/AppNotice/NavIco/AppNotice/I201703021913011372.jpg",
            "title": "【清明节】4月第1周 清明期间文明祭祀安全出行倡议书（2020.3.30-4.4）",
            "createUserName": "   ",
            "createUserUnit": "   ",
            "sendCount": 0,
            "readCount": 0,
           "sendTime": "2020-04-02 09:27:26",
           "constraintAffirm": false,
           "isRead": true,
           "isShowDetail": true,
           "redirectUrl": "https://file.safetree.com.cn/apph5/html/WarningNoticeDetial_v2_0.html?currentRT=1&currentUserRegion=0&PrvCode=26&SortId=11&result=53112553&host=https://qingdao.safetree.com.cn"
        }
    ],
      "message": "OK"
    }


# 完成安全提醒

## read_safetips(tipurl,accessToken,accessCookie)

#### accessCookie,accessToken位于login()返回的dict中,tipurl位于get_safetips()请求回的list中
