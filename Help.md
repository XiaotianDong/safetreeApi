# 帮助文档

# 所有函数的参数都必须为str

# Login
    
    import SafetreeApi  

    SafetreeApi.login(yourUserName,Password)  

    #yourUserName,Password都为str类型

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

     import safetreeApi
     safetreeApi.get_homework_list()

## 所有值都位于login()返回的dict中，如遇非str类型请自行转换

# 完成作业
## 此功能暂未验证！
    import safetreeApi
    safetreeApi.finish_homework()
## workid、li、gid位于get_homework_list返回的list中，accessCookie位于login()返回的dict中
## 部分参数请自行转化为str
