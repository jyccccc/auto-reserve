import auto_res_win as RES
import schedule
import time


def reserve(username,password,area,pos,start,end,cur_date,url,aliyun_u,aliyun_p,aliyun_r,email):
    dr = RES.AutoRes(username,password,area,pos,start,end,cur_date,url,aliyun_u,aliyun_p,aliyun_r,email)
    dr.login()
    dr.make_res()
    global res_flag
    global sign_flag
    global cur
    print("res_flag = %d sign_flag = %d cur = %d " % (res_flag, sign_flag,cur))
    res_flag += 1
    print("res_flag = %d sign_flag = %d cur = %d " % (res_flag, sign_flag,cur))
    dr.driver.quit()


def signin(username,password,area,pos,start,end,start_date,url,aliyun_u,aliyun_p,aliyun_r,email):
    dr = RES.AutoRes(username,password,area,pos,start,end,start_date,url,aliyun_u,aliyun_p,aliyun_r,email)
    dr.sign_in()
    global res_flag
    global sign_flag
    global cur
    print("res_flag = %d sign_flag = %d cur = %d " % (res_flag, sign_flag,cur))
    sign_flag += 1
    print("res_flag = %d sign_flag = %d cur = %d " % (res_flag, sign_flag,cur))
    dr.driver.quit()


def init_vars(path):
    res = []
    with open(path, "r",encoding="utf-8") as f:
        for line in f:
            print(line[:-1])
            res.append(line[:-1])
    return res

if __name__ == '__main__':
    print("------ 简单自制的图书馆预约/签到脚本 -----")
    print("提示：该脚本从开始预约的日期开始到结束的日期自动帮你预约并签到两个时间段：08:00-16:00和18:00-21:00")
    path = "..//input//input.txt"
    (username,password,start_date,end_date,area,pos,email,url,aliyun_u,aliyun_p,aliyun_r) = init_vars(path)
    res_flag = 0
    sign_flag = -1
    cur = int(start_date)
    # 设置预约/签到任务
    res_job1 = schedule.every().day.at("15:27").do(reserve,username,password,area,pos,'1530','1600',cur,url,aliyun_u,aliyun_p,aliyun_r,email)
    res_job2 = schedule.every().day.at("15:28").do(reserve,username,password,area,pos,'1800','2100',cur,url,aliyun_u,aliyun_p,aliyun_r,email)
    sign_job1 = schedule.every().day.at("15:31").do(signin,username,password,area,pos,'0800','1600',cur,url,aliyun_u,aliyun_p,aliyun_r,email)
    sign_job2 = schedule.every().day.at("18:01").do(signin,username,password,area,pos,'0800','1600',cur,url,aliyun_u,aliyun_p,aliyun_r,email)
    print("----- 脚本开始 ------")
    while(True):
        schedule.run_pending()
        # 到达最后一天，而且完成前一天的签到 2
        if(cur == int(end_date) and sign_flag == 2):
            print("预约结束")
            print("res_flag = %d sign_flag = %d " % (res_flag, sign_flag))
            break
        if(res_flag == 2):  # 当天的预约完成 2
            print("res_flag = %d sign_flag = %d cur = %d " % (res_flag, sign_flag,cur))
            res_flag = 0
            sign_flag = 0  # 当前签到的个数
            cur += 1
            print("res_flag = %d sign_flag = %d cur = %d " % (res_flag, sign_flag,cur))
        if(sign_flag == 2):  # 当天的签到完成 2
            print("res_flag = %d sign_flag = %d cur = %d " % (res_flag, sign_flag,cur))
            sign_flag = -1 # 恢复初值
            print("res_flag = %d sign_flag = %d cur = %d " % (res_flag, sign_flag,cur))
        time.sleep(1)
