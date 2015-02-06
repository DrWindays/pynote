#!/usr/bin/python
# -*- coding:utf-8 -*-

'''

----------------------------------------------------
#2015-2-6 windays

设置行高
注意 一定要移动textcursor到下一个block 否则只会修改第一个block的format

#2015-2-5 windays
界面构成

便笺为任意的dialog类型的无边框子窗口，标题栏为自己绘制
程序拥有一个父窗口，只显示一个像素在左上角，用来辅助实现
任务栏的效果，任务栏只有一个任务窗口，并且关闭任务栏会关闭
所有子便笺窗口，点击任务栏进程使所有子窗口处于top-level

加入logging机制

设置行高
----------------------------------------------------

'''

import sys,os
from PyQt4 import QtGui, QtCore
from datetime import datetime

import logging,logging.handlers

class TitleBar(QtGui.QWidget):
    def __init__(self,parent):
        super(TitleBar, self).__init__()
        self.parent = parent
        self.Init()        

    def Init(self):
        
        self.setObjectName("titlebar")
        self.setAutoFillBackground(True)
          

        self.newwindow = QtGui.QToolButton()
        self.close = QtGui.QToolButton()
        
        pix = self.style().standardPixmap(QtGui.QStyle.SP_TitleBarCloseButton)
        self.close.setIcon(QtGui.QIcon(pix))

        pix = self.style().standardPixmap(QtGui.QStyle.SP_TitleBarMaxButton)
        self.newwindow.setIcon(QtGui.QIcon(pix))

        self.close.setObjectName('closeButton')
        self.newwindow.setObjectName('newwindowButton')

        self.close.setFixedSize(20, 20)
        self.newwindow.setFixedSize(20, 20)

        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addWidget(self.close,0,QtCore.Qt.AlignLeft)

        #self.hbox.addStretch(0)
        self.hbox.addWidget(self.newwindow)

        self.setLayout(self.hbox)

        self.hbox.setContentsMargins(5, 4, 5, 4)
        self.hbox.setSpacing(0)
        #self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)

        pl = QtGui.QPalette()
        pl.setColor(QtGui.QPalette.Background, QtGui.QColor(197,247,193))
        
        self.setPalette(pl)
        
        self.setStyleSheet('QToolButton{background-color:rgb(0,0,0,0);}QToolButton::hover{border:1px solid gray;border-radius:2px}')

        self.maxNormal = False

        self.connect(self.close, QtCore.SIGNAL( 'clicked()'), self.closeButtonClicked)
        self.connect(self.newwindow, QtCore.SIGNAL('clicked()'), self.parent.windowManager.createWindow)


    def mousePressEvent(self, event):
        self.startPos = event.globalPos()
        self.clickPos = self.mapToParent(event.pos())

    def mouseMoveEvent(self, event):
        if self.maxNormal == True:
            return
        self.parent.move(event.globalPos() - self.clickPos)

    def closeButtonClicked(self):
        self.parent.windowManager.closeWindow(self.parent)

class BottomBar(QtGui.QWidget):
    def __init__(self,parent):
        super(BottomBar, self).__init__()
        self.parent = parent
        self.hbox = QtGui.QHBoxLayout()
        self.adjustButton = QtGui.QToolButton()

        self.Init()   


    def Init(self):        
        self.adjustButton.setFixedSize(10, 10)


        self.hbox.setContentsMargins(5, 2, 5, 2)
        self.hbox.setSpacing(0)
        self.hbox.addWidget(self.adjustButton,0,QtCore.Qt.AlignRight)
        self.setLayout(self.hbox)

