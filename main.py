## @package Labelling_app
# Labelling app software developed with Grabcut
# 
#  @version 1 
#
# Pontificia Universidad Javeriana
# 
# Electronic Enginnering
# 
# Developed by:
# - Andrea Juliana Ruiz Gomez
#       Mail: <andrea_ruiz@javeriana.edu.co>
#       GitHub: andrearuizg
# - Pedro Eli Ruiz Zarate
#       Mail: <pedro.ruiz@javeriana.edu.co>
#       GitHub: PedroRuizCode
#  
# With support of:
# - Francisco Carlos Calderon Bocanegra
#       Mail: <calderonf@javeriana.edu.co>
#       GitHub: calderonf
# - John Alberto Betancout Gonzalez
#       Mail: <john@kiwibot.com>
#       GitHub: JohnBetaCode

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import numpy as np
from time import time
import random


## GUI class
class GUI(QMainWindow):

    ## The constructor
    #
    # Here you can configure the screen, buttons (rectangle, foreground,
    # iteration, open file, new label, original image, segmented image,
    # labelled image, previous, next, save, exit, reset), labels (video frame,
    # label, show image), spin box (video frames), list (labels), image panel,
    # checkbox (full screen, dark theme) and mouse events
    # @param self The object pointer.
    def __init__(self):
        super().__init__()
        app.setStyle('Fusion')

        screen = app.primaryScreen()
        rect = screen.size()
        width = rect.width()
        height = rect.height() - 30

        self.setGeometry(10, 10, width, height)
        self.setWindowTitle("Kiwi & PUJ - Labelling software")
        self.setWindowIcon(QIcon("media/.icons/ICON.png"))

        self.b_rec = QPushButton(self)
        self.b_rec.setText('&Rectangle')
        self.b_rec.move(((width // 2) - 210), 15)
        self.b_rec.setEnabled(False)
        self.b_rec.setShortcut('Ctrl+r')
        self.b_rec.clicked.connect(self.rectangle_)

        self.b_bg = QPushButton(self)
        self.b_bg.setText('&Background')
        self.b_bg.move(((width // 2) - 105), 15)
        self.b_bg.setEnabled(False)
        self.b_bg.setShortcut('Ctrl+b')
        self.b_bg.clicked.connect(self.background_)

        self.b_fg = QPushButton(self)
        self.b_fg.setText('&Foreground')
        self.b_fg.move(width // 2, 15)
        self.b_fg.setEnabled(False)
        self.b_fg.setShortcut('Ctrl+f')
        self.b_fg.clicked.connect(self.foreground_)

        self.b_it = QPushButton(self)
        self.b_it.setText('&Iteration')
        self.b_it.move(((width // 2) + 105), 15)
        self.b_it.setEnabled(False)
        self.b_it.setShortcut('Ctrl+i')
        self.b_it.clicked.connect(self.iteration_)

        f_open = QPushButton(self)
        f_open.setText('&Open file')
        f_open.setIcon(QIcon('media/.icons/file.png'))
        f_open.move(10, 15)
        f_open.setShortcut('Ctrl+o')
        f_open.clicked.connect(self.open_)

        t1 = QLabel(self)
        t1.setText("Video frames")
        t1.move(10, height - 175)

        self.spin = QSpinBox(self)
        self.spin.move(10, height - 150)
        self.spin.setValue(30)
        self.spin.setRange(1, 999)
        self.spin.valueChanged.connect(self.sh_spin_val)

        t1 = QLabel(self)
        t1.setText("Labels")
        t1.move(10, 90)

        self.b_new = QPushButton(self)
        self.b_new.setText('&New')
        self.b_new.setIcon(QIcon('media/.icons/new.png'))
        self.b_new.setEnabled(False)
        self.b_new.setShortcut('Ctrl+n')
        self.b_new.move(10, 120)
        self.b_new.clicked.connect(self.new_label)

        labels = open('/tmp/labels.txt', 'r').read()
        self.labels = list(labels.split("\n"))

        self.Label_n = QComboBox(self)
        for n in range(len(self.labels) - 1):
            self.Label_n.addItem(self.labels[n])
        self.Label_n.move(10, 150)
        self.Label_n.setEnabled(False)
        self.Label_n.activated[str].connect(self.sel_LN)

        t2 = QLabel(self)
        t2.setText("Show image")
        t2.move(10, height // 2)

        self.b_or = QPushButton(self)
        self.b_or.setText('Original')
        self.b_or.move(10, (height // 2) + 30)
        self.b_or.setEnabled(False)
        self.b_or.clicked.connect(self.b_or_)

        self.b_seg = QPushButton(self)
        self.b_seg.setText('Segmented')
        self.b_seg.move(10, (height // 2) + 60)
        self.b_seg.setEnabled(False)
        self.b_seg.clicked.connect(self.b_seg_)

        self.b_lab = QPushButton(self)
        self.b_lab.setText('Labels')
        self.b_lab.move(10, (height // 2) + 90)
        self.b_lab.setEnabled(False)
        self.b_lab.clicked.connect(self.b_lab_)

        self.b_pre = QPushButton(self)
        self.b_pre.setText('Previous')
        self.b_pre.setIcon(QIcon('media/.icons/undo.png'))
        self.b_pre.move(10, height - 110)
        self.b_pre.setShortcut('Ctrl+Left')
        self.b_pre.setEnabled(False)
        self.b_pre.clicked.connect(self.b_pre_)

        self.b_nxt = QPushButton(self)
        self.b_nxt.setText('Next')
        self.b_nxt.setIcon(QIcon('media/.icons/redo.png'))
        self.b_nxt.move(10, height - 80)
        self.b_nxt.setShortcut('Ctrl+Right')
        self.b_nxt.setEnabled(False)
        self.b_nxt.clicked.connect(self.b_nxt_)

        self.b_sav = QPushButton(self)
        self.b_sav.setText('&SAVE')
        self.b_sav.setIcon(QIcon('media/.icons/save.png'))
        self.b_sav.move(10, height - 30)
        self.b_sav.setEnabled(False)
        self.b_sav.setShortcut('Ctrl+s')
        self.b_sav.clicked.connect(self.b_sav_)

        b_ext = QPushButton(self)
        b_ext.setText('EXIT')
        b_ext.setIcon(QIcon('media/.icons/exit.png'))
        b_ext.move(width - 110, height - 30)
        b_ext.clicked.connect(self.b_ext_)

        b_res = QPushButton(self)
        b_res.setText('RESET')
        b_res.move(width - 110, height - 80)
        b_res.clicked.connect(self.reset_)

        self.image_1 = QLabel(self)
        self.image_1.resize(640, 480)
        self.image_1.move((width // 2) - 320, (height // 2) - 200)

        self.dark = QCheckBox(self)
        self.dark.setText('Dark theme')
        self.dark.setChecked(True)
        self.dark.move((width - 110), 15)
        self.dark.toggled.connect(self.dark_)

        self.fs = QCheckBox(self)
        self.fs.setText('Full Screen')
        self.fs.setChecked(True)
        self.fs.move((width - 110), 35)
        self.fs.toggled.connect(self.fullScreen_)

        self.fullScreen_()
        self.show()
        self.reset_()
        self.dark_()

        self.image_1.mousePressEvent = self.mouse_down
        self.image_1.mouseMoveEvent = self.mouse_move
        self.image_1.mouseReleaseEvent = self.mouse_up

    ## Label selection function
    #
    # Select the label of the segmented image, and created the labelled image
    # file
    # @param self The object pointer.
    # @param text Label gave by the user
    def sel_LN(self, text):
        for n in range(len(self.labels) - 1):
            if text == self.labels[n]:
                self.contour_()
                self.colors = tuple(self.colors)
                cv2.drawContours(self.img_out, self.contours, -1, n + 1,
                                 thickness=cv2.FILLED)
                cv2.drawContours(self.img_label, self.contours, -1,
                                 self.colors[n], thickness=cv2.FILLED)

    ## Contour function
    #
    # Determine the contour of the segmented image
    # @param self The object pointer.
    def contour_(self):
        imgray = cv2.cvtColor(self.out, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 1, 255, 0)
        self.contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,
                                                    cv2.CHAIN_APPROX_SIMPLE)

    ## New label button function
    #
    # Set enable flag true
    # @param self The object pointer.
    def new_label(self):
        self.Label_n.setEnabled(True)
        self.b_lab_()

    ## Original picture button
    #
    # Show original picture
    # @param self The object pointer.
    def b_or_(self):
        self.showImage_(self.img_in)

    ## Segmented picture button
    #
    # Show segmented picture
    # @param self The object pointer.
    def b_seg_(self):
        self.showImage_(self.out)

    ## Labelled picture button
    #
    # Show labelled picture
    # @param self The object pointer.
    def b_lab_(self):
        self.showImage_(self.img_label)

    ## Spin value function
    #
    # Update video frame variable
    # @param self The object pointer.
    def sh_spin_val(self):
        self.value_sp = self.spin.value()

    ## Previous image button function
    #
    # Disable buttons and show warnings
    # @param self The object pointer.
    def b_pre_(self):
        if self.flag_save == 0:
            self.b_sav.setEnabled(False)
            self.b_bg.setEnabled(False)
            self.b_fg.setEnabled(False)
            self.b_it.setEnabled(False)
            self.b_new.setEnabled(False)
            self.Label_n.setEnabled(False)
            self.b_or.setEnabled(False)
            self.b_seg.setEnabled(False)
            self.b_lab.setEnabled(False)
            if self.flag_save == 1:
                self.show_alert()
            if self.file_vid == 0:
                self.file_num -= 1
                self.load()
            else:
                if self.flag_vid == 1:
                    self.flag_vid = 0
                    self.file_num -= 2
                self.frame_act -= int(self.value_sp)
                self.load_vid()
        else:
            self.flag_save = 0
            self.show_alert()

    ## Next image button function
    #
    # Disable buttons and show warnings
    # @param self The object pointer.
    def b_nxt_(self):
        if self.flag_save == 0:
            self.b_sav.setEnabled(False)
            self.b_bg.setEnabled(False)
            self.b_fg.setEnabled(False)
            self.b_it.setEnabled(False)
            self.b_new.setEnabled(False)
            self.Label_n.setEnabled(False)
            self.b_or.setEnabled(False)
            self.b_seg.setEnabled(False)
            self.b_lab.setEnabled(False)
            if self.file_vid == 0:
                self.file_num += 1
                self.load()
            else:
                self.frame_act += int(self.value_sp)
                self.load_vid()
        else:
            self.flag_save = 0
            self.show_alert()

    ## Save button function
    #
    # Save files
    # - for pictures only save the labelled mask
    # - for videos save labelled mask and original frame
    # @param self The object pointer.
    def b_sav_(self):
        str = (self.filename[self.file_num].split(".")[0]).split("/")[-1]
        if self.file_vid == 0:
            outfile = 'media/%s-mask.png' % (str)
            outfile1 = 'media/%s.png' % (str)
        else:
            outfile = 'media/%s-frame-%s-mask.png' % (str, self.frame_act)
            outfile1 = 'media/%s-frame-%s.png' % (str, self.frame_act)
        original = '%s' % self.filename[self.file_num].split("/")[-1]
        mask = '%s' % outfile.split("/")[-1]
        tf = '%s' % (time() - self.ti)
        self.d_time[self.frame_num, ...] = [original, mask, tf]
        cv2.imwrite(outfile, self.img_out)
        cv2.imwrite(outfile1, self.img_in)
        self.frame_num += 1
        self.flag_save = 0
        self.flag_file = 1

    ## Exit button function
    #
    # Save time stamps csv and close app
    # @param self The object pointer.
    def b_ext_(self):
        if self.flag_file == 1:
            np.savetxt("media/timestamps.csv", self.d_time, delimiter=", ", 
                       fmt='%s')
        self.close()
        QApplication.quit()

    ## Open button function
    #
    # Open file dialog window
    # @param self The object pointer.
    def open_(self):
        self.filename, _ = QFileDialog.getOpenFileNames(None, 'Buscar Imagen',
                        '.', 'Image Files (*.png *.jpg *.jpeg *.bmp *.mp4)')
        self.file_num = 0
        self.frame_num = 1
        self.flag_save = 0
        self.flag_vid = 0
        self.file_vid = 0
        self.b_rec.setEnabled(True)
        self.b_pre.setEnabled(True)
        self.b_nxt.setEnabled(True)
        self.load()

    ## Load function
    #
    # Open file in open cv
    # @param self The object pointer.
    def load(self):
        self.flag_save = 0
        if self.file_num < len(self.filename):
            if (self.filename[self.file_num].split(".")[-1] in 
                ['png', 'jpg', 'jpeg', 'bmp']):
                self.img_in = cv2.imread(self.filename[self.file_num], 
                                         cv2.IMREAD_UNCHANGED)
                self.img_in = cv2.resize(self.img_in, (640, 480))
                self.img_copy = self.img_in.copy()
                self.img_out = np.zeros((480, 640), np.uint8)
                self.img_label = self.img_in.copy()
                self.showImage_(self.img_in)
            else:
                self.file_vid = 1
                self.vid = cv2.VideoCapture(self.filename[self.file_num])
                self.length = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
                self.frame_act = 1
                self.load_vid()
        else:
            self.b_ext_()
        if ((self.file_num == 0) and (self.file_vid == 0)):
            self.b_pre.setEnabled(False)
        else:
            self.b_pre.setEnabled(True)
        if ((self.file_num == (len(self.filename) - 1)) 
            and (self.file_vid == 0)):
            self.b_nxt.setEnabled(False)
        else:
            self.b_nxt.setEnabled(True)

    ## Load video function
    #
    # Open video frames
    # @param self The object pointer.
    def load_vid(self):
        self.sh_spin_val()
        if self.vid.isOpened():
            if (self.frame_act <= self.length) and (self.frame_act > 0):
                self.vid.set(1, self.frame_act)
                ret, self.img_in = self.vid.read()
                self.img_in = cv2.resize(self.img_in, (640, 480))
                self.img_copy = self.img_in.copy()
                self.img_out = np.zeros((480, 640), np.uint8)
                self.img_label = self.img_in.copy()
                self.showImage_(self.img_in)
            else:
                self.flag_vid = 1
                self.vid.release()
                self.file_vid = 0
                self.file_num += 1
                self.load()

    ## Show image function
    #
    # Show picture in Pixmap
    # @param self The object pointer.
    #  @param image Image to display.
    def showImage_(self, image):
        size = image.shape
        step = image.size / size[0]
        qformat = QImage.Format_Indexed8
        if len(size) == 3:
            if size[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(image, size[1], size[0], step, qformat)
        img = img.rgbSwapped()
        self.image_1.setPixmap(QPixmap.fromImage(img))
        self.resize(self.image_1.pixmap().size())

    ## Rectangle button function
    #
    # Enable flags to draw rectangle in picture
    # @param self The object pointer.
    def rectangle_(self):
        self.b_bg.setEnabled(True)
        self.b_fg.setEnabled(True)
        self.b_it.setEnabled(True)
        self.flag_rect = True
        self.flag_circle_fg = False
        self.flag_circle_bg = False
        self.ini_points = []
        self.ti = time()

    ## Background button function
    #
    # Enable flags to draw the background
    # @param self The object pointer.
    def background_(self):
        self.flag_rect = False
        self.flag_circle_fg = False
        self.flag_circle_bg = True

    ## Foreground button function
    #
    # Enable flags to draw the foreground
    # @param self The object pointer.
    def foreground_(self):
        self.flag_rect = False
        self.flag_circle_fg = True
        self.flag_circle_bg = False

    ## Iteration button function
    #
    # Iteration to make the segmented image
    # @param self The object pointer.
    def iteration_(self):
        self.b_sav.setEnabled(True)
        self.b_new.setEnabled(True)
        self.b_or.setEnabled(True)
        self.b_seg.setEnabled(True)
        self.b_lab.setEnabled(True)
        self.flag_save = 1
        self.flag_rect = False
        self.flag_circle_fg = False
        self.flag_circle_bg = False
        cv2.grabCut(self.img_in, self.mask, None, self.BGD_model,
                    self.FGD_model, 1, cv2.GC_INIT_WITH_MASK)
        comp = (self.mask == 1) | (self.mask == 3)
        self.m_out = np.where(comp, 1, 0).astype('uint8')
        self.out = cv2.bitwise_and(self.img_in, self.img_in, mask=self.m_out)
        self.showImage_(self.out)

    ## Dark theme function
    #
    # Set dark or white theme
    # @param self The object pointer.
    def dark_(self):
        if self.dark.isChecked() is True:
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            palette.setColor(QPalette.Disabled, QPalette.Base, 
                             QColor(52, 52, 52))
            palette.setColor(QPalette.Disabled, QPalette.Text, 
                             QColor(57, 57, 57))
            palette.setColor(QPalette.Disabled, QPalette.Button, 
                             QColor(47, 47, 47))
            palette.setColor(QPalette.Disabled, QPalette.ButtonText, 
                             QColor(67, 67, 67))
            palette.setColor(QPalette.Disabled, QPalette.Window, 
                             QColor(49, 49, 49))
            palette.setColor(QPalette.Disabled, QPalette.WindowText, 
                             QColor(57, 57, 57))
            self.setPalette(palette)
        if self.dark.isChecked() is False:
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(239, 239, 239))
            palette.setColor(QPalette.WindowText, Qt.black)
            self.setPalette(palette)

    ## Show alert function
    #
    # Show alert when the labelled picture is not save
    # @param self The object pointer.
    def show_alert(self):
        warning = QMessageBox(self)
        warning.setIcon(QMessageBox.Warning)
        warning.setText("Remember to save the results")
        warning.setWindowTitle("Warning")
        warning.exec_()

    ## Maximized function
    #
    # Maximized window
    # @param self The object pointer.
    def maximized(self):
        self.showMaximized()

    ## Full-screen function
    #
    # Full-screen window
    # @param self The object pointer.
    def fullScreen_(self):
        if self.fs.isChecked() is True:
            self.showFullScreen()
        else:
            self.showMaximized()

    ## Mouse move function
    #
    # Make the rectangle or circles when user is pressing the mouse
    # @param self The object pointer.
    #  @param event The mouse event.
    def mouse_move(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if self.flag_rect is True:
            img_temp_m = self.img_in.copy()
            self.fin_points = [x, y]
            self.img_copy = cv2.rectangle(img_temp_m, tuple(self.ini_points), 
                                          tuple(self.fin_points), (0, 0, 255), 
                                          5)
        if ((self.flag_circle_fg is True) and (self.start is True)):
            cv2.circle(self.img_copy, (x, y), 3, (255, 255, 255), -1)
            cv2.circle(self.mask, (x, y), 5, 1, -1)
        if ((self.flag_circle_bg is True) and (self.start is True)):
            cv2.circle(self.img_copy, (x, y), 3, (0, 0, 0), -1)
            cv2.circle(self.mask, (x, y), 5, 0, -1)
        self.showImage_(self.img_copy)

    ## Mouse down function
    #
    # Make the initial points of the rectangle or start circles
    # @param self The object pointer.
    #  @param event The mouse event.
    def mouse_down(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if self.flag_rect is True:
            self.ini_points = [x, y]
        if ((self.flag_rect is False) and ((self.flag_circle_fg is True) 
            or (self.flag_circle_bg is True))):
            self.start = True

    ## Mouse up function
    #
    # Make the final points of the rectangle or finish circles
    # @param self The object pointer.
    #  @param event The mouse event.
    def mouse_up(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if self.flag_rect is True:
            img_temp = self.img_in.copy()
            self.fin_points = [x, y]
            self.img_copy = cv2.rectangle(img_temp, tuple(self.ini_points),
                                          tuple(self.fin_points), (0, 0, 255),
                                          5)
            self.mask = np.zeros((480, 640), np.uint8)
            self.mask = cv2.rectangle(self.mask, tuple(self.ini_points), 
                                      tuple(self.fin_points), 3, -1)
            self.flag_rect = False
        self.start = False
        self.showImage_(self.img_copy)

    ## Reset function
    #
    # Reset app
    # @param self The object pointer.
    def reset_(self):
        self.flag_file = 0
        self.d_time = np.zeros((10000, 3), dtype='U255')
        self.d_time[0, ...] = ['Img. Original', 'Img. Mask', 'Time (s)']
        self.BGD_model = np.zeros((1, 65), np.float64)
        self.FGD_model = np.zeros((1, 65), np.float64)
        self.ini_points, self.fin_points = [], []
        self.flag_rect = False
        self.flag_circle_fg = False
        self.flag_circle_bg = False
        self.start = False
        self.mask = np.zeros((640, 480), np.uint8)
        img = cv2.imread('media/.icons/INTRO.png', 1)
        img = cv2.resize(img, (640, 480))
        self.colors = np.random.randint(20, 255, (len(self.labels) - 1, 3))
        self.colors = []
        for n in range(len(self.labels) - 1):
            color = []
            for _ in range(3):
                color.append(random.randrange(0, 255))
            self.colors.append(tuple(color))
        self.showImage_(img)

    ## @var flag_file
    # It takes 0 value when the user hasn't chosen a file
    #
    # It takes 1 value when the user choose a file

    ## @var b_rec
    # Rectangle push button variable

    ## @var b_bg
    # Background push button variable

    ## @var b_fg
    # Foreground push button variable

    ## @var b_it
    # Iteration push button variable

    ## @var spin
    # Value of video frame variable at spin box

    ## @var b_new
    # New push button variable

    ## @var labels
    # List of labels that the user wrote on the labels.txt

    ## @var Label_n
    # List of labels

    ## @var b_or
    # Original image push button variable

    ## @var b_seg
    # Segmented image push button variable

    ## @var b_lab
    # Labelled image push button variable

    ## @var b_pre
    # Previous image push button variable

    ## @var b_nxt
    # Next image push button variable

    ## @var b_sav
    # Save image push button variable

    ## @var image_1
    # Image panel variable

    ## @var dark
    # Dark theme checkbox variable

    ## @var fs
    # Full screen checkbox variable

    ## @var colors
    # Variable of random colors generated when the application begins or 
    # restart

    ## @var value_sp
    # Value at video frame spin box

    ## @var flag_save
    # It takes 0 value when the user hasn't saved a file
    #
    # It takes 1 value when the user save a file

    ## @var file_vid
    # It takes 0 value when the file is an image
    #
    # It takes 1 value when the file is a video

    ## @var flag_vid
    # Overflow when video frame is the first or the last

    ## @var d_time
    # List with the data of timestamps.csv

    ## @var file_num
    # Number of file that shows the image panel

    ## @var frame_num
    # Number of frame

    ## @var img_in
    # Input image or frame

    ## @var img_copy
    # Copy of input image or frame

    ## @var img_out
    # Output image

    ## @var img_label
    # Output labelled image

    ## @var vid
    # Video frame

    ## @var length
    # Length of video frames

    ## @var frame_act
    # Actual video frame

    ## @var flag_rect
    # It takes 0 value when the user hasn't pressed rectangle push button
    #
    # It takes 1 value when the user press rectangle push button

    ## @var flag_circle_fg
    # It takes 0 value when the user hasn't pressed foreground push button
    #
    # It takes 1 value when the user press foreground push button

    ## @var flag_circle_bg
    # It takes 0 value when the user hasn't pressed background push button
    #
    # It takes 1 value when the user press background push button

    ## @var ini_points
    # Initial coordinates of mouse at image panel after the rectangle push
    # button was pressed

    ## @var ti
    # Previous time. This variable is update after the rectangle push button
    # was pressed

    ## @var mask
    # Output mask of Grabcut algorithm. It can It takes 4 posible values:
    #
    # 0 - True background
    # 1 - True foreground
    # 2 - Possible background
    # 3 - Possible foreground

    ## @var m_out
    # Output mask. 0 and 2 values It takess 0 value; 1 and 3 values It takess 1 value.

    ## @var out
    # Out of segmented image

    ## @var fin_points
    # When the mouse is moving, it It takess the actual value of mouse coordinates
    # 
    # When the mouse is up, it It takess the last value of mouse coordinates when
    # it was moving

    ## @var start
    # It takes 0 value when the user hasn't pressed background or foreground push
    # button. Can It takes 0 value when the user press background or foreground
    # push button and up the mouse in the image panel
    #
    # It takes 1 value when the user press background or foreground push button
    # and press the mouse in the image panel


    ## @var BGD_model
    # Variable exclusive of Grabcut algorithm

    ## @var FGD_model
    # Variable exclusive of Grabcut algorithm


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())
