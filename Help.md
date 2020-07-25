# 帮助文档

Update Time: 7-19

### 本文档全部基于：

```python
 from safetreeApi import  *
```

# 学生类功能

## 登陆

```python
Student(Studentname, password) #登录并返回Student对象
```

```
In[0]: u = Student("Student_NAME","Student_PASSWORD")
In[1]: u
Out[1]: <safetreeApi.Student at 0x8ccf748> 
```

## 获取作业

```python
Student.get_homeworks()
```

```
In[0]: Student.get_homeworks()
In[1]: Student.homeworks
Out[1]: [{..},{..},..]
```

## 获取安全提醒

```python
Student.get_safetips(pagesize) #默认为10
```

```
In[0]: Student.get_safetips() //pagesize为需请求安全提醒数量
In[1]: Student.safetips
Out[1]: [{..},{..},....]
In[2]: len(Student.safetips)
Out[2]: 10
```

## 完成作业

```python
Student.finish_Homework(homework) #homework为Student.homeworks中的任意字典或符合其规范的任一字典
```

```
In[0]: Student.finish_Homework(homework)
out[0]: True
```

## 完成安全提醒

```python
Student.read_tips(tip) #tip为Student.safetips中的任意字典或符合其规范的任一字典
```

#### 暂未实现



# 教师类功能
# UNAVAILABLE!!

## 登录

```python
teacher(TEACHER_NAME,TEACHER_PASSWORD)
```

```python
In[0]: teacher = teacher("EXAMPLE","EXAMPLE")
```

## 获取学生信息

```python
teacher.get_students_information()
```

```python
In[0]: teacher = teacher("EXAMPLE","EXAMPLE")
In[1]: teacher.get_students_information()
In[2]: teacher.students
Out:[2]:  [<safetreeApi.Student at 0x8c14888>,.......]
```

## 重置学生密码

```python
teacher.reset_student_password(StudentClass)
```

```python
In[0]: teacher = teacher("EXAMPLE","EXAMPLE")
In[1]: teacher.get_students_information()
In[2]: teacher.reset_student_password(teacher.students[0])
Out[2]: True
```
```
OR
---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
<ipython-input-5-782790b0e305> in <module>
----> 2  teacher.reset_student_password(teacher.students[0])

RuntimeError: Can't reset studnet Password.
```
