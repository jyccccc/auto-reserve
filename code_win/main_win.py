import auto_res_win as RES
import schedule
import time
from selenium import webdriver
import global_vars


def reserve(username,password,area,pos,st,et,date,email):
    dr = RES.AutoRes(username,password,area,pos,st,et,date)
    RES.doLogin(dr)  # 登录
    RES.doRes(dr,email)  # 预约
    global res_flag
    res_flag += 1
    dr.driver.quit()


def signin(key,username,password,email):
    driver = webdriver.Chrome(executable_path='C:\\Users\\Mar.J\\Downloads\\Compressed\\chromedriver_win32\\chromedriver.exe')
    RES.sign_in(driver,key,username,password,email)
    global sign_flag
    sign_flag += 1
    driver.quit()


if __name__ == '__main__':
    print("------ 简单自制的图书馆预约/签到脚本 -----")
    print("提示：该脚本从开始预约的日期开始到结束的日期自动帮你预约并签到两个时间段：08:00-16:00和18:00-21:00")
    username = input("输入学号：")
    password = input("输入密码（办事大厅）：")
    start_date = int(input("输入开始预约的日期："))
    end_date = int(input("输入结束预约的日期（不包含该天）："))
    area = input("输入预约的区域：")
    pos = input("输入预约的位置：")
    email = input("输入发送的邮件通知：")
    url = input("输入座位的二维码地址：")
    aliyun_u = input("输入阿里云邮箱服务的发件人地址：")
    aliyun_p = input("输入阿里云邮箱服务的发件人密码：")
    aliyun_r = input("输入阿里云邮箱服务的回复地址：")
    keys = ['username','start_date','end_date','password','area','pos','email','key','url','aliyun_u','aliyun_p','aliyun_r']
    values = [username,start_date,end_date,password,area,pos,email,'',url,aliyun_u,aliyun_p,aliyun_r]
    global_vars._init()
    global_vars.set_values(keys,values)
    res_flag = 0
    sign_flag = -1
    # 设置预约/签到任务
    res_job1 = schedule.every().day.at("00:01").do(reserve,username,password,area,pos,'0800','1600',global_vars.get_value('start_date'),email)
    res_job2 = schedule.every().day.at("00:03").do(reserve,username,password,area,pos,'1800','2100',global_vars.get_value('start_date'),email)
    sign_job1 = schedule.every().day.at("08:01").do(signin,global_vars.get_value('key'),username,password,email)
    sign_job2 = schedule.every().day.at("18:01").do(signin,global_vars.get_value('key'),username,password,email)
    print("----- 脚本开始 ------")
    while(True):
        schedule.run_pending()
        # 到达最后一天，而且完成前一天的签到 2
        if((global_vars.get_value('start_date') == global_vars.get_value('end_date')) and sign_flag == 2):
            print("预约结束")
            print("res_flag = %d sign_flag = %d " % (res_flag, sign_flag))
            break
        if(res_flag == 2):  # 当天的预约完成 2
            res_flag = 0
            sign_flag = 0  # 当前签到的个数
            next = global_vars.get_value('start_date') + 1
            global_vars.set_value('start_date',next)
        if(sign_flag == 2):  # 当天的签到完成 2
            sign_flag = -1 # 恢复初值
        time.sleep(1)
