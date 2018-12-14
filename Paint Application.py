import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QGridLayout,
                             QGroupBox, QFileDialog, QRadioButton, QWidget, QStyleOptionButton,
                             QSlider, QAction, QToolBar, QColorDialog)
from PyQt5.QtGui import (QPen, QIcon, QImage, QPainter, QPixmap)
import os
from PyQt5.QtCore import (QPoint, Qt, QSize)

class Assignment_2(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):

        '''
            Initialize all the variable to operate for the paint program
        '''
        # menus
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu(" File")  # the space is required as "File" is reserved in Mac
        brushSizeMenu = mainMenu.addMenu(" Brush Size")
        brushColorMenu = mainMenu.addMenu(" Brush Colour")
        capOption = mainMenu.addMenu(" Cap")
        joinOption = mainMenu.addMenu(" Join")
        penOption = mainMenu.addMenu(" Pen")
        pathComposed = mainMenu.addMenu(" Path")

        # Cap Style
        flatCap = QAction("Flat", self)
        capOption.addAction(flatCap)
        flatCap.triggered.connect(self.flatCap)

        squareCap = QAction("Square", self)
        capOption.addAction(squareCap)
        squareCap.triggered.connect(self.squareCap)

        roundCap = QAction("Round", self)
        capOption.addAction(roundCap)
        roundCap.triggered.connect(self.roundCap)

        # Join Style
        bevelJoin = QAction("Bevel", self)
        joinOption.addAction(bevelJoin)
        bevelJoin.triggered.connect(self.bevelJoin)

        miterJoin = QAction("Miter", self)
        joinOption.addAction(miterJoin)
        miterJoin.triggered.connect(self.miterJoin)

        roundJoin = QAction("Round", self)
        joinOption.addAction(roundJoin)
        roundJoin.triggered.connect(self.roundJoin)


        #Pen Style
        solidLine = QAction(QIcon("./icons/qpen-solid"),"Solid Line", self)
        penOption.addAction(solidLine)
        solidLine.triggered.connect(self.solidLine)

        dashLine = QAction(QIcon("./icons/qpen-dash"),"Dash Line", self)
        penOption.addAction(dashLine)
        dashLine.triggered.connect(self.dashLine)

        dotLine = QAction(QIcon("./icons/qpen-dot"),"Dot Line", self)
        penOption.addAction(dotLine)
        dotLine.triggered.connect(self.dotLine)

        dashDotLine = QAction(QIcon("./icons/qpen-dashdot"),"Dash Dot Line", self)
        penOption.addAction(dashDotLine)
        dashDotLine.triggered.connect(self.dashDotLine)

        dashDotDotLine = QAction(QIcon("./icons/qpen-dashdotdot"),"Dash Dot Dot Line", self)
        penOption.addAction(dashDotDotLine)
        dashDotDotLine.triggered.connect(self.dashDotDotLine)

        # save
        saveAction = QAction(QIcon("./icons/save.png"), "Save", self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)  # when the menu option is selected or the shortcut is used the save menu is triggered

        # clear
        clearAction = QAction(QIcon("./icons/clear.png"), "Clear", self)
        clearAction.setShortcut("Ctrl+C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        # brush thickness - brush thickness icons have not been downloaded
        threepxAction = QAction(QIcon("./icons/threepx.png"), "3px", self)
        threepxAction.setShortcut("Ctrl+3")  # TODO changed the control options to be numbers
        brushSizeMenu.addAction(threepxAction)
        threepxAction.triggered.connect(self.threepx)

        fivepxAction = QAction(QIcon("./icons/fivepx.png"), "5px", self)
        fivepxAction.setShortcut("Ctrl+5")
        brushSizeMenu.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivepx)

        sevenpxAction = QAction(QIcon("./icons/sevenpx.png"), "7px", self)
        sevenpxAction.setShortcut("Ctrl+7")
        brushSizeMenu.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenpx)

        ninepxAction = QAction(QIcon("./icons/ninepx.png"), "9px", self)
        ninepxAction.setShortcut("Ctrl+9")
        brushSizeMenu.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninepx)

        # brush colors
        blackAction = QAction(QIcon("./icons/black.png"), "Black", self)
        blackAction.setShortcut("Ctrl+B")
        brushColorMenu.addAction(blackAction);
        blackAction.triggered.connect(self.black)

        redAction = QAction(QIcon("./icons/red.png"), "Red", self)
        redAction.setShortcut("Ctrl+R")
        brushColorMenu.addAction(redAction);
        redAction.triggered.connect(self.red)

        greenAction = QAction(QIcon("./icons/green.png"), "Green", self)
        greenAction.setShortcut("Ctrl+G")
        brushColorMenu.addAction(greenAction);
        greenAction.triggered.connect(self.green)

        yellowAction = QAction(QIcon("./icons/yellow.png"), "Yellow", self)
        yellowAction.setShortcut("Ctrl+Y")
        brushColorMenu.addAction(yellowAction);
        yellowAction.triggered.connect(self.yellow)


        #----------------------------------------------------

        # window dimensions
        top = 400
        left = 400
        width = 800
        height = 600

        self.setWindowTitle("Paint Application");
        self.setGeometry(top, left, width, height)
        # windows version
        self.setWindowIcon(QIcon("./icons/paint-brush.png"))
        # mac version - not yet working
        # self.setWindowIcon(QIcon(QPixmap("./icons/paint-brush.png")))

        # image settings (default)
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        # draw settings (default)
        self.drawing = False
        self.brushSize = 3
        self.brushColor = Qt.black
        self.penStyle = Qt.DashDotDotLine
        self.capStyle = Qt.RoundCap
        self.joinStyle = Qt.RoundJoin

        # reference to last point recorded by mouse
        self.lastPoint = QPoint()


        # ----------------------------------------------------


        '''
            Scroll the slider to increase the brush size.
            Default: 3px 
            Minimum: 2px
            Maximum: 35px
        '''
        self.penWidth = QSlider(Qt.Horizontal)
        self.penWidth.setMinimum(2)
        self.penWidth.setMaximum(35)
        self.penWidth.setTickInterval(2)
        self.penWidth.setValue(3)
        self.penWidth.setTickPosition(QSlider.TicksBelow)
        self.penWidth.setFixedWidth(120)

        self.penWidth.valueChanged.connect(self.slider_change)

        centralWidget = QWidget()
        #centralWidget.setLayout(layout)

        toolBar = self.addToolBar("My Toolbar")
        toolBar.setAllowedAreas(Qt.LeftToolBarArea)
        #toolBar.setOrientation(Qt.Vertical)
        toolBar.allowedAreas()

        toolBar.addWidget(self.penWidth)
        toolBar.addSeparator()


        self.setCentralWidget(centralWidget)


        self.setWindowTitle("Paint Application")
        self.show()




    #----------------------------------------------------
    # event handlers
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True  # we are now entering draw mode
            self.lastPoint = event.pos()  # new point is saved as last point
            print(self.lastPoint)

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)  # object which allows drawing to take place on an image
            # allows the selection of brush colour, brish size, line type, cap type, join type. Images available here http://doc.qt.io/qt-5/qpen.html
            painter.setPen(QPen(self.brushColor, self.brushSize, self.penStyle, self.capStyle, self.joinStyle))

            print(self.brushColor)
            print(self.brushSize)
            print(self.penStyle)
            print(self.capStyle)
            print(self.joinStyle)


            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    # ----------------------------------------------------

    '''
        Functions to call when someone calls the menubar items.
    '''
    # slots
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "","PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":
            return
        self.image.save(filePath)

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def threepx(self):
        self.brushSize = 3

    def fivepx(self):
        self.brushSize = 5

    def sevenpx(self):
        self.brushSize = 7

    def ninepx(self):
        self.brushSize = 9

    def black(self):
        self.brushColor = Qt.black

    def red(self):
        self.brushColor = Qt.red

    def green(self):
        self.brushColor = Qt.green

    def yellow(self):
        self.brushColor = Qt.yellow

    def slider_change(self):
        print(str(self.penWidth.value()))
        self.brushSize = int(str(self.penWidth.value()))

    def flatCap(self):
        self.capStyle = Qt.FlatCap
    def squareCap(self):
        self.capStyle = Qt.SquareCap
    def roundCap(self):
        self.capStyle = Qt.RoundCap

    def bevelJoin(self):
        self.joinStyle = Qt.BevelJoin
    def miterJoin(self):
        self.joinStyle = Qt.MiterJoin
    def roundJoin(self):
        self.joinStyle = Qt.RoundJoin

    def solidLine(self):
        self.penStyle = Qt.SolidLine
    def dashLine(self):
        self.penStyle = Qt.DashLine

    def dotLine(self):
        self.penStyle = Qt.DotLine
    def dashDotLine(self):
        self.penStyle = Qt.DashDotLine
    def dashDotDotLine(self):
        self.penStyle = Qt.DashDotDotLine


app = QApplication(sys.argv)
assignment = Assignment_2()

sys.exit(app.exec_())