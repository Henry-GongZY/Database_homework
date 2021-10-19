from view import *  # 菜单栏对应的各个子页面

class MainPage(object):
    def __init__(self,info,master=None):
        self.information=info
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (500, 350))  #设置窗口大小
        self.createPage()

    def createPage(self):
        self.infoPage = InfoFrame(self.information,self.root)  # 创建不同Frame
        self.bookPage = BookFrame(self.information,self.root)
        self.commentPage = CommentFrame(self.information,self.root)
        self.cataPage = CataFrame(self.information,self.root)
        self.VIPPage = VIPFrame(self.information, self.root)
        self.infoPage.pack()  # 默认显示数据录入界面
        menubar = Menu(self.root)
        menubar.add_command(label='个人信息', command=self.infoData)
        menubar.add_command(label='书籍管理', command=self.bookData)
        menubar.add_command(label='评论管理', command=self.commentData)
        menubar.add_command(label='我的喜好', command=self.cataData)
        menubar.add_command(label='会员及充值服务', command=self.VIPData)
        self.root['menu'] = menubar  # 设置菜单栏

    def infoData(self):
        self.infoPage.pack()
        self.bookPage.pack_forget()
        self.commentPage.pack_forget()
        self.cataPage.pack_forget()
        self.VIPPage.pack_forget()

    def bookData(self):
        self.infoPage.pack_forget()
        self.bookPage.pack()
        self.commentPage.pack_forget()
        self.cataPage.pack_forget()
        self.VIPPage.pack_forget()

    def commentData(self):
        self.infoPage.pack_forget()
        self.bookPage.pack_forget()
        self.commentPage.pack()
        self.cataPage.pack_forget()
        self.VIPPage.pack_forget()

    def cataData(self):
        self.infoPage.pack_forget()
        self.bookPage.pack_forget()
        self.commentPage.pack_forget()
        self.cataPage.pack()
        self.VIPPage.pack_forget()

    def VIPData(self):
        self.infoPage.pack_forget()
        self.bookPage.pack_forget()
        self.commentPage.pack_forget()
        self.cataPage.pack_forget()
        self.VIPPage.pack()