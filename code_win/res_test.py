import auto_res_win as ars
import main_win as mw
import schedule
from time import sleep

if __name__ == '__main__':
    path = "..//input//input.txt"
    (username,password,start_date,end_date,area,pos,email,url,aliyun_u,aliyun_p,aliyun_r) = mw.init_vars(path)
    start = '1500'
    end = '1800'
    dr = ars.AutoRes(username,password,area,pos,start,end,start_date,url,aliyun_u,aliyun_p,aliyun_r,email)
    if(dr.login()):
        if(dr.make_res()):
            dr.driver.quit()
            schedule.every().day.at("15:00").do(dr.sign_in)
            while(True):
                schedule.run_pending()
                sleep(1)
    dr.driver.quit()