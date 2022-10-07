import sys
import os
import time
import xml.etree.ElementTree as ET  # https://docs.python.org/2/library/xml.etree.elementtree.html
from pathlib import Path
# from ipywidgets import Layout, Label, Text, Checkbox, Button, BoundedIntText, HBox, VBox, Box, \
    # FloatText, Dropdown, SelectMultiple, RadioButtons, interactive
# import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, Ellipse, Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.colors as mplc
from matplotlib import gridspec
from collections import deque

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QFrame,QApplication,QWidget,QTabWidget,QFormLayout,QLineEdit, QHBoxLayout,QVBoxLayout, \
    QRadioButton,QLabel,QCheckBox,QComboBox,QScrollArea,  QMainWindow,QGridLayout, QPushButton, QFileDialog, QMessageBox

import math
import numpy as np
import scipy.io  # .io.loadmat(full_fname, info_dict)
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
# from matplotlib.figure import Figure

class Vis(QWidget):
    def __init__(self):
        super().__init__()
        # global self.config_params

        self.xml_root = None
        self.frame_count = 0
        # self.current_svg_frame = 0
        self.timer = QtCore.QTimer()
        # self.t.timeout.connect(self.task)
        self.timer.timeout.connect(self.play_plot_cb)

        # self.tab = QWidget()
        # self.tabs.resize(200,5)
        
        self.use_defaults = True
        self.title_str = ""
        self.xmin = -1000
        self.xmax = 1000
        self.x_range = self.xmax - self.xmin

        self.ymin = -1000
        self.ymax = 1000
        self.y_range = self.ymax - self.ymin
        self.show_nucleus = False
        self.show_edge = False
        self.alpha = 0.7

        self.cell_mod = 1
        self.substrate_mod = 1

        # self.cells_toggle = None
        # self.substrates_toggle = None

        basic_length = 12.0
        basic_length = 10.0
        self.figsize_width_substrate = 18.0  # allow extra for colormap
        self.figsize_width_substrate = 12.0  # allow extra for colormap
        self.figsize_height_substrate = basic_length

        self.figsize_width_2Dplot = basic_length
        self.figsize_height_2Dplot = basic_length

        # rwh: TODO these params
        self.modulo = 1
        self.field_index = 4   # "4" is the 0th substrate
        # define dummy size of mesh (set in the tool's primary module)
        self.numx = 0
        self.numy = 0
        self.colormap_min = 0.5
        self.colormap_max = 1.0
        self.colormap_fixed_toggle = False
        # self.fontsize = 10
        self.fontsize = 5

        # self.canvas = None
        self.first_time = True


        # self.width_substrate = basic_length  # allow extra for colormap
        # self.height_substrate = basic_length

        self.figsize_width_svg = basic_length
        self.figsize_height_svg = basic_length

        # self.output_dir = "/Users/heiland/dev/PhysiCell_V.1.8.0_release/output"
        self.output_dir = "./output"

        self.customized_output_freq = False

        #-------------------------------------------
        label_width = 110
        domain_value_width = 100
        value_width = 60
        label_height = 20
        units_width = 70

        # self.create_figure()

        self.scroll = QScrollArea()  # might contain centralWidget

        self.config_params = QWidget()

        self.main_layout = QVBoxLayout()

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(0)

        # self.substrates_toggle = None

        #------------------
        controls_vbox = QVBoxLayout()
        
        controls_hbox = QHBoxLayout()
        w = QPushButton("Directory")
        w.clicked.connect(self.open_directory_cb)
        controls_hbox.addWidget(w)

        # self.output_dir = "/Users/heiland/dev/PhysiCell_V.1.8.0_release/output"
        self.output_dir_w = QLineEdit()
        self.output_dir_w.setText("./output")
        # w.setText("/Users/heiland/dev/PhysiCell_V.1.8.0_release/output")
        # w.setText(self.output_dir)
        # w.textChanged[str].connect(self.output_dir_changed)
        # w.textChanged.connect(self.output_dir_changed)
        controls_hbox.addWidget(self.output_dir_w)

        self.back0_button = QPushButton("<<")
        self.back0_button.clicked.connect(self.back0_plot_cb)
        controls_hbox.addWidget(self.back0_button)

        self.back_button = QPushButton("<")
        self.back_button.clicked.connect(self.back_plot_cb)
        controls_hbox.addWidget(self.back_button)

        self.forward_button = QPushButton(">")
        self.forward_button.clicked.connect(self.forward_plot_cb)
        controls_hbox.addWidget(self.forward_button)

        self.play_button = QPushButton("Play")
        # self.play_button.clicked.connect(self.play_plot_cb)
        self.play_button.clicked.connect(self.animate)
        controls_hbox.addWidget(self.play_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setEnabled(False)
        # self.play_button.clicked.connect(self.play_plot_cb)
        self.reset_button.clicked.connect(self.reset_plot_cb)
        controls_hbox.addWidget(self.reset_button)
        controls_vbox.addLayout(controls_hbox)

        #-------------
        hbox = QHBoxLayout()

        widget_width = 60
        self.cells_toggle = QCheckBox("cells")
        self.cells_toggle.setFixedWidth(widget_width)
        self.cells_toggle.setChecked(True)
        self.cells_toggle.stateChanged.connect(self.cells_toggle_cb)
        hbox.addWidget(self.cells_toggle)

        label = QLabel("mod")
        label.setFixedWidth(30)
        label.setAlignment(QtCore.Qt.AlignRight)
        hbox.addWidget(label)

        self.cell_mod_val = QLineEdit()
        self.cell_mod_val.setFixedWidth(50)
        self.cell_mod_val.setText(str(self.cell_mod))
        self.cell_mod_val.textChanged.connect(self.cell_modulo_cb)
        self.cell_mod_val.setValidator(QtGui.QIntValidator())
        hbox.addWidget(self.cell_mod_val)

        self.cells_edges_toggle = QCheckBox("edges")
        self.cells_edges_toggle.setFixedWidth(widget_width)
        self.cells_edges_toggle.setChecked(False)
        self.cells_edges_toggle.stateChanged.connect(self.cells_edges_toggle_cb)
        hbox.addWidget(self.cells_edges_toggle)

        self.substrates_toggle = QCheckBox("substrates")
        self.substrates_toggle.setFixedWidth(100)
        self.substrates_toggle.setEnabled(False)
        self.substrates_toggle.setChecked(True)
        self.substrates_toggle.stateChanged.connect(self.substrates_toggle_cb)
        hbox.addWidget(self.substrates_toggle)

        label = QLabel("mod")
        label.setFixedWidth(30)
        label.setAlignment(QtCore.Qt.AlignRight)
        hbox.addWidget(label)

        self.substrate_mod_val = QLineEdit()
        self.substrate_mod_val.setFixedWidth(50)
        self.substrate_mod_val.setText(str(self.substrate_mod))
        self.substrate_mod_val.textChanged.connect(self.substrate_modulo_cb)
        self.substrate_mod_val.setValidator(QtGui.QIntValidator())
        hbox.addWidget(self.substrate_mod_val)

        self.substrate_dropdown = QComboBox()
        self.substrate_dropdown.setFixedWidth(250)
        # self.cycle_dropdown.currentIndex.connect(self.cycle_changed_cb)
        self.substrate_dropdown.currentIndexChanged.connect(self.substrate_changed_cb)
        # self.substrate_dropdown.addItem("foo")
        hbox.addWidget(self.substrate_dropdown)

        controls_vbox.addLayout(hbox)

        # self.prepare_button = QPushButton("Prepare")
        # self.prepare_button.clicked.connect(self.prepare_plot_cb)
        # controls_hbox.addWidget(self.prepare_button)

        #==================================================================
        self.config_params.setLayout(self.vbox)

        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)

        self.create_figure()

        # self.scroll.setWidget(self.config_params) # self.config_params = QWidget()
        self.scroll.setWidget(self.canvas) # self.config_params = QWidget()
        self.layout = QVBoxLayout(self)
        # self.layout.addLayout(controls_hbox)
        self.layout.addLayout(controls_vbox)

        self.layout.addWidget(self.scroll)


        self.reset_plot_cb("")


    def open_directory_cb(self):
        dialog = QFileDialog()
        dir_path = dialog.getExistingDirectory(self, 'Select an output directory')
        print("open_directory_cb:  output_dir=",dir_path)
        # if self.output_dir is "":
        if dir_path == "":
            return

        self.output_dir = dir_path

        self.output_dir_w.setText(self.output_dir)
        # Verify initial.xml and at least one .svg file exist. Obtain bounds from initial.xml
        # tree = ET.parse(self.output_dir + "/" + "initial.xml")
        xml_file = Path(self.output_dir, "initial.xml")
        if not os.path.isfile(xml_file):
            print("Expecting initial.xml, but does not exist.")
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Did not find 'initial.xml' in this directory.")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            return

        tree = ET.parse(Path(self.output_dir, "initial.xml"))
        xml_root = tree.getroot()

        bds_str = xml_root.find(".//microenvironment//domain//mesh//bounding_box").text
        bds = bds_str.split()
        print('bds=',bds)
        self.xmin = float(bds[0])
        self.xmax = float(bds[3])
        self.x_range = self.xmax - self.xmin

        self.ymin = float(bds[1])
        self.ymax = float(bds[4])
        self.y_range = self.ymax - self.ymin

        # and plot 1st frame (.svg)
        self.current_svg_frame = 0
        self.forward_plot_cb("")  


    def cells_toggle_cb(self):
        self.plot_substrate()
        self.canvas.update()
        self.canvas.draw()

    def cell_modulo_cb(self, text):
        print("cell_modulo_cb(): text = ",text)
        if len(text) > 0:
            self.cell_mod = int(text)

    def cells_edges_toggle_cb(self,bval):
        self.show_edge = bval
        self.plot_substrate()
        self.canvas.update()
        self.canvas.draw()

    def substrates_toggle_cb(self):
        self.plot_substrate()
        self.canvas.update()
        self.canvas.draw()

    def substrate_modulo_cb(self, text):
        print("substrate_modulo_cb(): text = ",text)
        if len(text) > 0:
            self.substrate_mod = int(text)

    def substrate_changed_cb(self):
        print("\n== substrate_changed_cb(): ", self.substrate_dropdown.currentText(),self.substrate_dropdown.currentIndex() )
        if not self.first_time:
            self.field_index = int(self.substrate_dropdown.currentIndex()) + 4
            self.plot_substrate()
            print("== substrate_changed_cb():  self.field_index =  ",self.field_index )
            self.canvas.update()
            self.canvas.draw()
        else:
            self.first_time = False
        

    # def output_dir_changed(self, text):
    #     self.output_dir = text
    #     print(self.output_dir)

    def back0_plot_cb(self, text):
        self.frame_count = 0
        print('frame # ',self.frame_count)
        self.plot_substrate()
        # self.canvas.update()
        self.canvas.draw()
        self.timer.stop()

    def back_plot_cb(self, text):
        self.frame_count -= 1
        if self.frame_count < 0:
            self.frame_count = 0
        print('frame # ',self.frame_count)
        self.plot_substrate()
        # self.plot_svg(self.current_svg_frame)

        # self.canvas.update()
        self.canvas.draw()

    def forward_plot_cb(self, text):
        self.frame_count += 1
        print('frame # ',self.frame_count)
        self.plot_substrate()
        # self.plot_svg(self.current_svg_frame)
        # self.canvas.update()
        self.canvas.draw()

    def reset_plot_cb(self, text):
        print("-------------- reset_plot_cb() ----------------")
        # self.create_figure()

        xml_file = Path(self.output_dir, "initial.xml")
        if not os.path.isfile(xml_file):
            print("Expecting initial.xml, but does not exist.")
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Did not find 'initial.xml' in this directory.")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            return

        # if self.first_time:
        #     self.first_time = False
        #     full_xml_filename = Path(os.path.join(self.output_dir, 'config.xml'))
        #     if full_xml_filename.is_file():
        #         tree = ET.parse(full_xml_filename)  # this file cannot be overwritten; part of tool distro
        #         xml_root = tree.getroot()
        #         self.svg_delta_t = int(xml_root.find(".//SVG//interval").text)
        #         self.substrate_delta_t = int(xml_root.find(".//full_data//interval").text)
        #         # print("---- svg,substrate delta_t values=",self.svg_delta_t,self.substrate_delta_t)        
        #         self.modulo = int(self.substrate_delta_t / self.svg_delta_t)
        #         # print("---- modulo=",self.modulo)        

        # all_files = sorted(glob.glob(os.path.join(self.output_dir, 'snap*.svg')))   # if .svg
        # if len(all_files) > 0:
        #     last_file = all_files[-1]
        #     # print("substrates.py/update(): len(snap*.svg) = ",len(all_files)," , last_file=",last_file)
        #     self.max_frames.value = int(last_file[-12:-4])  # assumes naming scheme: "snapshot%08d.svg"
        # else:
        #     substrate_files = sorted(glob.glob(os.path.join(self.output_dir, 'output*.xml')))
        #     if len(substrate_files) > 0:
        #         last_file = substrate_files[-1]
        #         self.max_frames.value = int(last_file[-12:-4])


        tree = ET.parse(Path(self.output_dir, "initial.xml"))
        xml_root = tree.getroot()

        bds_str = xml_root.find(".//microenvironment//domain//mesh//bounding_box").text
        bds = bds_str.split()
        print('bds=',bds)
        self.xmin = float(bds[0])
        self.xmax = float(bds[3])
        self.x_range = self.xmax - self.xmin

        self.ymin = float(bds[1])
        self.ymax = float(bds[4])
        self.y_range = self.ymax - self.ymin

        # self.numx =  math.ceil( (self.xmax - self.xmin) / config_tab.xdelta.value)
        # self.numy =  math.ceil( (self.ymax - self.ymin) / config_tab.ydelta.value)
        self.numx =  math.ceil( (self.xmax - self.xmin) / 20.)
        self.numy =  math.ceil( (self.ymax - self.ymin) / 20.)
        print(" calc: numx,numy = ",self.numx, self.numy)

        vars_uep = xml_root.find(".//microenvironment//domain//variables")
        self.substrates = []
        self.substrate_dropdown.clear()
        for var in vars_uep.findall("variable"):
            print(" substrate name = ",var.attrib["name"])
            self.substrates.append(var.attrib["name"])
            self.substrate_dropdown.addItem(var.attrib["name"])


        self.cbar = None

        self.frame_count = 0
        self.plot_substrate()
        # self.plot_svg(self.current_svg_frame)
        # self.canvas.clear()
        self.canvas.update()
        self.canvas.draw()


    # def task(self):
            # self.dc.update_figure()
    def play_plot_cb(self):
        for idx in range(1):
            self.frame_count += 1
            print('frame # ',self.frame_count)

            self.current_svg_frame = int(self.frame_count / self.cell_mod)

            fname = "snapshot%08d.svg" % self.current_svg_frame
            full_fname = os.path.join(self.output_dir, fname)
            # print("full_fname = ",full_fname)
            # with debug_view:
                # print("plot_svg:", full_fname) 
            # print("-- plot_svg:", full_fname) 
            if not os.path.isfile(full_fname):
                # print("Once output files are generated, click the slider.")   
                print("ERROR:  filename not found.")
                self.frame_count -= 1
                self.timer.stop()
                return

            self.plot_substrate()
            # self.plot_svg(self.current_svg_frame)
            self.canvas.update()
            self.canvas.draw()

    def animate(self, text):
        self.frame_count = 0
        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.play_plot_cb)
        # self.timer.start(2000)  # every 2 sec
        # self.timer.start(100)
        self.timer.start(50)

    # def play_plot_cb0(self, text):
    #     for idx in range(10):
    #         self.current_svg_frame += 1
    #         print('svg # ',self.current_svg_frame)
    #         self.plot_svg(self.current_svg_frame)
    #         self.canvas.update()
    #         self.canvas.draw()
    #         # time.sleep(1)
    #         # self.ax0.clear()
    #         # self.canvas.pause(0.05)

    # def prepare_plot_cb(self, text):
    #     self.current_svg_frame += 1
    #     print('svg # ',self.current_svg_frame)
    #     # self.plot_substrate(self.current_svg_frame)
    #     self.plot_svg(self.current_svg_frame)
    #     self.canvas.update()
    #     self.canvas.draw()

    def create_figure(self):
        # self.figure = plt.figure()
        # self.figure = plt.figure(figsize=(self.figsize_width_substrate, self.figsize_height_substrate))
        self.fig, (self.ax0) = plt.subplots(1,1, figsize=(self.figsize_width_substrate, 
                        self.figsize_height_substrate))
        # self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas = FigureCanvasQTAgg(self.fig)
        # self.canvas.setStyleSheet("background-color:transparent;")

        # Adding one subplot for image
        # self.ax0 = self.figure.add_subplot(111, frameon=True)
        # self.ax0 = self.figure.add_axes([0.1,0.1,0.8,0.8])

        # self.fig = plt.figure(figsize=(self.figsize_width_substrate, self.figsize_height_substrate))
        # self.ax0 = plt.figure(figsize=(self.figsize_width_substrate, self.figsize_height_substrate))

        # self.ax0.get_xaxis().set_visible(True)
        # self.ax0.get_yaxis().set_visible(True)

        # self.ax0.set_frame_on(True)

        print(mpl.rcParams['axes.edgecolor'])
        # self.ax0.grid(True, linestyle='-.')
        # plt.tight_layout()
        # self.ax0.tight_layout()

        # np.random.seed(19680801)  # for reproducibility
        # N = 50
        # x = np.random.rand(N) * 2000
        # y = np.random.rand(N) * 2000
        # colors = np.random.rand(N)
        # area = (30 * np.random.rand(N))**2  # 0 to 15 point radii
        # self.ax0.scatter(x, y, s=area, c=colors, alpha=0.5)

        self.plot_substrate()

        # self.ax0.get_xaxis().set_visible(True)
        # self.ax0.get_yaxis().set_visible(True)

        # self.plot_svg(self.current_svg_frame)

        # self.imageInit = [[255] * 320 for i in range(240)]
        # self.imageInit[0][0] = 0

        # Init image and add colorbar
        # self.image = self.ax0.imshow(self.imageInit, interpolation='none')
        # divider = make_axes_locatable(self.ax0)
        # cax = divider.new_vertical(size="5%", pad=0.05, pack_start=True)
        # self.colorbar = self.figure.add_axes(cax)
        # self.figure.colorbar(self.image, cax=cax, orientation='horizontal')

        # plt.subplots_adjust(left=0, bottom=0.05, right=1, top=1, wspace=0, hspace=0)

        self.canvas.draw()

    #---------------------------------------------------------------------------
    def ellipses(self, x, y, w,h,a, c='b', vmin=None, vmax=None, **kwargs):

        if np.isscalar(c):
            kwargs.setdefault('color', c)
            c = None

        if 'fc' in kwargs:
            kwargs.setdefault('facecolor', kwargs.pop('fc'))
        if 'ec' in kwargs:
            kwargs.setdefault('edgecolor', kwargs.pop('ec'))
        if 'ls' in kwargs:
            kwargs.setdefault('linestyle', kwargs.pop('ls'))
        if 'lw' in kwargs:
            kwargs.setdefault('linewidth', kwargs.pop('lw'))
        # You can set `facecolor` with an array for each patch,
        # while you can only set `facecolors` with a value for all.

