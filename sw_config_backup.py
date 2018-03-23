import paramiko
import time,os,sys,datetime

here = os.path.dirname(os.path.abspath(__file__))

#with open('devices.txt',"r") as f:
with open('devices_35srv.txt', "r") as f:
  credentials = [x.strip().split('\t') for x in f.readlines()]

for ip,username,password,name in credentials:
    remote_conn_pre=paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(ip,username=username,password=password,look_for_keys=False,allow_agent=False,port=22)
    remote_conn = remote_conn_pre.invoke_shell()
    remote_conn.send("\n")
    remote_conn.send("system-view\n")
    remote_conn.send("user-interface vty 0 15\n")
    remote_conn.send("screen-length 0\n")
    remote_conn.send("quit\n")
    remote_conn.send("info-center loghost 172.26.9.12\n")
    remote_conn.send("dis cu\n")
    time.sleep(5)
    remote_conn.send("save\n")
    remote_conn.send("y\n")
    remote_conn.send("\n")
    remote_conn.send("y\n")

    time.sleep(2)

    output = remote_conn.recv(65535)

    filename = name + str(datetime.date.today()) + '.txt'
    fullfilename = os.path.join(here,filename)

    try:
        fp = open(fullfilename)
        fp.write(output)
        fp.close()
    except IOError:
        fp = open(fullfilename,'w+')
        fp.write(output)
        fp.close()

    print output

    remote_conn.close()
