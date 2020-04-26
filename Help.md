# 帮助文档

### 4-25更新

## 登录、查询作业/安全提醒:

    import safetreeApi as sf
    #登录
    #返回user类
    user = sf.user("EXAMPLE_USER","EXAMPLE_PASSWORD")
    # 获取作业
    #返回列表，列表内为homework类
    homeworks = user.get_homework()
    #获取安全提醒
    #pagesize为需要请求的数量，从最新一个开始
    #返回内为safetip类的列表
    safetips = user.get_safetips(self,pagesize)

## 完成安全作业/阅读安全提醒

    import safetreeApi as sf
    #登录
    user = sf.user("EXAMPLE_USER","EXAMPLE_PASSWORD")
    #获取作业
    homeworks = user.get_homework()
    #完成作业其中之一
    homeworks[0].finish_homework(user)
    #获取安全提醒
    tips = user.get_safetips(pagesize)
    #阅读其中之一
    tips[0].ReadTips(user)


## 缓存功能
    import safetreeApi as sf
    #登录
    user = sf.user("EXAMPLE_USER","EXAMPLE_PASSWORD")
    #新建缓存文件
    user.write_Cache(FILE_PATH)
    #读取缓存
    user = sf.user(UsingCache=True,CacheFile=FILE_PATH)