import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.header import Header
import smtplib
import time
from time import sleep


class Mail_util:
    # 发件人地址，通过控制台创建的发件人地址
    __username = 'xxx'
    # 发件人密码，通过控制台创建的发件人密码
    __password = 'xxx'
    __replyto = 'xxx'

    def __init__(self):
        super()

    # 发送邮件
    def send_email(self,header,content,receiver,ssl=0):
        nums_flag = len(receiver)  # 发送邮件列表长度
        rcptto = ''
        if(nums_flag <= 0):
            return
        elif(nums_flag == 1):
            rcptto = receiver[0]
        else:
            rcptto = ','.join(rcptto)
        # 构建alternative结构
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header(header).encode()
        msg['From'] = '%s <%s>' % (Header('Jyccc').encode(), self.__username)
        msg['To'] = rcptto
        msg['Reply-to'] = self.__replyto
        msg['Message-id'] = email.utils.make_msgid()
        msg['Date'] = email.utils.formatdate()
        # 构建alternative的text/plain部分
        textplain = MIMEText(content, _subtype='plain', _charset='UTF-8')
        msg.attach(textplain)
        # 发送邮件
        try:
            if(ssl == 1):  # 若需要使用SSL
                client = smtplib.SMTP_SSL()
            else:
                client = smtplib.SMTP()
            # SMTP普通端口为25或80：阿里云服务器需要设置为80端口
            client.connect('smtpdm.aliyun.com', 80)
            client.login(self.__username, self.__password)
            if(nums_flag == 1):  # 单封
                client.sendmail(self.__username, rcptto, msg.as_string())
            else:
                client.sendmail(self.__username, receiver, msg.as_string())
            client.quit()
            print('邮件发送成功！')
        except smtplib.SMTPConnectError as e:
            print('邮件发送失败，连接失败:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPAuthenticationError as e:
            print('邮件发送失败，认证错误:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPSenderRefused as e:
            print('邮件发送失败，发件人被拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPRecipientsRefused as e:
            print('邮件发送失败，收件人被拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPDataError as e:
            print('邮件发送失败，数据接收拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPException as e:
            print('邮件发送失败, ', e.message)
        except Exception as e:
            print('邮件发送异常, ', str(e))
            print("Error: 无法发送邮件")