# ww = X / 10.0
# hh = Y / 15.0
# aa = X * 9
# fig, ax = plt.subplots()
# ec = EllipseCollection(ww, hh, aa, units='x', offsets=XY, offset_transform=ax.transData)

        zipped = np.broadcast(x, y, w,h,a)
        patches = [Ellipse((x_, y_), w_, h_, a_)
                for x_, y_, w_, h_, a_ in zipped]
        collection = PatchCollection(patches, **kwargs)
        if c is not None:
            c = np.broadcast_to(c, zipped.shape).ravel()
            collection.set_array(c)
            collection.set_clim(vmin, vmax)

        # ax = plt.gca()
        self.ax0.add_collection(collection)
        self.ax0.autoscale_view()
        # plt.draw_if_interactive()
        if c is not None:
            # plt.sci(collection)
            self.ax0.sci(collection)
        # return collection


    #------------------------------------------------------------
    # def plot_svg(self, frame, rdel=''):
    def plot_svg(self):
        # global current_idx, axes_max
        global current_frame

        # fname = "snapshot%08d.svg" % frame
        fname = "snapshot%08d.svg" % self.frame_count
        full_fname = os.path.join(self.output_dir, fname)
        print("full_fname = ",full_fname)
        # with debug_view:
            # print("plot_svg:", full_fname) 
        print("-- plot_svg:", full_fname) 
        if not os.path.isfile(full_fname):
            # print("Once output files are generated, click the slider.")   
            print("ERROR:  filename not found.")   
            return

        # self.ax0.cla()
        # ax.cla()
        self.title_str = ""

        xlist = deque()
        ylist = deque()
        rxlist = deque()
        rylist = deque()
        rotlist = deque()
        rgb_list = deque()

        #  print('\n---- ' + fname + ':')
