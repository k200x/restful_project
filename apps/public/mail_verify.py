# coding=utf-8
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib,random
from email.mime.text import MIMEText


class MailVerify(object):
    def __init__(self):
        self.msg_from = '13671387369@163.com' # 发送方邮箱
        self.passwd = 'z19890315'  # 填入发送方邮箱的授权码
        self.server = "smtp.163.com"
        self.port = 465
        self.name = "官方邮件"

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def mail_format(self, subject, content, recipient):
        msg = MIMEText(content, _charset="utf-8")
        msg['From'] = self._format_addr(u"%s <%s>" % (self.name, self.msg_from))
        msg['Subject'] = subject
        msg['To'] =recipient
        return msg

    def send_mail(self, subject, content, recipient):
        try:
            msg = self.mail_format(subject, content, recipient)
            s = smtplib.SMTP_SSL(self.server, self.port)  # 邮件服务器及端口号
            s.login(self.msg_from, self.passwd)
            s.sendmail(self.msg_from, recipient, msg.as_string())
            print("成功")
        except Exception as e:
            print("失败", e)
        finally:
            s.quit()


if __name__ == '__main__':
    mail_obj = MailVerify()
    subject = "密码找回验证码"
    content = "验证码为:%d,将在1min后失效"%random.randint(0,9999)
    recipient = "z675701527@126.com"
    mail_obj.send_mail(subject=subject,content=content,recipient=recipient)
