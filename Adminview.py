from tkinter import *
from tkinter.messagebox import showinfo
from pymysql import *

class InfoFrame(Frame):
    def __init__(self, info, master=None):
        Frame.__init__(self, master)
        self.information = info
        self.root = master
        self.usernum=IntVar()
        self.createPage()

    def createPage(self):
        Label(self).grid(row=1, stick=W, pady=10)
        Label(self,text='注销账号(输入其账号）').grid(row=2, stick=W, pady=10)
        Entry(self,textvariable=self.usernum).grid(row=3, column=1,stick=W, pady=10)
        Button(self,text = '注销',command = self.deleteuser).grid(row=4, column = 2,stick=E, pady=10)

    def deleteuser(self):
        num = self.usernum.get()
        conn = connect(host='127.0.0.1', user='root', password='123456', database='novelsystem', charset='utf8')
        cursor = conn.cursor()
        sql_1='delete from user where userid = %s'
        sql_2='delete from VIP where userid = %s'
        sql_3='delete from readhistory where userid = %s'
        sql_4='delete from comments where userid = %s'
        try:
            cursor.execute(sql_2,num)
            cursor.execute(sql_3,num)
            cursor.execute(sql_4,num)
            cursor.execute(sql_1, num)
        except Exception as e:
            conn.rollback()  # 事务回滚
            showinfo(title='事务处理失败', message = e)
        else:
            conn.commit()  # 事务提交
            if cursor.rowcount==0:
                showinfo(title='错误',message='账号不存在！')   # 没有完成行的更改，即没有做删除操作
            else:
                showinfo(title='事务处理成功', message ='账号已删除！')
            cursor.close()
            conn.close()