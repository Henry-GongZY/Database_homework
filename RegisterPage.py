from tkinter import *
from tkinter.messagebox import showinfo
from pymysql import *

class RegisterPage(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (500, 300))  # 设置窗口大小
        self.username = StringVar()
        self.nickname = StringVar()
        self.password = StringVar()
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W, pady=20)
        Label(self.page, text='注册您的帐号',font=30).grid(row=1,pady=10)
        Label(self.page, text='昵称: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.nickname).grid(row=2, column=1, stick=E)
        Label(self.page, text='密码: ').grid(row=3, stick=W, pady=10)
        Entry(self.page, textvariable=self.password, show='*').grid(row=3, column=1, stick=E)
        Button(self.page, text='注册账号', command=self.doregister).grid(row=4, stick=E, column=2,pady=10)

    def doregister(self):
        conn = connect(host='127.0.0.1', user='root', password='123456', database='novelsystem', charset='utf8')
        cursor = conn.cursor()
        nickname = self.nickname.get()
        secret = self.password.get()
        if len(nickname)<=20 and len(secret)<=16:
           sql = 'select count(userid) from user;'
           cursor.execute(sql)
           m=(cursor.fetchone())[0]
           m+=1
           sql = 'insert into user values(%s,%s,%s,0,0);'
           cursor.execute(sql,(m,nickname,secret))
           conn.commit()
           cursor.close()
           conn.close()
           showinfo(title='注册成功', message='注册成功，请重新启动客户端以登录！')
           self.page.quit()
        else:
            showinfo(title='错误', message='用户名或密码字段过长！')

