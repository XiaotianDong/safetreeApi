package safetreeapi

import (
	"fmt"

	"github.com/asmcos/requests"
)

//用户基本信息
type userInformation struct {
	accessToken   string
	accessCookie  string
	cityId        string
	classroom     string
	grade         string
	plainUserId   string
	userTruthName string //用户真实名称
}

//作业信息
type homeworkInformation struct {
	workid string
	gid    string
	li     string
	name   string
}

//安全提醒的有关信息
type safetipInformation struct {
	name string //安全提醒题目
	url  string //安全提醒的URL
}

func login(username string, password string) {
	fmt.Println("Load Login Func Succeed")
	fmt.Println("UserName = " + username + "Password = " + password)
	resp, err := requests.Get("http://www.baidu.com")
	if err != nil {
		return
	}
	fmt.Println(resp.Text())
}