#        tree = ET.parse(fname)
        tree = ET.parse(full_fname)
        root = tree.getroot()
        #  print('--- root.tag ---')
        #  print(root.tag)
        #  print('--- root.attrib ---')
        #  print(root.attrib)
        #  print('--- child.tag, child.attrib ---')
        numChildren = 0
        for child in root:
            #    print(child.tag, child.attrib)
            #    print("keys=",child.attrib.keys())
            if self.use_defaults and ('width' in child.attrib.keys()):
                self.axes_max = float(child.attrib['width'])
                # print("debug> found width --> axes_max =", axes_max)
            if child.text and "Current time" in child.text:
                svals = child.text.split()
                # remove the ".00" on minutes
                self.title_str += "   cells: " + svals[2] + "d, " + svals[4] + "h, " + svals[7][:-3] + "m"

                # self.cell_time_mins = int(svals[2])*1440 + int(svals[4])*60 + int(svals[7][:-3])
                # self.title_str += "   cells: " + str(self.cell_time_mins) + "m"   # rwh

            # print("width ",child.attrib['width'])
            # print('attrib=',child.attrib)
            # if (child.attrib['id'] == 'tissue'):
            if ('id' in child.attrib.keys()):
                # print('-------- found tissue!!')
                tissue_parent = child
                break

        # print('------ search tissue')
        cells_parent = None

        for child in tissue_parent:
            # print('attrib=',child.attrib)
            if (child.attrib['id'] == 'cells'):
                # print('-------- found cells, setting cells_parent')
                cells_parent = child
                break
            numChildren += 1

        num_cells = 0
        #  print('------ search cells')
        for child in cells_parent:
            #    print(child.tag, child.attrib)
            #    print('attrib=',child.attrib)
            for ellip in child:  # two circles in each child: outer + nucleus
                xval = float(ellip.attrib['cx'])

                # map SVG coords into comp domain
                # xval = (xval-self.svg_xmin)/self.svg_xrange * self.x_range + self.xmin
                xval = xval/self.x_range * self.x_range + self.xmin
                print("xrange, xmin= ",self.x_range,self.xmin)

                s = ellip.attrib['fill']
                # print("s=",s)
                # print("type(s)=",type(s))
                if (s[0:3] == "rgb"):  # if an rgb string, e.g. "rgb(175,175,80)" 
                    rgb = list(map(int, s[4:-1].split(",")))  
                    rgb[:] = [x / 255. for x in rgb]
                else:     # otherwise, must be a color name
                    rgb_tuple = mplc.to_rgb(mplc.cnames[s])  # a tuple
                    rgb = [x for x in rgb_tuple]

                # test for bogus x,y locations (rwh TODO: use max of domain?)
                too_large_val = 10000.
                if (np.fabs(xval) > too_large_val):
                    print("bogus xval=", xval)
                    break
                yval = float(ellip.attrib['cy'])
                # yval = (yval - self.svg_xmin)/self.svg_xrange * self.y_range + self.ymin
                yval = yval/self.y_range * self.y_range + self.ymin
                if (np.fabs(yval) > too_large_val):
                    print("bogus xval=", xval)
                    break
