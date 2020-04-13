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

## 所有值都位于login()返回的dict中，如遇非str类型请自行转换

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

## workid、li、gid位于get_homework_list返回的list中，accessCookie位于login()返回的dict中

## 部分参数请自行转化为str

# 获取安全提醒

## get_safetips(accessToken,accessCookie ,pagesize,plainUserId)

## plainUserId,accessCookie,accessToken位于login()返回的dict中,pagesize为需要请求的条数,从最新一条开始

### 返回值
    


# 完成安全提醒

## read_safetips(tipurl,accessToken,accessCookie)

## accessCookie,accessToken位于login()返回的dict中,tipurl位于get_safetips()请求回的list中
