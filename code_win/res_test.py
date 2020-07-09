import auto_res_win as ars
import main_win as mw
import schedule
from time import sleep

# 异常列表：
# 找不到start和end时间，没显示-TimeoutException
# 
if __name__ == '__main__':
    path = "..//input//input.txt"
    (username,password,start_date,end_date,area,pos,email,url,aliyun_u,aliyun_p,aliyun_r) = mw.init_vars(path)
    start = '1020'
    end = '1100'  
    dr = ars.AutoRes(username,password,area,pos,start,end,int(start_date),url,aliyun_u,aliyun_p,aliyun_r,email)
    if(dr.login()):
        if(dr.make_res()):
            dr.driver.quit()
            print("ok")
            #schedule.every().day.at("09:12").do(dr.sign_in)
            #while(True):
                #schedule.run_pending()
                #sleep(1)
    dr.driver.quit()