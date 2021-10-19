from datetime import *
from tkinter.messagebox import showinfo
from pymysql import *
from tkinter import *
from tkinter import ttk

class InfoFrame(Frame):
    def __init__(self, info, master=None):
        Frame.__init__(self, master)
        self.information = info
        self.root = master
        self.createPage()

    def createPage(self):
        conn = connect(host='127.0.0.1', user='root', password='123456', database='novelsystem', charset='utf8')
        cursor = conn.cursor()
        Label(self).grid(row=0, stick=W, pady=10)
        Label(self, text='您的昵称: ').grid(row=1, stick=W, pady=10)
        Label(self, text=self.information[1]).grid(row=1, column=1, stick=E)
        Label(self, text='您的用户账号:').grid(row=2, stick=W, pady=10)
        Label(self, text=self.information[0]).grid(row=2, column=1, stick=E)
        sql="select coin from user where userid = %s"
        cursor.execute(sql,self.information[0])
        Label(self, text='您的金币: ').grid(row=3, stick=W, pady=10)
        Label(self, text=(cursor.fetchone())[0]).grid(row=3, column=1, stick=E)
        sql="select VIPornot from user where userid = %s"
        cursor.execute(sql, self.information[0])
        fetch = cursor.fetchone()[0]
        if fetch == True:
            Label(self, text='您是尊贵的VIP用户，可以免费阅读所有电子读物。').grid(row=4, stick=W, pady=10)
        else:
            Label(self, text='您不是VIP用户，充值VIP享受更多权益。').grid(row=4, stick=W, pady=10)
        cursor.close()
        conn.close()
        Button(self, text='退出', command=self.quit).grid(row=5, stick=E, pady=10)

