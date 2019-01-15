from django.test import TestCase

# Create your tests here.
import ftplib

HOST = '172.16.53.113'
PORT = '2121'
user = 'admin'
password = '123456'


def connect():
    try:
        ftp = ftplib.FTP(HOST, PORT)
        ftp.login(user=user, passwd=password)
        print('已连接到："%s"' % HOST)
        return ftp
    except Exception as e:
        print('FTP登录失败，请检查主机号、用户名、密码是否正确', e)
        return None


def disconnect(ftp):
    ftp.quit()

if __name__ == '__main__':
    ftp = connect()