class TextEdit(QtGui.QTextEdit):
    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)
        self.setFrameShape(self.Box)
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.parent = parent
      
        self.height = 0    
        self.connect(self.document(),QtCore.SIGNAL('blockCountChanged(int)'), self.setPasteText)

        #fmt = QtGui.QTextBlockFormat()
        #fmt.setLineHeight(10, QtGui.QTextBlockFormat.FixedHeight)
        #cur.setBlockFormat(fmt)
        #self.setTextCursor(cur)

        #stylesheet

        #another way to set backgroundcolor
        #p2 = QtGui.QPalette()
        #p2.setColor(QtGui.QPalette.Base, QtGui.QColor(192,253,123))
        #p2.setColor(QtGui.QPalette.Text, QtGui.QColor(QtCore.Qt.red))
        #p2.setColor(QtGui.QPalette.Active, QtGui.QPalette.Highlight, QtGui.QColor(QtCore.Qt.white))

        #self.textEdit.setPalette(p2)

        #self.textEdit.connect(self.textEdit, QtCore.SIGNAL('customContextMenuRequested()'), self.customContextMenuEvent)
    def setPasteText(self, num):
        #self.setLineHeight(self.height)
        '''cur = self.textCursor()
        i = 0
        logger.debug(num)
        while i != num:
            cur.movePosition(QtGui.QTextCursor.NextBlock) 
            tmpbl = cur.block()
            logger.debug(tmpbl.text()) 
            textFmt = tmpbl.blockFormat()
            #textFmt.setBottomMargin(5)
            textFmt.setLineHeight(self.height, QtGui.QTextBlockFormat.FixedHeight)
            cur.setBlockFormat(textFmt)
            self.setTextCursor(cur)
            i = i + 1
        '''    #注意 一定要移动textcursor到下一个block 否则只会修改第一个block的format
        pass

    def setLineHeight(self, height):
        #return
        self.height = height
        doc = self.document()

        doc = self.document()
        cur = self.textCursor()
        logger.debug('blockCount: ' + str(doc.blockCount()))
        #修改每一个block的格式
        for i in range(doc.blockCount()):
            it = doc.findBlockByNumber(i)
            logger.debug('blockNum: ' + str(i) + ' content: ' + it.text())
            textFmt = it.blockFormat()
            #textFmt.setBottomMargin(5)
            textFmt.setLineHeight(self.height, QtGui.QTextBlockFormat.FixedHeight)
            cur.setBlockFormat(textFmt)
            self.setTextCursor(cur)
            #注意 一定要移动textcursor到下一个block 否则只会修改第一个block的format
            cur.movePosition(QtGui.QTextCursor.NextBlock)        
        cur.movePosition(QtGui.QTextCursor.Start)
        self.setTextCursor(cur)

    def contextMenuEvent(self, event):
        logger.debug('contextMenuEvent')
        menu = QtGui.QMenu()
         
        #cutAct = menu.addAction('cut', self, QtCore.SLOT('cut()'), QtGui.QKeySequence.Cut)
        cutAct = menu.addAction('cut', self, QtCore.SLOT('cut()'))
        cutAct.setEnabled(self.textCursor().hasSelection())
 
        copyAct = menu.addAction('copy', self, QtCore.SLOT('copy()'))
        copyAct.setEnabled(self.textCursor().hasSelection())

        menu.addAction('paste', self, QtCore.SLOT('paste()'))

       # delAct = menu.addAction('del', self, QtCore.SLOT('del()'))
       # delAct.setEnabled(self.textCursor().hasSelection())

        menu.addSeparator()

        selectAct = menu.addAction('selectAll', self, QtCore.SLOT('selectAll()'))

        menu.addSeparator()

        greenAct = QtGui.QAction('green', self)             
        menu.addAction(greenAct)
        self.connect(greenAct, QtCore.SIGNAL('triggered()'), self.setColor)
  
        whiteAct = QtGui.QAction('white', self)             
        menu.addAction(whiteAct)
        self.connect(whiteAct, QtCore.SIGNAL('triggered()'), self.setWhite)

        pinkAct = QtGui.QAction('pink', self)             
        menu.addAction(pinkAct)
        self.connect(pinkAct, QtCore.SIGNAL('triggered()'), self.setPink)

        blueAct = QtGui.QAction('blue', self)             
        menu.addAction(blueAct)
        self.connect(blueAct, QtCore.SIGNAL('triggered()'), self.setBlue)

        purpleAct = QtGui.QAction('purple', self)             
        menu.addAction(purpleAct)
        self.connect(purpleAct, QtCore.SIGNAL('triggered()'), self.setPurple)

        yellowAct = QtGui.QAction('yellow', self)             
        menu.addAction(yellowAct)
        self.connect(yellowAct, QtCore.SIGNAL('triggered()'), self.setYellow)

        menu.exec_(event.globalPos())

    def setGreen(self):
        logger.debug('setGreen')
        self.parent.setWindowColorStyle('green')

    def setWhite(self):
        logger.debug('setWhite')
        self.parent.setWindowColorStyle('white')
    def setPink(self):
        logger.debug('setPink')
        self.parent.setWindowColorStyle('pink')  

    def setBlue(self):
        logger.debug('setBlue')
        self.parent.setWindowColorStyle('blue') 

    def setPurple(self):
        logger.debug('setPurple')
        self.parent.setWindowColorStyle('purple') 
    def setYellow(self):
        logger.debug('setYellow')
        self.parent.setWindowColorStyle('yellow') 