# now:  Note: rotate(angle, cx,cy)
#  <ellipse cx="160.117" cy="980.212" rx="50" ry="21.7945" stroke-width="0.5" stroke="black" fill="grey" transform="rotate(81.9098,160.117,980.212)"/>
                rxval = float(ellip.attrib['rx'])
                ryval = float(ellip.attrib['ry'])
                rot_str = ellip.attrib['transform']
                angle_str =  rot_str[rot_str.find('(')+1: rot_str.find(',')]
                print("angle_str= ",angle_str)
                angle = float(angle_str)
                print("angle= ",angle)
                # if (rgb[0] > rgb[1]):
                #     print(num_cells,rgb, rval)
                xlist.append(xval)
                ylist.append(yval)
                rxlist.append(rxval)
                rylist.append(ryval)
                rotlist.append(angle)
                rgb_list.append(rgb)

                # For .svg files with cells that *have* a nucleus, there will be a 2nd
                if (not self.show_nucleus):
                #if (not self.show_nucleus):
                    break

            num_cells += 1

            # if num_cells > 3:   # for debugging
            #   print(fname,':  num_cells= ',num_cells," --- debug exit.")
            #   sys.exit(1)
            #   break

            # print(fname,':  num_cells= ',num_cells)

        xvals = np.array(xlist)
        yvals = np.array(ylist)
        rxvals = np.array(rxlist)
        ryvals = np.array(rylist)
        rotvals = np.array(rotlist)
        rgbs = np.array(rgb_list)
        # print("xvals[0:5]=",xvals[0:5])
        # print("rvals[0:5]=",rvals[0:5])
        # print("rvals.min, max=",rvals.min(),rvals.max())


        self.title_str += " (" + str(num_cells) + " agents)"
        # plt.title(self.title_str, fontsize=self.fontsize)
        self.ax0.set_title(self.title_str, fontsize=self.fontsize)

        # plt.xlim(self.xmin, self.xmax)
        # plt.ylim(self.ymin, self.ymax)
        self.ax0.set_xlim(self.xmin, self.xmax)
        self.ax0.set_ylim(self.ymin, self.ymax)

        #rwh - temp fix - Ah, error only occurs when "edges" is toggled on
        if (self.show_edge):
            try:
                self.ellipses(xvals,yvals, w=rxvals, h=ryvals, a=rotvals, color=rgbs, alpha=self.alpha, edgecolor='black', linewidth=0.5)
            except (ValueError):
                pass
        else:
            self.ellipses(xvals,yvals, w=rxvals, h=ryvals, a=rotvals, color=rgbs, alpha=self.alpha)

    #---------------------------------------------------------------------------
    # assume "frame" is cell frame #, unless Cells is togggled off, then it's the substrate frame #
    # def plot_substrate(self, frame, grid):
    def plot_substrate(self):
        # global cbar

        # print("plot_substrate(): frame*self.substrate_delta_t  = ",frame*self.substrate_delta_t)
        # print("plot_substrate(): frame*self.svg_delta_t  = ",frame*self.svg_delta_t)
        # print("plot_substrate(): fig width: SVG+2D = ",self.figsize_width_svg + self.figsize_width_2Dplot)  # 24
        # print("plot_substrate(): fig width: substrate+2D = ",self.figsize_width_substrate + self.figsize_width_2Dplot)  # 27

        # self.ax0.cla()
        # self.ax0.axis('on')

        self.title_str = ''

        # Recall:
        # self.svg_delta_t = config_tab.svg_interval.value
        # self.substrate_delta_t = config_tab.mcds_interval.value
        # self.modulo = int(self.substrate_delta_t / self.svg_delta_t)
        # self.therapy_activation_time = user_params_tab.therapy_activation_time.value

        # print("plot_substrate(): pre_therapy: max svg, substrate frames = ",max_svg_frame_pre_therapy, max_substrate_frame_pre_therapy)

        # Assume: # .svg files >= # substrate files
