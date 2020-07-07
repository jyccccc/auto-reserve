from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
import time
from time import sleep
from selenium.webdriver.support.select import Select
import mail_utils as MU
import global_vars


class AutoRes:
    chrome_options = webdriver.ChromeOptions()
    username = ''
    password = ''
    area = ''
    pos = ''
    start = ''
    end = ''
    
    def __init__(self,username,password,area,pos,start,end,cur_date):
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
        
    # 登录
    def login(self):
        try:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ': try to login ')
            self.driver.implicitly_wait(10)  # wait for the web page
            sleep(2)
            self.driver.get('https://uis.nbu.edu.cn/authserver/login?service=http://zizhu.nbu.edu.cn/loginall.aspx?page=')
            input_username = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.ID,'username')))
            input_password = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.ID,'password')))
            login_btn = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,'//form[@id="casLoginForm"]/p[4]/button')))
            input_username.send_keys(self.username)
            input_password.send_keys(self.password)
            sleep(5)
            input_password.submit()
            # login_btn.click()
            self.driver.implicitly_wait(10)  # wait for the web page
        except NoSuchElementException as e:
            raise
    
    # 预约
    def make_res(self):
        try:
            areas = self.driver.find_elements_by_class_name('it')
            # 打开区域
            for area in areas:
                if(area.text == self.area):
                    right_area = area
                    break
            right_area.click()
            sleep(5)
            # 选择预约时间
            date_ele = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,'fp-date')))
            # 选择日期
            date_ele.click()
            sleep(2)
            row = (self.cur_date + 5)/7 + 1
            col = (self.cur_date - 5)%7
            xpath = '//*[@id="ui-datepicker-div"]/table/tbody/tr[%d]/td[%d]' %(row,col)
            date_time = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,xpath)))
            date_time.click()
            # 选择预约时间
            cssh = '#ui-datepicker-div>div.ui-timepicker-div>dl>dd.ui_tpicker_hour>div>select'
            cssm = '#ui-datepicker-div>div.ui-timepicker-div>dl>dd.ui_tpicker_minute>div>select'
            #  h-8:21:1;  m-0:50:10
            start_ele = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,'fp-time-start')))
            self.selectTime(start_ele,int(self.start[:2]),int(self.start[2:]),cssh,cssm)
            end_ele = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,'fp-time-end')))
            self.selectTime(end_ele,int(self.end[:2]),int(self.end[2:]),cssh,cssm)
            self.driver.find_element_by_class_name('ui-datepicker-close').click()
            print('choose the time %s:%s-%s:%s successfully!' %(self.start[:2],self.start[2:],self.end[:2],self.end[2:]))
            # 选择座位
            poses = self.driver.find_elements_by_class_name("fp-dot")
            num = len(poses)
            rs = 0
            for i in range(0,num):
                pos = self.driver.find_elements_by_class_name("fp-dot")[i]
                titles = self.driver.find_elements_by_class_name("fp-dot")[i].get_attribute('data-original-title')
                if(self.area+self.pos == titles):
                    rs = i
                    break
            right_pos = self.driver.find_elements_by_class_name("fp-dot")[rs]
            key = right_pos.get_attribute('key')
            global_vars.set_values('key',key)  # 设置全局变量
            print(key)
            print('choose the ' + right_pos.get_attribute('data-original-title') + ' successfully!')
            sleep(3)
            # 预约
            right_pos.click()
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.ID,"ui-id-1")))
            st = self.start
            et = self.end
            if(self.start[0] == '0'):
                st = self.start[1:]
            if(self.end[0] == '0'):
                et = self.end[1:]
            self.driver.find_element_by_xpath("//select[@name='start_time']/option[@value='%s']" %st).click()
            self.driver.find_element_by_xpath("//select[@name='end_time']/option[@value='%s']" %et).click()
            sleep(3)
            submit_btn = self.driver.find_element_by_class_name('mt_sub_resv')
            submit_btn.click()
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.ID,'uni_confirm')))
        except Exception as e:
            raise


    # select下拉选框
    def selectTime(self,element,h,m,cssh,cssm):
        element.click()
        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.ID,'ui-datepicker-div')))
        hour = self.driver.find_element_by_css_selector(cssh)
        Select(hour).select_by_value(str(h))
        minute = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,cssm)))
        Select(minute).select_by_value(str(m))


def doLogin(dr):
    count_retry = 9  # retry count
    flag = False
    while(count_retry > 0 and not flag):
        try:
            dr.login()
            if(dr.driver.title == '宁波大学信息共享空间'):
                print(dr.username + ' login successfully! ')
                flag = True
        except NoSuchElementException as e:
            print(e)
            print('can not locate element, now start %d ...' %((10 - count_retry)))
            count_retry -= 1


def doRes(dr,email):
    count_retry = 9  # retry count
    flag = False
    while(count_retry > 0 and not flag):
        try:
            dr.driver.refresh()
            dr.make_res()
            if(dr.driver.find_element_by_css_selector('#uni_confirm>p').text == '申请提交成功，是否跳转查看预约信息?'):
                mail_util = MU.Mail_util()
                res_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                content = ' %s 预约%s-%s：%s-%s成功！' % (dr.username,dr.area,dr.pos,dr.start,dr.end)
                mail_util.send_email('图书馆预约通知',res_time + content,email)
                print(dr.username + ' reserve successfully! ')
                flag = True
        except Exception as e:
            print(e)
            print('can not reserve, now start %d ...' % ((10 - count_retry)))


def sign_in(driver,key,username,password,email,count=5):
    if(count == 0):
        return
    try:
        url = global_vars.get_value('url')
        driver.get(url)
        input_username = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.NAME,'szLogonName')))
        input_password = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.NAME,'szPassword')))
        login_btn = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME,'btn')))
        input_username.send_keys(username)
        input_password.send_keys(password)
        sleep(3)
        input_password.submit()
        sleep(3)
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.TAG_NAME,'button'))).click()
        flag = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.info>p'))).text
        sleep(3)
        if(flag[:4] == '签到成功'):
            mail_util = MU.Mail_util()
            mail_util.send_email('图书馆预约通知','签到成功了',email)
            print(username + ' signin successfully! ')
        else:
            sign_in(driver,key,username,password,email,count-1)
    except Exception as e:
        print(e)
        print('sign in fail,retrying ... ')
        sign_in(driver,key,username,password,email,count-1)
