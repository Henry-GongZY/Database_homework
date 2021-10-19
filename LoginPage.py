from MainPage import *
from RegisterPage import *
from AdminMainPage import *

class LoginPage(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (500, 300))  # 设置窗口大小
        self.userid = StringVar()
        self.password = StringVar()
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W,pady=20)
        Label(self.page, text='用户名: ').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.userid).grid(row=1, column=1, stick=E)
        Label(self.page, text='密码: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.password, show='*').grid(row=2, column=1, stick=E)
        Button(self.page, text='用户登陆', command=self.loginCheck).grid(row=3,stick=W,pady=10)
        Button(self.page, text='管理员登陆', command=self.admincheck).grid(row=3, stick=W, pady=10,column=1)
        Button(self.page, text='用户注册', command=self.register).grid(row=3,pady=10,stick=E,column=2)

    def loginCheck(self):
        name = self.userid.get()
        secret = self.password.get()
        conn = connect(host='127.0.0.1', user='root', password='123456', database='novelsystem', charset='utf8')
        cursor = conn.cursor()
        sql = 'select userid,username from user where username = %s and password = %s;'
        cursor.execute(sql,(name,secret))
        fetch = cursor.fetchone()
        if fetch != None:
            self.page.destroy()
            cursor.close()
            conn.close()
            MainPage(fetch,self.root)
        else:
            showinfo(title='错误', message='用户名或密码错误！')
    def register(self):
        self.page.destroy()
        RegisterPage(self.root)
    def admincheck(self):
        conn = connect(host='127.0.0.1', user='root', password='123456', database='novelsystem', charset='utf8')
        cursor = conn.cursor()
        name = self.userid.get()
        secret = self.password.get()
        sql = 'select adminid,adminname from administrator where adminname = %s and adminpassword = %s;'
        cursor.execute(sql,(name,secret))
        fetch = cursor.fetchone()
        if(fetch != None):
            self.page.destroy()
            cursor.close()
            conn.close()
            AdminMainPage(fetch, self.root)
        else:
            showinfo(title='错误', message='用户名或密码错误！')