#        if (self.cells_toggle.value):

        if self.substrates_toggle.isChecked():
            # plt.clf()
            # self.fig, (self.ax0) = plt.subplots(1, 1, figsize=(self.figsize_width_substrate, self.figsize_height_substrate))
            self.ax0.cla()

            self.substrate_frame = int(self.frame_count / self.substrate_mod)

            fname = "output%08d_microenvironment0.mat" % self.substrate_frame
            xml_fname = "output%08d.xml" % self.substrate_frame
            # fullname = output_dir_str + fname

    #        fullname = fname
            full_fname = os.path.join(self.output_dir, fname)
            print("--- plot_substrate(): full_fname=",full_fname)
            full_xml_fname = os.path.join(self.output_dir, xml_fname)
    #        self.output_dir = '.'

    #        if not os.path.isfile(fullname):
            if not os.path.isfile(full_fname):
                # print("Once output files are generated, click the slider.")  # No:  output00000000_microenvironment0.mat
                print("-- Error: no file ",full_fname)  # No:  output00000000_microenvironment0.mat

                # if self.cells_toggle.isChecked():
                #     self.svg_frame = frame
                #     # print('plot_svg with frame=',self.svg_frame)
                #     self.plot_svg(self.svg_frame)

                # return

            else:

        #        tree = ET.parse(xml_fname)
                tree = ET.parse(full_xml_fname)
                xml_root = tree.getroot()
                mins = round(int(float(xml_root.find(".//current_time").text)))  # TODO: check units = mins
                self.substrate_mins= round(int(float(xml_root.find(".//current_time").text)))  # TODO: check units = mins

                hrs = int(mins/60)
                days = int(hrs/24)
                self.title_str = 'substrate: %dd, %dh, %dm' % (int(days),(hrs%24), mins - (hrs*60))
                # self.title_str = 'substrate: %dm' % (mins )   # rwh

                info_dict = {}
                scipy.io.loadmat(full_fname, info_dict)
                M = info_dict['multiscale_microenvironment']
                f = M[self.field_index, :]   # 4=tumor cells field, 5=blood vessel density, 6=growth substrate

                try:
                    print("numx, numy = ",self.numx, self.numy)
                    xgrid = M[0, :].reshape(self.numy, self.numx)
                    ygrid = M[1, :].reshape(self.numy, self.numx)
                except:
                    print("substrates.py: mismatched mesh size for reshape: numx,numy=",self.numx, self.numy)
                    pass
    #                xgrid = M[0, :].reshape(self.numy, self.numx)
    #                ygrid = M[1, :].reshape(self.numy, self.numx)

                num_contours = 15
                # levels = MaxNLocator(nbins=num_contours).tick_values(self.colormap_min.value, self.colormap_max.value)
                levels = MaxNLocator(nbins=num_contours).tick_values(self.colormap_min, self.colormap_max)
                contour_ok = True
                # if (self.colormap_fixed_toggle.isChecked()):
                if (self.colormap_fixed_toggle):
                    try:
                        # substrate_plot = plt.contourf(xgrid, ygrid, M[self.field_index, :].reshape(self.numy, self.numx), 
                        substrate_plot = self.ax0.contourf(xgrid, ygrid, M[self.field_index, :].reshape(self.numy, self.numx), 
                                levels=levels, extend='both', cmap="viridis", fontsize=self.fontsize)
                    except:
                        contour_ok = False
                        print('got error on contourf 1.')
                else:    
                    try:
                        print("field min,max= ", M[self.field_index, :].min(), M[self.field_index, :].max())
                        print("self.field_index = ", self.field_index)
                        # substrate_plot = plt.contourf(xgrid, ygrid, M[self.field_index, :].reshape(self.numy,self.numx), 
                        substrate_plot = self.ax0.contourf(xgrid, ygrid, M[self.field_index, :].reshape(self.numy,self.numx), 
                                num_contours, cmap = "viridis" ) #  cmap=self.colormap_dd.value)
                    except:
                        contour_ok = False
                        print('\n -->> got error on contourf 2  \n')  # rwh: argh, getting here

                if (contour_ok):
                    self.ax0.set_title(self.title_str, fontsize=self.fontsize)
                    # plt.title(self.title_str, fontsize=5)

                    # self.image = self.ax0.imshow(self.imageInit, interpolation='none')
                    # divider = make_axes_locatable(self.ax0)
                    # cax = divider.new_vertical(size="5%", pad=0.05, pack_start=True)
                    # self.colorbar = self.figure.add_axes(cax)
                    # self.figure.colorbar(self.image, cax=cax, orientation='horizontal')
                    # plt.subplots_adjust(left=0, bottom=0.05, right=1, top=1, wspace=0, hspace=0)

                    # cbar = self.figure.colorbar(substrate_plot, ax=self.ax0)
                    # cbar = self.figure.colorbar(substrate_plot, cax=self.ax0)
                    # cbar = self.figure.colorbar(substrate_plot, cax=self.ax0, orientation='horizontal')
                    if self.cbar == None:  # if we always do this, it creates an additional colorbar!
                        # cbar = plt.colorbar(my_plot)
                        # self.cbar = self.ax0.colorbar(substrate_plot)
                        self.cbar = self.fig.colorbar(substrate_plot)
                        self.cbar.ax.tick_params(labelsize=self.fontsize)
                    else:
                        # self.cbar.ax0.clear()
                        self.cbar.ax.clear()
                        # self.figure.cbar = self.figure.colorbar(substrate_plot, cax=self.ax0)
                        self.cbar = self.fig.colorbar(substrate_plot , cax=self.cbar.ax)

                    # cbar.ax.tick_params(labelsize=self.fontsize)

                # print("l. 805: xmin,xmax = ",self.xmin, self.xmax)
                # print("l. 805: ymin,ymax = ",self.ymin, self.ymax)
                # self.ax0.set_xlim(self.xmin, self.xmax)
                # self.ax0.set_ylim(self.ymin, self.ymax)
                # self.ax0.tick_params(labelsize=4)
                # self.ax0.set_xticks(fontsize= self.fontsize)
                # self.ax0.set_yticks(fontsize= self.fontsize)

        # Now plot the cells (possibly on top of the substrate)
        if self.cells_toggle.isChecked():
            # if not self.substrates_toggle.isChecked():
            #     self.fig, (self.ax0) = plt.subplots(1, 1, figsize=(self.figsize_width_svg, self.figsize_height_svg))

            # self.svg_frame = frame
            # print('plot_svg with frame=',self.svg_frame)
            self.plot_svg()