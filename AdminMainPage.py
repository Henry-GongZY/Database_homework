from Adminview import *
class AdminMainPage(object):
    def __init__(self,info,master=None):
        self.information=info
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (500, 350))  # 设置窗口大小
        self.createPage()

    def createPage(self):
        self.infoPage = InfoFrame(self.information,self.root)
        self.infoPage.pack()