class BookFrame(Frame):  # 继承Frame类
    def __init__(self, info, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.information = info
        self.bookname = StringVar()
        self.ckall = BooleanVar(value=False)
        self.createPage()

    def createPage(self):
        Label(self).grid(row=0, stick=W, pady=10)
        Label(self, text='书籍检索（按照书名）: ').grid(row=2, stick=W, pady=10)
        Entry(self, textvariable=self.bookname).grid(row=2, column=1, stick=E)
        Button(self, text='所有书籍', command=self.checkall).grid(row=3, stick=W, pady=10)
        Button(self, text='检索', command=self.checksome).grid(row=3, column=2,stick=E, pady=10)
        Checkbutton(self, text="仅显示我能借阅的书籍",variable = self.ckall).grid(row=4, stick=W, pady=10)
        Button(self, text='我正在阅读的书籍', command=self.minebook).grid(row=5, column=2, stick=E, pady=10)

    def minebook(self):
        conn = connect(host='127.0.0.1', user='root', password='123456', database='novelsystem', charset='utf8')
        cursor = conn.cursor()
        sql = "select novelid,novelname,writter,catagory from novels natural join readhistory where userid = %s"
        cursor.execute(sql,self.information[0])
        fetch = cursor.fetchall()
        cursor.close()
        conn.close()
        temp = Tk()
        temp.title('书籍目录')
        tree = ttk.Treeview(temp, height=len(fetch), columns=["书籍编号", "书籍名称", "作者", "书籍分类"], show="headings")
        tree.heading("书籍编号", text="书籍编号")
        tree.heading("书籍名称", text="书籍名称")
        tree.heading("作者", text="作者")
        tree.heading("书籍分类", text="书籍分类")
        tree.column("书籍编号", anchor="center")
        tree.column("书籍名称", anchor="center")
        tree.column("作者", anchor="center")
        tree.column("书籍分类", anchor="center")
        for i in range(0, len(fetch)):
            tree.insert('', 'end', values=fetch[i])
        tree.pack(side=LEFT, fill=BOTH)

    def checkall(self):
        m = self.ckall.get()
        conn = connect(host='127.0.0.1', user='root', password='123456', database='novelsystem', charset='utf8')
        cursor = conn.cursor()
        if(m==True):
            sql = "select VIPornot from user where userid = %s"
            cursor.execute(sql, self.information[0])
            k=(cursor.fetchone())[0]
            if(k==1):
                cursor = conn.cursor()
                sql="select novelid,novelname,writter,catagory from novels where novelid not in (select novelid from readhistory where userid = %s)"
                cursor.execute(sql,self.information[0])
                fetch=cursor.fetchall()
                temp = Tk()
                temp.title('书籍目录')
                tree = ttk.Treeview(temp,height=len(fetch), columns=["书籍编号","书籍名称","作者","书籍分类"],show="headings")
                tree.heading("书籍编号", text="书籍编号")
                tree.heading("书籍名称", text="书籍名称")
                tree.heading("作者", text="作者")
                tree.heading("书籍分类", text="书籍分类")
                tree.column("书籍编号", anchor="center")
                tree.column("书籍名称", anchor="center")
                tree.column("作者", anchor="center")
                tree.column("书籍分类", anchor="center")
                for i in range(0,len(fetch)):
                    tree.insert('','end',values=fetch[i])
                tree.pack(side=LEFT, fill=BOTH)
            else:
                sql = "select novelid,novelname,writter,catagory from novels where novelid not in (select novelid from readhistory where userid = %s) and VIPbookornot = False"
                cursor.execute(sql,self.information[0])
                fetch = cursor.fetchall()
                temp = Tk()
                temp.title('书籍目录')
                tree = ttk.Treeview(temp, height=len(fetch), columns=["书籍编号", "书籍名称", "作者", "书籍分类"], show="headings")
                tree.heading("书籍编号", text="书籍编号")
                tree.heading("书籍名称", text="书籍名称")
                tree.heading("作者", text="作者")
                tree.heading("书籍分类", text="书籍分类")
                tree.column("书籍编号", anchor="center")
                tree.column("书籍名称", anchor="center")
                tree.column("作者", anchor="center")
                tree.column("书籍分类", anchor="center")
                for i in range(0, len(fetch)):
                    tree.insert('', 'end', values=fetch[i])
                tree.pack(side=LEFT, fill=BOTH)
        else:
            sql = "select novelid,novelname,writter,catagory from novels where novelid not in (select novelid from readhistory where userid = %s)"
            cursor.execute(sql, self.information[0])
            fetch = cursor.fetchall()
            temp = Tk()
            temp.title('书籍目录')
            tree = ttk.Treeview(temp, height=len(fetch), columns=["书籍编号", "书籍名称", "作者", "书籍分类"], show="headings")
            tree.heading("书籍编号", text="书籍编号")
            tree.heading("书籍名称", text="书籍名称")
            tree.heading("作者", text="作者")
            tree.heading("书籍分类", text="书籍分类")
            tree.column("书籍编号", anchor="center")
            tree.column("书籍名称", anchor="center")
            tree.column("作者", anchor="center")
            tree.column("书籍分类", anchor="center")
            for i in range(0, len(fetch)):
                tree.insert('', 'end', values=fetch[i])
            tree.pack(side=LEFT, fill=BOTH)
        cursor.close()
        conn.close()
    def checksome(self):
        n = self.bookname.get()
        m = self.ckall.get()
        conn = connect(host='127.0.0.1', user='root', password='123456', database='novelsystem', charset='utf8')
        cursor = conn.cursor()
        if (m == True):
            sql = "select VIPornot from user where userid = %s"
            cursor.execute(sql, self.information[0])
            k = (cursor.fetchone())[0]
            if (k == 1):
                cursor = conn.cursor()
                sql = "select novelid,novelname,writter,catagory from novels where novelid not in (select novelid from readhistory where userid = %s) and novelname = %s"
                cursor.execute(sql, [self.information[0],n])
                fetch = cursor.fetchall()
                temp = Tk()
                temp.title('书籍目录')
                tree = ttk.Treeview(temp, height=len(fetch), columns=["书籍编号", "书籍名称", "作者", "书籍分类"], show="headings")
                tree.heading("书籍编号", text="书籍编号")
                tree.heading("书籍名称", text="书籍名称")
                tree.heading("作者", text="作者")
                tree.heading("书籍分类", text="书籍分类")
                tree.column("书籍编号", anchor="center")
                tree.column("书籍名称", anchor="center")
                tree.column("作者", anchor="center")
                tree.column("书籍分类", anchor="center")
                for i in range(0, len(fetch)):
                    tree.insert('', 'end', values=fetch[i])
                tree.pack(side=LEFT, fill=BOTH)
            else:
                sql = "select novelid,novelname,writter,catagory from novels where novelid not in (select novelid from readhistory where userid = %s) and VIPbookornot = False and novelname = %s"
                cursor.execute(sql, [self.information[0],n])
                fetch = cursor.fetchall()
                temp = Tk()
                temp.title('书籍目录')
                tree = ttk.Treeview(temp, height=len(fetch), columns=["书籍编号", "书籍名称", "作者", "书籍分类"], show="headings")
                tree.heading("书籍编号", text="书籍编号")
                tree.heading("书籍名称", text="书籍名称")
                tree.heading("作者", text="作者")
                tree.heading("书籍分类", text="书籍分类")
                tree.column("书籍编号", anchor="center")
                tree.column("书籍名称", anchor="center")
                tree.column("作者", anchor="center")
                tree.column("书籍分类", anchor="center")
                for i in range(0, len(fetch)):
                    tree.insert('', 'end', values=fetch[i])
                tree.pack(side=LEFT, fill=BOTH)
        else:
            sql = "select novelid,novelname,writter,catagory from novels where novelid not in (select novelid from readhistory where userid = %s) and novelname = %s"
            cursor.execute(sql, [self.information[0], n])
            fetch = cursor.fetchall()
            temp = Tk()
            temp.title('书籍目录')
            tree = ttk.Treeview(temp, height=len(fetch), columns=["书籍编号", "书籍名称", "作者", "书籍分类"], show="headings")
            tree.heading("书籍编号", text="书籍编号")
            tree.heading("书籍名称", text="书籍名称")
            tree.heading("作者", text="作者")
            tree.heading("书籍分类", text="书籍分类")
            tree.column("书籍编号", anchor="center")
            tree.column("书籍名称", anchor="center")
            tree.column("作者", anchor="center")
            tree.column("书籍分类", anchor="center")
            for i in range(0, len(fetch)):
                tree.insert('', 'end', values=fetch[i])
            tree.pack(side=LEFT, fill=BOTH)
        cursor.close()
        conn.close()

class CommentFrame(Frame):  # 继承Frame类
    def __init__(self, info, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.inforation = info
        self.bookid = StringVar()
        self.text = Text(self, width=60, height=15)
        self.createPage()

    def createPage(self):
        self.text.grid(row=1)
        Label(self, text='请输入您想评论书籍的编号: ').grid(row=2, stick=W, pady=20)
        Entry(self, textvariable=self.bookid).grid(row=2, stick=E, pady=20)
        Button(self, text='发表评论', command=self.input).grid(row=3, stick=E, pady=10)

    def input(self):
        k = self.text.get('0.0',END)
        p = self.bookid.get()
        conn = connect(host='127.0.0.1', user='root', password='123456', database='novelsystem', charset='utf8')
        cursor = conn.cursor()
        if(len(p)==0):
            showinfo(title='错误', message='未输入图书编号！')
        else:
            sql = 'select novelid from readhistory where userid = %s and novelid = %s'
            cursor.execute(sql,[self.inforation[0],p])
            fetch = cursor.fetchone()
            if(fetch==None):
                showinfo(title='错误', message='您没有阅读过这本图书，请阅读后给予评论！')
            else:
                dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                sql = 'insert into comments values(%s,%s,%s,%s)'
                cursor.execute(sql,(self.inforation[0],p,dt,k))
                conn.commit()
                cursor.close()
                conn.close()
                showinfo(title='评论成功！', message='感谢您的评论！')

class CataFrame(Frame):  # 继承Frame类
    def __init__(self, info, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.information = info
        self.createPage()

    def createPage(self):
        Label(self, text='我喜欢的作者：').grid(row=2, stick=W, column = 1,pady=20)
        Button(self, text='获取',command = self.goto1).grid(row=2, stick=E, column = 2,pady=20)
        Label(self, text='我喜欢的书籍类别：').grid(row=3, stick=W, column=1, pady=20)
        Button(self, text='获取', command=self.goto2).grid(row=3, stick=E, column=2, pady=20)
    def goto1(self):
        temp=Tk()
        temp.title('我喜欢的作者')
        conn = connect(host='127.0.0.1', user='root', password='123456', database='novelsystem', charset='utf8')
        cursor = conn.cursor()
        sql = "select writter,count(writter) as number from favouritewritter where userid = %s group by writter order by number desc"
        cursor.execute(sql,self.information[0])
        fetch = cursor.fetchall()
        tree = ttk.Treeview(temp, height=len(fetch), columns=["作者", "书籍数目"], show="headings")
        tree.heading("作者", text="作者")
        tree.heading("书籍数目", text="书籍数目")
        tree.column("作者", anchor="center")
        tree.column("书籍数目", anchor="center")
        for i in range(0, len(fetch)):
            tree.insert('', 'end', values=fetch[i])
        tree.pack(side=LEFT, fill=BOTH)
        cursor.close()
        conn.close()
    def goto2(self):
        temp=Tk()
        temp.title('我喜欢的书籍类别')
        conn = connect(host='127.0.0.1', user='root', password='123456', database='novelsystem', charset='utf8')
        cursor = conn.cursor()
        sql = "select catagory,count(catagory) as number from favouritecatagory where userid = %s group by catagory order by number desc"
        cursor.execute(sql,self.information[0])
        fetch = cursor.fetchall()
        tree = ttk.Treeview(temp, height=len(fetch), columns=["类别", "书籍数目"], show="headings")
        tree.heading("类别", text="类别")
        tree.heading("书籍数目", text="书籍数目")
        tree.column("类别", anchor="center")
        tree.column("书籍数目", anchor="center")
        for i in range(0, len(fetch)):
            tree.insert('', 'end', values=fetch[i])
        tree.pack(side=LEFT, fill=BOTH)
        cursor.close()
        conn.close()

class VIPFrame(Frame):  # 继承Frame类
    def __init__(self, info, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.inforation = info
        self.number = IntVar()
        self.monthnum = IntVar()
        self.createPage()

    def createPage(self):
        Label(self, text='').grid(row=1, stick=W, column=1, pady=10)
        Label(self, text='充值金币').grid(row=2, stick=W, column=1, pady=10)
        Entry(self, textvariable=self.number).grid(row=2, column=2, stick=E, pady=10)
        Button(self, text='充值', command=self.goto1).grid(row=3, stick=E, column=2, pady=10)
        conn = connect(host='127.0.0.1', user='root', password='123456', database='novelsystem', charset='utf8')
        cursor = conn.cursor()
        sql="select VIPenddate from VIP where userid = %s"
        cursor.execute(sql,self.inforation[0])
        fetch = cursor.fetchone()
        if(fetch==None):
            Label(self, text='您未充值VIP或VIP已过期！').grid(row=4, stick=W, column=1, pady=10)
        else:
            k = fetch[0]
            Label(self, text='VIP截止日期：'+ k.strftime("%Y-%m-%d %H:%M:%S")).grid(row=4, stick=W, column=1, pady=10)
        Label(self, text='充值VIP(15金币/月)：').grid(row=5, stick=W, column=1, pady=10)
        Entry(self,textvariable = self.monthnum).grid(row=5, stick=W, column=2, pady=10)
        Button(self, text='充值', command=self.goto2).grid(row=6, stick=E, column=2, pady=10)
        Label(self, text='续费一个月VIP(10金币)：').grid(row=7, stick=W, column=1, pady=10)
        Button(self, text='续费', command=self.goto3).grid(row=7, stick=E, column=2, pady=10)
        cursor.close()
        conn.close()

    def goto1(self):
        conn = connect(host='127.0.0.1', user='root', password='123456', database='novelsystem', charset='utf8')
        cursor = conn.cursor()
        number = self.number.get()
        sql = "update user set coin = %s +(select coin from user where userid = %s) where userid = %s"
        cursor.execute(sql,[number,self.inforation[0],self.inforation[0]])
        conn.commit()
        cursor.close()
        conn.close()
        showinfo(title='提示', message='您已充值成功！')

    def goto2(self):
        conn = connect(host='127.0.0.1', user='root', password='123456', database='novelsystem', charset='utf8')
        cursor = conn.cursor()
        monthnum = self.monthnum.get()
        sql = "insert into VIP values(%s,now() + interval %s MONTH)"
        try:
            cursor.execute(sql,[self.inforation[0],monthnum])
            conn.commit()
            showinfo(title='充值成功！', message='感谢您的支持！')
        except Exception:
            showinfo(title='充值失败！', message='您没有足够的金币！')
            conn.rollback()
            cursor.close()
            conn.close()

    def goto3(self):
        conn = connect(host='127.0.0.1', user='root', password='123456', database='novelsystem', charset='utf8')
        cursor = conn.cursor()
        sql = "select vipornot from user where userid = %s"
        cursor.execute(sql,self.inforation[0])
        if (cursor.fetchall())[0][0]==0:
            showinfo(title = '抱歉',message = '您不是VIP，不能享受价格优惠续费服务！')
        else:
            m = 0
            cursor.callproc("renewtime",[self.inforation[0],m])
            sql = "select @_renewtime_1"
            cursor.execute(sql)
            m = (cursor.fetchone())[0]
            if m<0:
                showinfo(title='续费失败！', message='您没有足够的金币！')
            else:
                showinfo(title='续费成功！', message='感谢您的支持！')
            cursor.close()
            conn.close()