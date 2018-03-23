#! /usr/bin/python

import dns.query
import dns.message
import dns.resolver
import re,sys
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import os
import socket, fcntl, struct


def get_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

def sendmail():
    sender = "xx@xxx.com"
    password = "xxxxxxxxx"
    smtp_server = "mail.xxx.com"
    body = get_ip('eth0')+' YYDNS was down, please check'
    msg = MIMEText(body,_subtype='plain',_charset='utf-8')
    msg['From'] = "xx@xxx.com"
    msg['To'] = "xx1@xxx.com,xx2@xxx.com"
    msg['Subject'] = Header("YYDNS down").encode()
    server = smtplib.SMTP(smtp_server,25)
    #server.set_debuglevel(1)
    server.login(sender,password)
    server.sendmail(sender,msg['To'].split(","),msg.as_string())
    server.quit()


dm = dns.message.make_query('www.qq.com','A')

try:
    result = dns.query.udp(dm,'172.26.9.9',timeout=10,port=5553)
except:
    sendmail()


#comment = re.compile(r'www.qq.com.\s\d+\sIN\sA\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

#if not comment.findall(result.to_text()):
#    sendmail()
