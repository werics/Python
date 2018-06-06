#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import os,sys,re
import time
import paramiko
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import netsnmp

ISOTIMEFORMAT="%Y-%m-%d %X"

def modify_isproute_weight(isp,weights):
    isps = ['asd','szvpn','cu']
    if not isp in isps:
        return False
    if not isinstance(weights,int):
        return False
    try:
        remote_conn_pre=paramiko.SSHClient()
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_conn_pre.connect('1.1.1.1',username='username',password='password',look_for_keys=False,port=32200)
        remote_conn = remote_conn_pre.invoke_shell()
        time.sleep(1)
        remote_conn.send('config\n')
        time.sleep(1)
        remote_conn.send('ip vrouter trust-vr\n')
        time.sleep(1)
        if isp=='asd':
            exec_command = 'ip route "ChinaIP" 2.2.2.2 weight '+str(weights)+'\n'
            print exec_command
            remote_conn.send(exec_command)
        elif isp=='szvpn':
            exec_command = 'ip route 0.0.0.0/0 3.3.3.3 weight '+str(weights)+'\n'
            print exec_command
            remote_conn.send(exec_command)
        elif isp=='cu':
            exec_command = 'ip route "ChinaIP" 4.4.4.4 weight '+str(weights)+'\n'
            print exec_command
            remote_conn.send(exec_command)
        remote_conn.close()
    except Exception,e:
        print e
        return False

def get_isproute_weight(isp):
    isps = ['asd','szvpn','cu']
    if not isp in isps:
        return False
    if isp == 'asd':
        gw_ip = re.compile(r'.*2.2.2.2.*')
    elif isp == 'szvpn':
        gw_ip = re.compile(r'.*3.3.3.3.*')
    elif isp == 'cu':
        gw_ip = re.compile(r'.*4.4.4.4.*')
    try:
        remote_conn_pre=paramiko.SSHClient()
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_conn_pre.connect('1.1.1.1',username='username',password='password',look_for_keys=False,port=32200)
        remote_conn = remote_conn_pre.invoke_shell()
        time.sleep(1)
        if isp == 'asd' or isp == 'cu':
            remote_conn.send('show ip route 114.114.114.114\n')
        elif isp == 'szvpn':
            remote_conn.send('show ip route 0.0.0.0\n')
        time.sleep(1)
        output = remote_conn.recv(65535)
        remote_conn.close()
        if output is None:
            return False
        else:
            for xx in output.splitlines():
                if gw_ip.search(xx):
                    weight = re.split(r'[\s\,]+',xx)
                    num = int(weight[2].replace('[','').replace(']','').split('/')[2])
                    return num
    except Exception,e:
        print e
        return False

def isnumber(weight):
    if weight is not None:
        if weight.isdigit():
            if isinstance(int(weight),int):
                if int(weight)>0 and int(weight)<256:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def redstr(redstr):
    print "\033[1;31m%s\033[0m"%redstr

def greenstr(greenstr,weight):
    print "\033[1;32m%s%d\033[0m"%(greenstr,weight)


M0=True
while M0:
    print ("""\033[1;35m
   
    1.检查线路路由权重

    2.修改线路路由权重
  
    请选择对应的操作。

    退出请按回车键\033[0m
    """)
    M0=raw_input("请输入相应的操作序号：")
    if M0=="1":
        M1=True
        while M1:
            print ("""\033[1;35m
   
            1.检查奥斯达路由权重

            2.检查联通路由权重

            3.检查SZVPN国际路由权重

            4.返回上层菜单
  
            请选择对应的操作。\033[0m
            """)
            M1=raw_input("请输入操作编号：")
            if M1=="1":
                asd_weight = get_isproute_weight('asd')
                if asd_weight is False:
                    redstr('获取路由权重出错!')
                else:
                    greenstr('奥斯达路由权重为: ',asd_weight)
            elif M1=="2":
                cu_weight = get_isproute_weight('cu')
                if cu_weight is False:
                    redstr('获取路由权重出错!')
                else:
                    greenstr('联通路由权重为: ',cu_weight)
            elif M1=="3":
                szvpn_weight = get_isproute_weight('szvpn')
                if szvpn_weight is False:
                    redstr('获取路由权重出错!')
                else:
                    greenstr('联通路由权重为: ',szvpn_weight)
            elif M1=="4":
                break
            elif M1 !="":
                redstr('无效输入请重试!')
    if M0=="2":
        M2=True
        while M2:
            print ("""\033[1;35m
   
            1.奥斯达线路

            2.合规联通线路

            3.SZVPN国际线路

            4.返回上层菜单
    
            请选择相应的线路编号修改流量权重。

            退出请按回车键\033[0m
            """)
            M2=raw_input("请输入线路编号:") 
            if M2=="1":
                passwd=raw_input("请输入密码:")
                if passwd=="it@yy.com":
                    asd_weight=raw_input("请输入路由权重数值(1-255的整数):")
                    if isnumber(asd_weight):
                        asd_route = modify_isproute_weight('asd', int(asd_weight))
                        if asd_route is False:
                            redstr('奥斯达线路权重修改出错！请联系管理员')
                        else:
                            greenstr('奥斯达线路权重修改为: ',int(asd_weight))
                    else:
                        redstr('线路路由权重输入错误')
                else:
                    redstr('密码输入错误，已退出')
                    break
            elif M2=="2":
                passwd=raw_input("请输入密码:")
                if passwd=="it@yy.com":
                    cu_weight=raw_input("请输入路由权重数值(1-255的整数):")
                    if isnumber(cu_weight):
                        cu_route = modify_isproute_weight('cu',int(cu_weight))
                        if cu_route is False:
                            redstr('联通线路权重修改出错！请联系管理员')
                        else:
                            greenstr('合规联通线路权重修改为：',int(cu_weight))
                    else:
                        redstr('线路路由权重输入错误')
                else:
                    redstr('密码输入错误，已退出')
                    break
            elif M2=="3":
                passwd=raw_input("请输入密码:")
                if passwd=="it@yy.com":
                    szvpn_weight=raw_input("请输入路由权重数值(1-255的整数):")
                    if isnumber(szvpn_weight):
                        szvpn_route = modify_isproute_weight('szvpn',int(szvpn_weight))
                        if szvpn_route is False:
                            redstr('SZVPN国际线路权重修改出错！请联系管理员')
                        else:
                            greenstr('SZVPN国际线路权重修改为：',int(szvpn_weight))
                    else:
                        redstr('线路路由权重输入错误')
                else:
                    redstr('密码输入错误，已退出')
                    break
            elif M2=="4":
                break
            elif M2 !="":
                redstr('无效输入请重试!')