class NoteWindow(QtGui.QFrame):
    def __init__(self, wm = None, x = 100, y = 200, parent=None):
        super(NoteWindow, self).__init__(parent)
        

        self.setObjectName("NoteWindow")         

        self.windowManager = wm
        self.color = 'green'


        self.mouseDown = False
        self.setFrameShape(self.Panel)
        self.setGeometry(950, 55, 350, 250)
        self.resize(300, 300)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)

        self.setMouseTracking(True)       

     
        #shadow
        #shadow_eff = QtGui.QGraphicsDropShadowEffect()
        #shadow_eff.setBlurRadius(5.0)
        #shadow_eff.setColor(QtGui.QColor(0,0,0,100))
        #shadow_eff.setOffset(1.0)
        #self.setGraphicsEffect(shadow_eff)        

        #set the backgroundColor
        #pl = QtGui.QPalette()
        #pl.setColor(QtGui.QPalette.Background, QtGui.QColor(19,253,123))
        
        #self.setPalette(pl)
        
        self.textEdit = TextEdit(self)

        self.titlebar = TitleBar(self)
        
        self.bottombar = BottomBar(self)
 
        #titlebar
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.titlebar)
        self.vbox.setMargin(0)
        self.vbox.setSpacing(0)
       
        self.layout = QtGui.QVBoxLayout()

        #textedit
        self.layout.addWidget(self.textEdit)
        #self.hbox.setContentsMargins(5, 3, 5, 5)
        self.layout.setContentsMargins(5, 0, 5, 0)
        #self.layout.setMargin(5)
        self.layout.setSpacing(0)
        self.vbox.addLayout(self.layout)

        #bottombar

        self.bottomlayout = QtGui.QVBoxLayout()
        self.bottomlayout.addWidget(self.bottombar)
        self.bottomlayout.setMargin(0)
        self.bottomlayout.setSpacing(0)        
        self.vbox.addLayout(self.bottomlayout)

        self.setLayout(self.vbox)
        self.setWindowTitle("Window Title")
        self.move(x, y)

        self.textEdit.setFocus()
        self.textEdit.setLineHeight(25)

        # green style: bottom 177,232,174 top 209,254,203
        # self.setStyleSheet('''
        #                    QTextEdit{padding:0px 10px 0px 10px ;background-color:rgb(0,0,0,0);border:0px solid;font-size:11pt;}
        #                    QFrame#NoteWindow{background:qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:1 rgb(177,232,174), stop:0 rgb(209,254,203));border:0px solid;}''')
        #self.setWindowColorStyle('purple')

        self.show()      

    def setText(self, text):
        self.textEdit.setText(text)
        self.textEdit.setLineHeight(26)

    #signal slot 
    def mousePressEvent(self, event):
        self.oldPos = event.pos()
        self.mouseDown = event.button() == QtCore.Qt.LeftButton
        self.rectWidth = self.geometry().width()

    def mouseMoveEvent(self, event):
        self.x = event.x()
        self.y = event.y()
        if self.mouseDown == True:
            dx = self.x - self.oldPos.x()
            dy = self.y - self.oldPos.y()
            g = self.geometry()
            if self.left == True:
                g.setLeft(g.left() + dx)
            if self.right == True:
                g.setRight(g.right() + dx)
            if self.bottom == True:
                g.setBottom(g.bottom() + dy)
            
            self.setGeometry(g)

            tmpx = event.x()
            if not self.left:
                tmpx = event.x()
            else:
                tmpx = self.oldPos.x()
            self.oldPos = QtCore.QPoint(tmpx, event.y())
            self.rectWidth = g.width()
        else:
            r = self.rect()
            self.left = QtCore.qAbs(self.x - r.left()) <= 5
            self.right = QtCore.qAbs(self.x - r.right()) <= 5
            self.bottom = QtCore.qAbs(self.y - r.bottom()) <= 5
            hor = self.left | self.right
            
            if hor and self.bottom == True:
                if self.left == True:
                    self.setCursor(QtCore.Qt.SizeBDiagCursor)
                else:
                    self.setCursor(QtCore.Qt.SizeFDiagCursor)
            elif hor == True:
                self.setCursor(QtCore.Qt.SizeHorCursor)
            elif self.bottom == True:
                self.setCursor(QtCore.Qt.SizeVerCursor)
            else:
                self.setCursor(QtCore.Qt.ArrowCursor)

    def mouseReleaseEvent(self, event):
        self.mouseDown = False

    #def closeEvent(self, event):
    #    self.emit(QtCore.SIGNAL('closeNotifyToWindowManager(QWidget)'),self)
    #    event.accept()       

    def setWindowColorStyle(self, style):
        # green style: bottom 177,232,174 top 209,254,203 title 197,247,193

        bottom = ''
        top = ''
        rgb = ()

        if style == 'green':
            bottom = '177,232,174'
            top = '209,254,203'
            rgb = (197, 247, 193)
        # green style: bottom 235,235,235 top 254,254,254 title 245,245,245
        elif style == 'white':
            bottom = '235,235,235'
            top = '254,254,254'
            rgb = (245,245,245)       
        elif style == 'blue':
            bottom = '184,219,244'
            top = '217,243,251'
            rgb = (201,236,248)
        elif style == 'pink':
            bottom = '235,174,235'
            top = '246,211,246'
            rgb = (241,195,241)
        elif style == 'purple':
            bottom = '198,184,254'
            top = '221,217,254'
            rgb = (212,205,243)
        elif style == 'yellow':
            bottom = '252,249,161'
            top = '254,254,204'
            rgb = (248,247,182)

        self.setStyleSheet('QTextEdit{background-color:rgb(0,0,0,0);border:0px solid;font:12pt;}QFrame#NoteWindow{background:qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:1 rgb(' + bottom + '), stop:0 rgb(' + top + '));border:0px solid;}QTextDocument{line-height:25px}')
        
        pl = QtGui.QPalette()  
        pl.setColor(QtGui.QPalette.Background, QtGui.QColor(*rgb))
        self.titlebar.setPalette(pl)                                    
        self.color = style 


