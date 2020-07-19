# 帮助文档

Update Time: 7-19

### 本文档全部基于：

```python
 from safetreeApi import  *
```

## 登陆

```python
User(username, password) #登录并返回User对象
```

```
In[0]: u = User("USER_NAME","USER_PASSWORD")
In[1]: u
Out[1]: <safetreeApi.User at 0x8ccf748> 
```

## 获取作业

```python
User.get_homeworks()
```

```
In[0]: User.get_homeworks()
In[1]: User.homeworks
Out[1]: [{..},{..},..]
```

## 获取安全提醒

```python
User.get_safetips(pagesize) #默认为10
```

```
In[0]: User.get_safetips() //pagesize为需请求安全提醒数量
In[1]: User.safetips
Out[1]: [{..},{..},....]
In[2]: len(User.safetips)
Out[2]: 10
```

## 完成作业

```python
User.finish_Homework(homework) #homework为User.homeworks中的任意字典或符合其规范的任一字典
```

```
In[0]: User.finish_Homework(homework)
out[0]: True
```

## 完成安全提醒

```python
User.read_tips(tip) #tip为User.safetips中的任意字典或符合其规范的任一字典
```

#### 暂未实现

