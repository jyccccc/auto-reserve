import time
import schedule

flag = False


def job():
    global i
    global flag
    print("I'm working... %d" % (i))
    flag = True


def auto_add():
    global i
    i += 1


if __name__ == '__main__':
    i = int(input("input the number you want to start: "))
    job = schedule.every().second.do(job)
    while(True):
        schedule.run_pending()  # 阻塞自己，继续向下执行
        if(flag):
            print("执行了job")
            i += 1
        if(i == 10):  # 停止
            schedule.cancel_job(job)
            break
        # print('now the i is ' + str(i))
        time.sleep(1)