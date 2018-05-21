#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
 
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
 
class MailHelper:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def sendmail(self, mail_to, subject, content):
        try:
            msg = MIMEText(content,'plain','utf-8')
            mail_to = mail_to.split(',')
            msg['From'] = formataddr(["your nickname", self.username]) # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['Subject'] = subject # 邮件的主题，也可以说是标题
            server = smtplib.SMTP("your smtp server", 587) # 发件人邮箱中的SMTP服务器，端口是25
            server.starttls()
            server.login(self.username, self.password) # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(self.username, mail_to, msg.as_string()) # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit() # 关闭连接
        except Exception as ex:
            print(ex.args)
            print(ex.value)
 
if __name__ == "__main__":
    mh = MailHelper('your mailbox', 'you mailbox password')
    mh.sendmail('mailto mailboxs', 'subject', '这只是一个测试邮件,请不要回复!')