class WindowManager:
    def __init__(self,appinst):

        self.noteIni = {}       
        self.windowInstances = {'windowMaxNum':10, 'windowInstance':{}}
        self.indexFile = 0
        self.instApp = appinst

        #创建一个stub主窗口 作用 使任务栏只有一个窗口出现
        #主窗口 为无边框窗口 大小1,1 移动到左上角 
        #点击任务栏进程 所有子窗口均返回top-level
        #关闭任务栏进程 所有子窗口均关闭
        self.mainWindow = QtGui.QMainWindow()  
        self.mainWindow.resize(1,1)
        self.mainWindow.move(-100,-100)
        self.mainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.mainWindow.show()

        #read note.ini for note position
        self.loadIniFile()

        #txtlist = self.getAllTxtFile("./")   
        #create window
        if not self.createWindowFromFileList():
            self.instApp.exit()
    
        #print self.windowInstances 

    def saveAll(self):
        logger.debug('saveAllNotes')
        #update the datafile

        logger.debug( self.windowInstances['windowInstance'])

        inilines = []

        for inst, name in self.windowInstances['windowInstance'].items():
            line = inst.color + ' ' + str(inst.pos().x()) + ' '+str(inst.pos().y()) + ' ' + name + '\n'
            inilines.append(line)
            qfile = QtCore.QFile(name)
            if qfile.open(QtCore.QFile.WriteOnly):
                stream = QtCore.QTextStream(qfile)
                stream << inst.textEdit.toPlainText()
                qfile.close()

        #write ini files
        ini = open('note.ini', 'w')  
        ini.writelines(inilines) 
        ini.close()    

    def loadIniFile(self):
        #读取配置文件的每一行
        inf = open('note.ini','r')
        lines_inf = inf.readlines()

        for line in lines_inf:
            tmplist = line.split()
            tmpdict = {}
            tmpdict['color'] = tmplist[0]
            tmpdict['x'] = int(tmplist[1])
            tmpdict['y'] = int(tmplist[2])

            self.noteIni[tmplist[3]] = tmpdict
 
    def createWindowFromFileList(self):
        i = 0 

        if any(self.noteIni) == False:
            window = self.createWindow()
            
        else:
            logger.debug( self.noteIni.keys() )
            for l in self.noteIni.keys():
                qfile = QtCore.QFile(l) 
                if qfile.open(QtCore.QFile.ReadOnly):
                    stream = QtCore.QTextStream(qfile)
                    text = stream.readAll()
        
                    window = self.createWindow(self.noteIni[unicode(l)]['x'], self.noteIni[unicode(l)]['y'], self.noteIni[unicode(l)]['color'], unicode(l))
                    window.setText(text)              

                    qfile.close()
                    i = i + 1
                else: 
                    logger.error( 'file not found')
                    return False

        return True        

    #获取所有的txt文件
    def getAllTxtFile(self, path):
        qdir = QtCore.QDir(path)
        filters = QtCore.QStringList()
        filters << "*.note"
        
        filename = qdir.entryList(filters, QtCore.QDir.Files)

        return filename


    #signal
    def closeWindow(self, inst):
        #delete save info    
        logger.debug( 'closeWindow')
        if self.windowInstances['windowInstance'].has_key(inst):
            self.indexFile = self.indexFile - 1
            cmd = 'rm ' + self.windowInstances['windowInstance'][inst]
            
            self.windowInstances['windowInstance'].pop(inst)
            os.system(cmd)
            inst.close()
        if self.indexFile == 0:
            logger.debug( 'should exit program')
            self.instApp.exit()

    def createWindow(self, x = 100, y = 200, style = 'purple', filen = None):
        window = None

        if filen == None:
            filen = datetime.now().strftime('%Y%m%d%H%M%S%f') +".note"

        if self.indexFile == self.windowInstances['windowMaxNum'] - 1:
            logger.debug( 'Max Window Num')
        else:
            #创建 便笺子窗口 父窗口为mainWIndow窗口
            window = NoteWindow(self, x, y, self.mainWindow)
            window.setWindowColorStyle(style)

            #window.setParent(self.mainWindow)

            self.indexFile = (self.indexFile + 1 ) % self.windowInstances['windowMaxNum']
            self.windowInstances['windowInstance'][window] = filen
     

        return window

if __name__ == '__main__':
    #init logging
    LOG_FILE = 'note.log'

    handler = logging.handlers.RotatingFileHandler(LOG_FILE)
    shandler = logging.StreamHandler()

    handler.setLevel(logging.DEBUG)
    shandler.setLevel(logging.DEBUG)

    fmt = '[%(asctime)s - %(filename)s:%(lineno)s] [%(levelname)s] %(funcName)s(): %(message)s'
    formatter = logging.Formatter(fmt)

    handler.setFormatter(formatter)
    shandler.setFormatter(formatter)
    
    logger = logging.getLogger('note')
    logger.addHandler(handler)
    logger.addHandler(shandler)
    logger.setLevel(logging.DEBUG)

    logger.info('program start')

    app = QtGui.QApplication(sys.argv)
    wm = WindowManager(app)
    ret = app.exec_()
    wm.saveAll()
    logger.info('program end')
    sys.exit(ret)

