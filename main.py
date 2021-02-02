# ---------------------------------------------------------------------
# Pontificia Universidad Javeriana
# Electronic Enginnering
# Developed by:
# - Andrea Juliana Ruiz Gomez
#       Mail: <andrea_ruiz@javeriana.edu.co> 
#       GitHub: <andrearuizg>
# - Pedro Eli Ruiz Zarate 
#       Mail: <pedro.ruiz@javeriana.edu.co> 
#       GitHub: <PedroRuizCode>
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import numpy as np
from time import time
import random

# ---------------------------------------------------------------------
class GUI(QMainWindow):

    # ---------------------------------------------------------------------
    def __init__(self):
        super().__init__()
        app.setStyle('Fusion')

        # Screen configuration
        screen = app.primaryScreen()
        rect = screen.size()
        width = rect.width()
        height = rect.height() - 30

        self.setGeometry(10, 10, width, height)
        self.setWindowTitle("Kiwi & PUJ - Labelling software")

        self.flag_file = 0

        # Rectangle button
        self.a = QPushButton(self)
        self.a.setText('&Rectangle')
        self.a.move(((width // 2) - 210), 15)
        self.a.setEnabled(False)
        self.a.setShortcut('Ctrl+r')
        self.a.clicked.connect(self.rectangle_)

        # Background button
        self.b = QPushButton(self)
        self.b.setText('&Background')
        self.b.move(((width // 2) - 105), 15)
        self.b.setEnabled(False)
        self.b.setShortcut('Ctrl+b')
        self.b.clicked.connect(self.background_)

        # Foreground button
        self.c = QPushButton(self)
        self.c.setText('&Foreground')
        self.c.move(width // 2, 15)
        self.c.setEnabled(False)
        self.c.setShortcut('Ctrl+f')
        self.c.clicked.connect(self.foreground_)

        # Iteration button
        self.d = QPushButton(self)
        self.d.setText('&Iteration')
        self.d.move(((width // 2) + 105), 15)
        self.d.setEnabled(False)
        self.d.setShortcut('Ctrl+i')
        self.d.clicked.connect(self.iteration_)

        # Open file button
        f = QPushButton(self)
        f.setText('&Open file')
        f.setIcon(QIcon('media/.icons/file.png'))
        f.move(10, 15)
        f.setShortcut('Ctrl+o')
        f.clicked.connect(self.open_)

        # Video frames label
        t1 = QLabel(self)
        t1.setText("Video frames")
        t1.move(10, height - 175)

        # Video frames spin box
        self.spin = QSpinBox(self)
        self.spin.move(10, height - 150)
        self.spin.setValue(30)
        self.spin.setRange(1, 999)
        self.spin.valueChanged.connect(self.sh_spin_val)

        # Labels label
        t1 = QLabel(self)
        t1.setText("Labels")
        t1.move(10, 90)

        # New label button
        self.Button_n = QPushButton(self)
        self.Button_n.setText('&New')
        self.Button_n.setIcon(QIcon('media/.icons/new.png'))
        self.Button_n.setEnabled(False)
        self.Button_n.setShortcut('Ctrl+n')
        self.Button_n.move(10, 120)
        self.Button_n.clicked.connect(self.new_label)

        # Read label list
        labels = open('/tmp/labels.txt', 'r').read()
        self.labels = list(labels.split("\n")) 

        # Label list
        self.Label_n = QComboBox(self)
        for n in range(len(self.labels)-1):
            self.Label_n.addItem(self.labels[n])
        self.Label_n.move(10, 150)
        self.Label_n.setEnabled(False)
        self.Label_n.activated[str].connect(self.sel_LN)

        # Show image label
        t2 = QLabel(self)
        t2.setText("Show image")
        t2.move(10, height // 2)

        # Original image button
        self.b_or = QPushButton(self)
        self.b_or.setText('Original')
        self.b_or.move(10, (height // 2) + 30)
        self.b_or.setEnabled(False)
        self.b_or.clicked.connect(self.b_or_)

        # Segmented image button
        self.b_seg = QPushButton(self)
        self.b_seg.setText('Segmented')
        self.b_seg.move(10, (height // 2) + 60)
        self.b_seg.setEnabled(False)
        self.b_seg.clicked.connect(self.b_seg_)

        # Labelled image button
        self.b_lab = QPushButton(self)
        self.b_lab.setText('Labels')
        self.b_lab.move(10, (height // 2) + 90)
        self.b_lab.setEnabled(False)
        self.b_lab.clicked.connect(self.b_lab_)

        # Previous image button
        self.b_pre = QPushButton(self)
        self.b_pre.setText('Previous')
        self.b_pre.setIcon(QIcon('media/.icons/undo.png'))
        self.b_pre.move(10, height - 110)
        self.b_pre.setShortcut('Ctrl+Left')
        self.b_pre.setEnabled(False)
        self.b_pre.clicked.connect(self.b_pre_)

        # Next image button
        self.b_nxt = QPushButton(self)
        self.b_nxt.setText('Next')
        self.b_nxt.setIcon(QIcon('media/.icons/redo.png'))
        self.b_nxt.move(10, height - 80)
        self.b_nxt.setShortcut('Ctrl+Right')
        self.b_nxt.setEnabled(False)
        self.b_nxt.clicked.connect(self.b_nxt_)

        # Save labels button
        self.b_sav = QPushButton(self)
        self.b_sav.setText('&SAVE')
        self.b_sav.setIcon(QIcon('media/.icons/save.png'))
        self.b_sav.move(10, height - 30)
        self.b_sav.setEnabled(False)
        self.b_sav.setShortcut('Ctrl+s')
        self.b_sav.clicked.connect(self.b_sav_)

        # Exit button
        b_ext = QPushButton(self)
        b_ext.setText('EXIT')
        b_ext.setIcon(QIcon('media/.icons/exit.png'))
        b_ext.move(width - 110, height - 30)
        b_ext.clicked.connect(self.b_ext_)

        # App reset button
        b_res = QPushButton(self)
        b_res.setText('RESET')
        b_res.move(width - 110, height - 80)
        b_res.clicked.connect(self.reset_)

        # Image
        self.image_1 = QLabel(self)
        self.image_1.resize(640, 480)
        self.image_1.move((width // 2) - 320, (height // 2) - 200)

        # Dark theme check box
        self.dark = QCheckBox(self)
        self.dark.setText('Dark theme')
        self.dark.setChecked(True)
        self.dark.move((width - 110), 15)
        self.dark.toggled.connect(self.dark_)

        # Full screen check box
        self.fs = QCheckBox(self)
        self.fs.setText('Full Screen')
        self.fs.setChecked(True)
        self.fs.move((width - 110), 35)
        self.fs.toggled.connect(self.fullScreen_)

        # Functions called for initial configurations
        self.fullScreen_()
        self.show()
        self.reset_()
        self.dark_()

        # Mouse events definition
        self.image_1.mousePressEvent = self.mouse_down
        self.image_1.mouseMoveEvent = self.mouse_move
        self.image_1.mouseReleaseEvent = self.mouse_up

    # ---------------------------------------------------------------------
    # Label selection function
    # Select the label of the segmented image, and created the labelled image file
    def sel_LN(self, text):
        for n in range(len(self.labels)-1):
            if text == self.labels[n]:
                self.contour_()
                self.colors=tuple(self.colors)
                cv2.drawContours(self.img_out, self.contours, -1, n+1, thickness=cv2.FILLED)
                cv2.drawContours(self.img_label, self.contours, -1, self.colors[n], thickness=cv2.FILLED)
        
    # ---------------------------------------------------------------------
    # Contour function
    # Determine the contour of the segmented image
    def contour_(self):
        imgray = cv2.cvtColor(self.output, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 1, 255, 0)
        self.contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # ---------------------------------------------------------------------
    # New label button function
    # Set enable flag true
    def new_label(self):
        self.Label_n.setEnabled(True)
        self.b_lab_()

    # ---------------------------------------------------------------------
    # Original picture button
    # Show original picture
    def b_or_(self):
        self.showImage_(self.img_in)

    # ---------------------------------------------------------------------
    # Segmented picture button
    # Show segmented picture
    def b_seg_(self):
        self.showImage_(self.output)

    # ---------------------------------------------------------------------
    # Labelled picture button
    # Show labelled picture
    def b_lab_(self):
        self.showImage_(self.img_label)

    # ---------------------------------------------------------------------
    # Spin value function
    # Update video frame variable
    def sh_spin_val(self):
        self.value_sp = self.spin.value()

    # ---------------------------------------------------------------------
    # Previous image button function
    # Disable buttons and show warnings
    def b_pre_(self):
        if self.flag_save == 0:
            self.b_sav.setEnabled(False)
            self.b.setEnabled(False)
            self.c.setEnabled(False)
            self.d.setEnabled(False)
            self.Button_n.setEnabled(False)
            self.Label_n.setEnabled(False)
            self.b_or.setEnabled(False)
            self.b_seg.setEnabled(False)
            self.b_lab.setEnabled(False)
            if self.flag_save == 1:
                self.show_alert()
            if self.file_vid == 0:
                self.i -= 1
                self.load()
            else:
                if self.flag_vid == 1:
                    self.flag_vid = 0
                    self.i -= 2
                self.frame_act -= int(self.value_sp)
                self.load_vid()
        else:
            self.flag_save = 0
            self.show_alert()

    # ---------------------------------------------------------------------
    # Next image button function
    # Disable buttons and show warnings
    def b_nxt_(self):
        if self.flag_save == 0:
            self.b_sav.setEnabled(False)
            self.b.setEnabled(False)
            self.c.setEnabled(False)
            self.d.setEnabled(False)
            self.Button_n.setEnabled(False)
            self.Label_n.setEnabled(False)
            self.b_or.setEnabled(False)
            self.b_seg.setEnabled(False)
            self.b_lab.setEnabled(False)
            if self.file_vid == 0:
                self.i += 1
                self.load()
            else:
                self.frame_act += int(self.value_sp)
                self.load_vid()
        else:
            self.flag_save = 0
            self.show_alert()

    # ---------------------------------------------------------------------
    # Save button function
    # Save files
    # - for pictures only save the labelled mask 
    # - for videos save labelled mask and original frame
    def b_sav_(self):
        if self.file_vid == 0:
            outfile = 'media/%s-mask.png' % ((self.filename[self.i].split(".")[0]).split("/")[-1])
            outfile1 = 'media/%s.png' % ((self.filename[self.i].split(".")[0]).split("/")[-1])
        else:
            outfile = 'media/%s-frame-%s-mask.png' % ((self.filename[self.i].split(".")[0]).split("/")[-1], self.frame_act)
            outfile1 = 'media/%s-frame-%s.png' % ((self.filename[self.i].split(".")[0]).split("/")[-1], self.frame_act)
        original = '%s' % self.filename[self.i].split("/")[-1]
        mask = '%s' % outfile.split("/")[-1]
        tf = '%s' % (time() - self.ti)
        self.d_time[self.j, ...] = [original, mask, tf]
        cv2.imwrite(outfile, self.img_out)
        cv2.imwrite(outfile1, self.img_in)
        self.j += 1
        self.flag_save = 0
        self.flag_file = 1

    # ---------------------------------------------------------------------
    # Exit button function
    # Save time stamps csv and close app
    def b_ext_(self):
        if self.flag_file == 1:
            np.savetxt("media/timestamps.csv", self.d_time, delimiter=", ", fmt='%s')
        self.close()
        QApplication.quit()

    # ---------------------------------------------------------------------
    # Open button function
    # Open file dialog window 
    def open_(self):
        self.filename, _ = QFileDialog.getOpenFileNames(None, 'Buscar Imagen', '.', 'Image Files (*.png *.jpg *.jpeg *.bmp *.mp4)')
        self.d_time = np.zeros((10000, 3), dtype='U255')
        self.d_time[0, ...] = ['Img. Original', 'Img. Mask', 'Time (s)']
        self.i = 0
        self.j = 1
        self.flag_save = 0
        self.flag_vid = 0
        self.file_vid = 0
        self.a.setEnabled(True)
        self.b_pre.setEnabled(True)
        self.b_nxt.setEnabled(True)
        self.load()

    # ---------------------------------------------------------------------
    # Load function
    # Open file in open cv 
    def load(self):
        self.flag_save = 0
        if self.i < len(self.filename):
            if self.filename[self.i].split(".")[-1] in ['png', 'jpg', 'jpeg', 'bmp']:
                self.img_in = cv2.imread(self.filename[self.i], cv2.IMREAD_UNCHANGED)
                self.img_in = cv2.resize(self.img_in, (640, 480))  
                self.img_copy = self.img_in.copy()  
                self.img_out = np.zeros((480, 640), np.uint8)  
                self.img_label = self.img_in.copy()  
                self.showImage_(self.img_in)
            else:
                self.file_vid = 1
                self.vid = cv2.VideoCapture(self.filename[self.i])
                self.length = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
                self.frame_act = 1
                self.load_vid()
        else:
            self.b_ext_()
        if ((self.i == 0) and (self.file_vid == 0)):
            self.b_pre.setEnabled(False)
        else:
            self.b_pre.setEnabled(True)
        if ((self.i == (len(self.filename) - 1)) and (self.file_vid == 0)):
            self.b_nxt.setEnabled(False)
        else:
            self.b_nxt.setEnabled(True)

    # ---------------------------------------------------------------------
    # Load video function
    # Open video frames 
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
                self.i += 1
                self.load()

    # ---------------------------------------------------------------------
    # Show image function
    # Show picture in Pixmap 
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

    # ---------------------------------------------------------------------
    # Rectangle button function
    # Enable flags to draw rectangle in picture
    def rectangle_(self):
        self.b.setEnabled(True)
        self.c.setEnabled(True)
        self.d.setEnabled(True)
        self.flag_rect = True  
        self.flag_circle_fg = False 
        self.flag_circle_bg = False 
        self.ini_points = []
        self.ti = time()

    # ---------------------------------------------------------------------
    # Background button function
    # Enable flags to draw the background
    def background_(self):
        self.flag_rect = False
        self.flag_circle_fg = False
        self.flag_circle_bg = True 

    # ---------------------------------------------------------------------
    # Foreground button function
    # Enable flags to draw the foreground
    def foreground_(self):
        self.flag_rect = False
        self.flag_circle_fg = True
        self.flag_circle_bg = False 

    # ---------------------------------------------------------------------
    # Iteration button function
    # Iteration to make the segmented image
    def iteration_(self):
        self.b_sav.setEnabled(True)
        self.Button_n.setEnabled(True)
        self.b_or.setEnabled(True)
        self.b_seg.setEnabled(True)
        self.b_lab.setEnabled(True)
        self.flag_save = 1
        self.flag_rect = False  
        self.flag_circle_fg = False
        self.flag_circle_bg = False
        cv2.grabCut(self.img_in, self.mask, None, self.BGD_model, self.FGD_model, 1, cv2.GC_INIT_WITH_MASK)
        self.mask_out = np.where((self.mask == 1) | (self.mask == 3), 1, 0).astype('uint8')
        # Si valor es 1 o 3 (primer plano), se cambia a 1 (primer plano seguro), valores de 0 y 2 (fondo) cambian a 0 (fondo seguro)
        self.output = cv2.bitwise_and(self.img_in, self.img_in, mask=self.mask_out)
        self.showImage_(self.output)

    # ---------------------------------------------------------------------
    # Dark theme  function
    # Set dark or white theme 
    def dark_(self):
        if self.dark.isChecked() == True:
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
            palette.setColor(QPalette.Disabled, QPalette.Base, QColor(52, 52, 52))
            palette.setColor(QPalette.Disabled, QPalette.Text, QColor(57, 57, 57))
            palette.setColor(QPalette.Disabled, QPalette.Button, QColor(47, 47, 47))
            palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(67, 67, 67))
            palette.setColor(QPalette.Disabled, QPalette.Window, QColor(49, 49, 49))
            palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(57, 57, 57))
            self.setPalette(palette)
        else:
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(239, 239, 239))
            palette.setColor(QPalette.WindowText, Qt.black)
            self.setPalette(palette)

    # ---------------------------------------------------------------------
    # Show alert function
    # Show alert when the labelled picture is not save 
    def show_alert(self):
        warning = QMessageBox(self)
        warning.setIcon(QMessageBox.Warning)
        warning.setText("Remember to save the results")
        warning.setWindowTitle("Warning")
        warning.exec_()

    # ---------------------------------------------------------------------
    # Maximized function
    # Maximized window 
    def maximized(self):
        self.showMaximized()

    # ---------------------------------------------------------------------
    # Full-screen function
    # Full-screen window 
    def fullScreen_(self):
        if self.fs.isChecked() == True:
            self.showFullScreen()
        else:
            self.showMaximized()

    # ---------------------------------------------------------------------
    # Mouse move function
    # Make the rectangle or circles when user is pressing the mouse  
    def mouse_move(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if self.flag_rect == True:
            img_temp_m = self.img_in.copy()
            self.fin_points = [x, y]
            self.img_copy = cv2.rectangle(img_temp_m, tuple(self.ini_points), tuple(self.fin_points), (0, 0, 255), 5)
        if self.flag_circle_fg == True and self.start == True:
            cv2.circle(self.img_copy, (x, y), 3, (255, 255, 255), -1)
            cv2.circle(self.mask, (x, y), 5, 1, -1)
        elif self.flag_circle_bg == True and self.start == True:
            cv2.circle(self.img_copy, (x, y), 3, (0, 0, 0), -1)
            cv2.circle(self.mask, (x, y), 5, 0, -1)
        self.showImage_(self.img_copy)

    # ---------------------------------------------------------------------
    # Mouse down function
    # Make the initial points of the rectangle or start circles
    def mouse_down(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if self.flag_rect == True:
            self.ini_points = [x, y]
        if ((self.flag_rect == False) and ((self.flag_circle_fg == True) or (self.flag_circle_bg == True))):
            self.start = True

    # ---------------------------------------------------------------------
    # Mouse up function
    # Make the final points of the rectangle or finish circles
    def mouse_up(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if self.flag_rect == True:
            img_temp = self.img_in.copy()
            self.fin_points = [x, y]
            self.img_copy = cv2.rectangle(img_temp, tuple(self.ini_points), tuple(self.fin_points), (0, 0, 255), 5)
            self.mask = np.zeros((480, 640), np.uint8)  # Mascara
            self.mask = cv2.rectangle(self.mask, tuple(self.ini_points), tuple(self.fin_points), 3, -1)
            self.corners = self.ini_points[0], self.ini_points[1], self.fin_points[0], self.fin_points[1]
            self.flag_rect = False
        self.start = False
        self.showImage_(self.img_copy)

    # ---------------------------------------------------------------------
    # Reset function
    # Reset app 
    def reset_(self):
        self.BGD_model = np.zeros((1, 65), np.float64)
        self.FGD_model = np.zeros((1, 65), np.float64)
        self.ini_points, self.fin_points, self.temp_points, self.corners = [], [], [], []
        self.flag_rect = False 
        self.flag_circle_fg = False
        self.flag_circle_bg = False
        self.start = False
        self.initial_mask = np.zeros((640, 480), np.uint8) 
        self.mask = np.zeros((640, 480), np.uint8)
        img = cv2.imread('media/.icons/INTRO.png', 1)
        img = cv2.resize(img, (640, 480))
        self.colors = np.random.randint(20,255,(len(self.labels)-1,3))
        self.colors = []
        for n in range(len(self.labels)-1):
            color = []
            for _ in range(3):
                color.append(random.randrange(0, 255))
            self.colors.append(tuple(color))
        self.showImage_(img)

# ---------------------------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())
