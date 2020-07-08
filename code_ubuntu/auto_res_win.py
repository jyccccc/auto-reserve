from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
import time
from time import sleep
from selenium.webdriver.support.select import Select
import mail_utils as MU


class AutoRes:
    chrome_options = webdriver.ChromeOptions()
    username = ''
    password = ''
    area = ''
    pos = ''
    start = ''
    end = ''
    
    def __init__(self,username,password,area,pos,start,end,cur_date,url,aliyun_u,aliyun_p,aliyun_r,email):
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--no-sandbox') # 这个配置很重要
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options,executable_path='/home/jyc/softwares/chromedriver')
        self.username = username
        self.password = password
        self.area = area
        self.pos = pos
        self.start = start
        self.end = end
        self.cur_date = cur_date
        self.url = url
        self.aliyun_u = aliyun_u
        self.aliyun_p = aliyun_p
        self.aliyun_r = aliyun_r
        self.email = email
        
    def login(self,count=5):  # 登录
        if(count == 0):
            print("can not login!")
            return False
        if(self.driver.title == '宁波大学信息共享空间'):
            print("login successfully")
            return True
        try:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ': try to login ')
            self.driver.get('https://uis.nbu.edu.cn/authserver/login?service=http://zizhu.nbu.edu.cn/loginall.aspx?page=')
            sleep(3)
            input_username = WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.ID,'username')))
            input_password = WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.ID,'password')))
            input_username.send_keys(self.username)
            input_password.send_keys(self.password)
            sleep(5)
            self.driver.find_element_by_id('password').submit()
        except NoSuchElementException:
            print("NoSuchElementException happened, now retry %d" %(count-1))
            self.driver.refresh()
            self.login(count-1)
        except StaleElementReferenceException:
            print("StaleElementReferenceException happened, now retry %d" %(count-1))
            self.driver.refresh()
            self.login(count-1)
        except TimeoutException:
            print("TimeoutException happened, now retry %d" %(count-1))
            self.driver.refresh()
            self.login(count-1)
        else:
            sleep(3)
            if(self.driver.title == '宁波大学信息共享空间'):
                print("login successfully")
                return True
            elif(self.driver.title == '宁波大学统一身份认证'):
                self.login(count-1)
        finally:
            if(self.driver.title == '宁波大学信息共享空间'):
                print("login successfully")
                return True
            if(self.driver.title == '宁波大学统一身份认证'):
                print("login fail")
                return True
    
    # 预约
    def make_res(self,count=5):
        if(count == 0):
            print("can not reserve")
            return False
        try:
            areas = self.driver.find_elements_by_class_name('it')
            # 打开区域
            for area in areas:
                if(area.text == self.area):
                    area.click()
                    break
            sleep(5)
            # 选择预约时间
            WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME,'fp-date'))).click()
            # 选择日期
            sleep(2)
            row = (self.cur_date - 6)/7 + 2
            col = (self.cur_date - 5)%7
            xpath = '//*[@id="ui-datepicker-div"]/table/tbody/tr[%d]/td[%d]' %(row,col)
            WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()
            # 选择预约时间
            #  h-8:21:1;  m-0:50:10
            start_ele = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,'fp-time-start')))
            self.selectTime(start_ele,int(self.start[:2]),int(self.start[2:]))
            end_ele = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,'fp-time-end')))
            self.selectTime(end_ele,int(self.end[:2]),int(self.end[2:]))
            self.driver.find_element_by_class_name('ui-datepicker-close').click()
            print('choose the time %s:%s-%s:%s successfully!' %(self.start[:2],self.start[2:],self.end[:2],self.end[2:]))
            # 选择座位
            poses = self.driver.find_elements_by_class_name("fp-dot")
            num = len(poses)
            rs = 0
            for i in range(0,num):
                titles = self.driver.find_elements_by_class_name("fp-dot")[i].get_attribute('data-original-title')
                if(self.area+self.pos == titles):
                    rs = i
                    break
            right_pos = self.driver.find_elements_by_class_name("fp-dot")[rs]
            print('choose the ' + right_pos.get_attribute('data-original-title') + ' successfully!')
            sleep(3)
            # 预约
            right_pos.click()
            sleep(5)
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.ID,"ui-id-1")))
            st = self.start
            et = self.end
            if(self.start[0] == '0'):
                st = self.start[1:]
            if(self.end[0] == '0'):
                et = self.end[1:]
            se = "//select[@name='start_time']/option[@value='%s']" %st
            ee = "//select[@name='end_time']/option[@value='%s']" %et
            print(se)
            print(ee)
            self.driver.find_element_by_xpath('//tbody[@class="dlg_dt_panel"]/tr[2]/td[2]/div[1]/span[1]/select').click()
            WebDriverWait(self.driver,5).until(EC.element_to_be_clickable((By.XPATH,se))).click()
            sleep(2)
            self.driver.find_element_by_xpath('//tbody[@class="dlg_dt_panel"]/tr[2]/td[2]/div[1]/span[3]/select').click()
            WebDriverWait(self.driver,5).until(EC.element_to_be_clickable((By.XPATH,ee))).click()
            sleep(3)
            submit_btn = self.driver.find_element_by_class_name('mt_sub_resv')
            submit_btn.click()
            sleep(1)
            infos = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="uni_confirm"]/p')))
            if(infos.text == '申请提交成功，是否跳转查看预约信息?'):
                mail_util = MU.Mail_util(self.aliyun_u,self.aliyun_p,self.aliyun_r)
                res_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                content = ' %s 预约%s-%s：%s-%s成功！' % (self.username,self.area,self.pos,self.start,self.end)
                mail_util.send_email('图书馆预约通知',res_time + content,self.email)
                print(self.username + ' reserve successfully! ')
                return True
            else:
                print(infos.text)
                return False
        except NoSuchElementException:
            print("NoSuchElementException happened, now retry %d" %(count-1))
            self.driver.refresh()
            self.make_res(count-1)
        except StaleElementReferenceException:
            print("StaleElementReferenceException happened, now retry %d" %(count-1))
            self.driver.refresh()
            self.make_res(count-1)
        except TimeoutException:
            print("TimeoutException happened, now retry %d" %(count-1))
            self.driver.refresh()
            self.make_res(count-1)


    def sign_in(self,count=5):
        if(count == 0):
            print("sigin in fail!")
            return False
        try:
            self.driver.get(self.url)
            input_username = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.NAME,'szLogonName')))
            input_password = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.NAME,'szPassword')))
            input_username.send_keys(self.username)
            input_password.send_keys(self.password)
            sleep(3)
            input_password.submit()
            sleep(3)
            WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.TAG_NAME,'button'))).click()
            flag = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.info>p'))).text
            print(flag)
            sleep(5)
            if(flag[:4] == '签到成功'):
                mail_util = MU.Mail_util(self.aliyun_u,self.aliyun_p,self.aliyun_r)
                mail_util.send_email('图书馆预约通知','签到成功了',self.email)
                print(self.username + ' signin successfully! ')
                return True
            elif(flag[:4] == '返回成功'):
                mail_util = MU.Mail_util(self.aliyun_u,self.aliyun_p,self.aliyun_r)
                mail_util.send_email('图书馆预约通知','签到成功了',self.email)
                print(self.username + ' signin successfully! ')
                return True
            else:
                self.driver.refresh()
                self.sign_in(count-1)
        except Exception:
            print('sign in fail,retrying ... ')
            self.driver.refresh()
            self.sign_in(count-1)


    # select下拉选框
    def selectTime(self,element,h,m):
        element.click()
        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.ID,'ui-datepicker-div')))
        sleep(2)
        hour = self.driver.find_element_by_xpath('//*[@class="ui_tpicker_hour"]/div/select')
        Select(hour).select_by_value(str(h))
        sleep(1)
        minute = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@class="ui_tpicker_minute"]/div/select')))
        Select(minute).select_by_value(str(m))


