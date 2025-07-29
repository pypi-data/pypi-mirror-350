# -*- coding: utf-8 -*-
# FlashGBX
# Author: Lesserkuma (github.com/lesserkuma)

import functools, os, json, platform, shutil
from PIL.ImageQt import ImageQt
from PIL import Image, ImageDraw
from .pyside import QtCore, QtWidgets, QtGui, QDesktopWidget
from .PocketCamera import PocketCamera
from .UserInputDialog import UserInputDialog

class PocketCameraWindow(QtWidgets.QDialog):
	CUR_PIC = None
	CUR_THUMBS = None
	CUR_INDEX = 0
	CUR_BICUBIC = False
	CUR_FILE = ""
	CUR_EXPORT_PATH = "."
	CUR_PC = None
	CUR_PALETTE = 3
	APP_PATH = "."
	CONFIG_PATH = "."
	APP = None
	FORCE_EXIT = False
	PALETTES = [
		[ 255, 255, 255,   176, 176, 176,   104, 104, 104,   0, 0, 0 ], # Grayscale
		[ 208, 217, 60,   120, 164, 106,   84, 88, 84,   36, 70, 36 ], # Game Boy
		[ 255, 255, 255,   181, 179, 189,   84, 83, 103,   9, 7, 19 ], # Super Game Boy
		[ 240, 240, 240,   218, 196, 106,   112, 88, 52,   30, 30, 30 ], # Game Boy Color (JPN)
		[ 240, 240, 240,   220, 160, 160,   136, 78, 78,   30, 30, 30 ], # Game Boy Color (USA Gold)
		[ 240, 240, 240,   134, 200, 100,   58, 96, 132,   30, 30, 30 ], # Game Boy Color (USA/EUR)
	]
	
	def __init__(self, app, file=None, icon=None, config_path=".", app_path="."):
		QtWidgets.QDialog.__init__(self)
		self.setAcceptDrops(True)
		if icon is not None: self.setWindowIcon(QtGui.QIcon(icon))

		self.FORCE_EXIT = False
		self.CUR_FILE = file
		self.CONFIG_PATH = config_path
		self.APP_PATH = app_path
		self.setWindowTitle("FlashGBX – GB Camera Album Viewer")
		self.setWindowFlags((self.windowFlags() | QtCore.Qt.MSWindowsFixedSizeDialogHint) & ~QtCore.Qt.WindowContextHelpButtonHint)
		
		self.layout = QtWidgets.QGridLayout()
		self.layout.setContentsMargins(-1, 8, -1, 8)
		self.layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
		self.layout_options1 = QtWidgets.QVBoxLayout()
		self.layout_options2 = QtWidgets.QVBoxLayout()
		self.layout_options3 = QtWidgets.QVBoxLayout()
		self.layout_photos = QtWidgets.QHBoxLayout()
		
		# Options
		self.grpOptions = QtWidgets.QGroupBox("Options")
		grpOptionsLayout = QtWidgets.QVBoxLayout()
		grpOptionsLayout.setContentsMargins(-1, 3, -1, -1)
		self.rowOptions1 = QtWidgets.QHBoxLayout()
		self.lblColor = QtWidgets.QLabel("Color Palette:")
		self.cmbColor = QtWidgets.QComboBox()
		self.cmbColor.setStyleSheet("combobox-popup: 0;")
		self.cmbColor.view().setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.cmbColor.addItems(["Grayscale", "Original Game Boy", "Super Game Boy", "Game Boy Color (Pocket Camera)", "Game Boy Color (Game Boy Camera Gold)", "Game Boy Color (Game Boy Camera)"])
		self.cmbColor.currentIndexChanged.connect(self.SetColors)
		self.cmbColor.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
		self.cmbColor.setCurrentIndex(-1)
		self.rowOptions1.addWidget(self.lblColor)
		self.rowOptions1.addWidget(self.cmbColor)
		self.rowOptions1.addStretch(1)
		
		self.lblZoom = QtWidgets.QLabel("Saved Picture Zoom:")
		self.spnZoom = QtWidgets.QSpinBox()
		self.spnZoom.setRange(1, 10)
		self.spnZoom.setSuffix("×")
		self.rowOptions1.addWidget(self.lblZoom)
		self.rowOptions1.addWidget(self.spnZoom)
		self.rowOptions1.addStretch(1)
		
		self.chkFrame = QtWidgets.QCheckBox("Save With &Frame")
		self.rowOptions1.addWidget(self.chkFrame)
		
		grpOptionsLayout.addLayout(self.rowOptions1)
		self.grpOptions.setLayout(grpOptionsLayout)

		self.layout_options1.addWidget(self.grpOptions)

		rowActionsGeneral1 = QtWidgets.QHBoxLayout()
		self.btnOpenSRAM = QtWidgets.QPushButton("&Open Save Data File")
		self.btnOpenSRAM.setStyleSheet("padding: 5px 10px;")
		self.btnOpenSRAM.clicked.connect(self.btnOpenSRAM_Clicked)
		self.btnClose = QtWidgets.QPushButton("&Close")
		self.btnClose.setStyleSheet("padding: 5px 15px;")
		self.btnClose.clicked.connect(self.btnClose_Clicked)
		rowActionsGeneral1.addWidget(self.btnOpenSRAM)
		rowActionsGeneral1.addStretch()
		rowActionsGeneral1.addWidget(self.btnClose)
		self.layout_options3.addLayout(rowActionsGeneral1)
		
		# Photo Viewer
		self.grpPhotoView = QtWidgets.QGroupBox("Preview")
		self.grpPhotoViewLayout = QtWidgets.QVBoxLayout()
		self.grpPhotoViewLayout.setContentsMargins(-1, 3, -1, -1)
		self.lblPhotoViewer = QtWidgets.QLabel(self)
		self.lblPhotoViewer.setMinimumSize(256, 223)
		self.lblPhotoViewer.setMaximumSize(256, 223)
		self.lblPhotoViewer.setStyleSheet("border-top: 1px solid #adadad; border-left: 1px solid #adadad; border-bottom: 1px solid #ffffff; border-right: 1px solid #ffffff;")
		self.lblPhotoViewer.mousePressEvent = self.lblPhotoViewer_Clicked
		self.grpPhotoViewLayout.addWidget(self.lblPhotoViewer)
		
		# Actions below Viewer
		rowActionsGeneral2 = QtWidgets.QHBoxLayout()
		self.btnSavePhoto = QtWidgets.QPushButton("&Save This Picture")
		self.btnSavePhoto.setStyleSheet("padding: 5px 10px;")
		self.btnSavePhoto.clicked.connect(self.btnSavePhoto_Clicked)
		rowActionsGeneral2.addWidget(self.btnSavePhoto)
		self.btnSaveAll = QtWidgets.QPushButton("Save &All Pictures")
		self.btnSaveAll.setStyleSheet("padding: 5px 10px;")
		self.btnSaveAll.clicked.connect(self.btnSaveAll_Clicked)
		rowActionsGeneral2.addWidget(self.btnSaveAll)
		self.grpPhotoViewLayout.addLayout(rowActionsGeneral2)
		
		self.grpPhotoView.setLayout(self.grpPhotoViewLayout)

		# Photo List
		self.grpPhotoThumbs = QtWidgets.QGroupBox("Photo Album")
		self.grpPhotoThumbsLayout = QtWidgets.QVBoxLayout()
		self.grpPhotoThumbsLayout.setSpacing(2)
		self.grpPhotoThumbsLayout.setContentsMargins(-1, 3, -1, -1)
		self.lblPhoto = []
		rowsPhotos = []
		for row in range(0, 5):
			rowsPhotos.append(QtWidgets.QHBoxLayout())
			rowsPhotos[row].setSpacing(2)
			for _ in range(0, 6):
				self.lblPhoto.append(QtWidgets.QLabel(self))
				self.lblPhoto[len(self.lblPhoto)-1].setMinimumSize(49, 43)
				self.lblPhoto[len(self.lblPhoto)-1].setMaximumSize(49, 43)
				self.lblPhoto[len(self.lblPhoto)-1].mousePressEvent = functools.partial(self.lblPhoto_Clicked, index=len(self.lblPhoto)-1)
				self.lblPhoto[len(self.lblPhoto)-1].setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
				self.lblPhoto[len(self.lblPhoto)-1].setAlignment(QtCore.Qt.AlignCenter)
				self.lblPhoto[len(self.lblPhoto)-1].setStyleSheet("border-top: 1px solid #adadad; border-left: 1px solid #adadad; border-bottom: 1px solid #fefefe; border-right: 1px solid #fefefe;")
				rowsPhotos[row].addWidget(self.lblPhoto[len(self.lblPhoto)-1])
			self.grpPhotoThumbsLayout.addLayout(rowsPhotos[row])
		
		rowActionsGeneral3 = QtWidgets.QHBoxLayout()
		self.btnShowGameFace = QtWidgets.QPushButton("&Game Face")
		self.btnShowGameFace.setStyleSheet("padding: 5px 10px;")
		self.btnShowGameFace.clicked.connect(self.btnShowGameFace_Clicked)
		rowActionsGeneral3.addWidget(self.btnShowGameFace)
		self.btnShowLastSeen = QtWidgets.QPushButton("&Last Seen Image")
		self.btnShowLastSeen.setStyleSheet("padding: 5px 10px;")
		self.btnShowLastSeen.clicked.connect(self.btnShowLastSeen_Clicked)
		rowActionsGeneral3.addWidget(self.btnShowLastSeen)
		self.grpPhotoThumbsLayout.addStretch()
		self.grpPhotoThumbsLayout.addLayout(rowActionsGeneral3)

		self.grpPhotoThumbsLayout.setAlignment(QtCore.Qt.AlignTop)
		self.grpPhotoThumbs.setLayout(self.grpPhotoThumbsLayout)
		
		self.layout_photos.addWidget(self.grpPhotoThumbs)
		self.layout_photos.addWidget(self.grpPhotoView)
		
		self.layout.addLayout(self.layout_options1, 0, 0)
		self.layout.addLayout(self.layout_options2, 1, 0)
		self.layout.addLayout(self.layout_photos, 2, 0)
		self.layout.addLayout(self.layout_options3, 3, 0)
		self.setLayout(self.layout)
		
		self.APP = app
		
		try:
			self.spnZoom.setValue(int(self.APP.SETTINGS.value("PocketCameraZoom")))
		except:
			self.spnZoom.setValue(2)
		self.chkFrame.setChecked(self.APP.SETTINGS.value("PocketCameraFrame", default="disabled") == "enabled")

		palette = self.APP.SETTINGS.value("PocketCameraPalette")
		try:
			palette = json.loads(palette)
		except:
			palette = None
			self.cmbColor.setCurrentIndex(3)
		palette_found = False
		if palette is not None:
			for i in range(0, len(self.PALETTES)):
				if palette == self.PALETTES[i]:
					self.cmbColor.setCurrentIndex(i)
					self.CUR_PALETTE = i
					palette_found = True
		if not palette_found:
			self.PALETTES.append(palette)
			self.CUR_PALETTE = len(self.PALETTES) - 1
		
		if self.CUR_FILE is not None:
			if self.OpenFile(self.CUR_FILE) is False:
				self.FORCE_EXIT = True
				return

		self.CUR_EXPORT_PATH = self.APP.SETTINGS.value("LastDirPocketCamera")
		if self.CUR_EXPORT_PATH is None:
			self.CUR_EXPORT_PATH = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation)
		
		self.SetColors()
		
		self.btnSaveAll.setDefault(True)
		self.btnSaveAll.setAutoDefault(True)
		self.btnSaveAll.setFocus()
	
	def run(self):
		if self.FORCE_EXIT:
			self.reject()
			return
		self.layout.update()
		self.layout.activate()
		screenGeometry = QDesktopWidget().screenGeometry(self)
		x = (screenGeometry.width() - self.width()) / 2
		y = (screenGeometry.height() - self.height()) / 2
		self.move(x, y)
		self.show()
	
	def SetColors(self):
		if self.CUR_PC is None: return
		self.CUR_PALETTE = self.cmbColor.currentIndex()
		self.CUR_PC.SetPalette(self.PALETTES[self.CUR_PALETTE])
		self.BuildPhotoList()
		self.UpdateViewer(self.CUR_INDEX)
	
	def OpenFile(self, file):
		if isinstance(file, bytearray) and len(file) == 0x100000 or isinstance(file, str) and os.path.getsize(file) == 0x100000:
			dlg_args = {
				"title":"Photo!",
				"intro":"A Photo! save file was detected.\n\nPlease select the roll of pictures that you would like to load.",
				"params": [
					[ "index", "cmb", "Roll:", [ "Current Save Data" ] + [ "Flash Directory Slot {:d}".format(l) for l in range(1, 8) ], 0 ],
				]
			}
			dlg = UserInputDialog(self, icon=self.windowIcon(), args=dlg_args)
			if dlg.exec_() == 1:
				result = dlg.GetResult()
				index = result["index"].currentIndex()
				if isinstance(file, str):
					with open(file, "rb") as f:
						file = bytearray(f.read())
				file = file[0x20000 * index:][:0x20000]
			else:
				self.CUR_PC = None
				return False

		try:
			self.CUR_PC = PocketCamera()
			if self.CUR_PC.LoadFile(file) == False:
				self.CUR_PC = None
				QtWidgets.QMessageBox.critical(self, "FlashGBX", "The save data file couldn’t be loaded.", QtWidgets.QMessageBox.Ok)
				return False
			self.CUR_FILE = file
			if self.CUR_EXPORT_PATH == "":
				self.CUR_EXPORT_PATH = os.path.dirname(self.CUR_FILE)
			self.UpdateViewer(0)
			self.SetColors()
			return True
		except:
			self.CUR_PC = None
			QtWidgets.QMessageBox.critical(self, "FlashGBX", "An error occured while trying to load the save data file.", QtWidgets.QMessageBox.Ok)
			return False
	
	def lblPhoto_Clicked(self, event, index):
		if event.button() == QtCore.Qt.LeftButton:
			self.CUR_INDEX = index
			self.UpdateViewer(self.CUR_INDEX)
	
	def lblPhotoViewer_Clicked(self, event):
		if event.button() == QtCore.Qt.LeftButton:
			self.CUR_BICUBIC = not self.CUR_BICUBIC
			self.UpdateViewer(self.CUR_INDEX)
	
	def btnOpenSRAM_Clicked(self):
		last_dir = self.APP.SETTINGS.value("LastDirSaveDataDMG")
		if last_dir is None: last_dir = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation)
		path = QtWidgets.QFileDialog.getOpenFileName(self, "Open GB Camera Save Data File", last_dir, "Save Data File (*.sav);;All Files (*.*)")[0]
		if (path == ""): return
		if self.OpenFile(path) is True:
			self.APP.SETTINGS.setValue("LastDirSaveDataDMG", os.path.dirname(path))
	
	def btnShowGameFace_Clicked(self, event):
		self.UpdateViewer(30)
		self.CUR_INDEX = 30
	
	def btnShowLastSeen_Clicked(self, event):
		self.UpdateViewer(31)
		self.CUR_INDEX = 31
	
	def btnSaveAll_Clicked(self, event):
		if self.CUR_PC is None: return
		path = self.CUR_EXPORT_PATH + "/IMG_PC.png"
		path = QtWidgets.QFileDialog.getSaveFileName(self, "Export all pictures", path, "PNG files (*.png);;BMP files (*.bmp);;GIF files (*.gif);;JPEG files (*.jpg);;All files (*.*)")[0]
		if path == "": return
		self.CUR_EXPORT_PATH = os.path.dirname(path)
		
		for i in range(0, 32):
			file = os.path.splitext(path)[0] + "{:02d}".format(i) + os.path.splitext(path)[1]
			if os.path.exists(file):
				answer = QtWidgets.QMessageBox.warning(self, "FlashGBX", "There are already pictures that use the same file names. If you continue, these files will be overwritten.", QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
				if answer == QtWidgets.QMessageBox.Ok:
					break
				elif answer == QtWidgets.QMessageBox.Cancel:
					return

		for i in range(0, 32):
			file = os.path.splitext(path)[0] + "{:02d}".format(i+1) + os.path.splitext(path)[1]
			self.SavePicture(i, path=file)
	
	def btnSavePhoto_Clicked(self, event):
		if self.CUR_PC is None: return
		self.SavePicture(self.CUR_INDEX)
	
	def btnClose_Clicked(self, event):
		self.FORCE_EXIT = True
		self.reject()
	
	def hideEvent(self, event):
		self.APP.SETTINGS.setValue("PocketCameraPalette", json.dumps(self.PALETTES[self.cmbColor.currentIndex()]))
		self.APP.SETTINGS.setValue("PocketCameraZoom", str(self.spnZoom.value()))
		self.APP.SETTINGS.setValue("PocketCameraFrame", str(self.chkFrame.isChecked()).lower().replace("true", "enabled").replace("false", "disabled"))
		self.APP.SETTINGS.setValue("LastDirPocketCamera", self.CUR_EXPORT_PATH)
		self.APP.activateWindow()
	
	def BuildPhotoList(self):
		cam = self.CUR_PC
		self.CUR_THUMBS = [None] * 30
		for i in range(0, 30):
			pic = cam.GetPicture(i).convert("RGBA")
			self.lblPhoto[i].setToolTip("")
			if cam.IsEmpty(i):
				pass
			elif cam.IsDeleted(i):
				draw_bg = Image.new("RGBA", pic.size)
				draw = ImageDraw.Draw(draw_bg)
				draw.line([0, 0, 128, 112], fill=(255, 0, 0, 192), width=8)
				draw.line([0, 112, 128, 0], fill=(255, 0, 0, 192), width=8)
				pic.paste(draw_bg, mask=draw_bg)
				self.lblPhoto[i].setToolTip("This picture was marked as “deleted” and may be overwritten when you take new pictures.")
			self.CUR_THUMBS[i] = ImageQt(pic.resize((47, 41), Image.Resampling.HAMMING))
			qpixmap = QtGui.QPixmap.fromImage(self.CUR_THUMBS[i])
			self.lblPhoto[i].setPixmap(qpixmap)
	
	def UpdateViewer(self, index):
		resampler = Image.Resampling.NEAREST
		if self.CUR_BICUBIC: resampler = Image.Resampling.BICUBIC
		cam = self.CUR_PC
		if cam is None: return
		
		for i in range(0, 30):
			self.lblPhoto[i].setStyleSheet("border-top: 1px solid #adadad; border-left: 1px solid #adadad; border-bottom: 1px solid #ffffff; border-right: 1px solid #ffffff;")
		
		if index >= 30:
			self.CUR_PIC = ImageQt(cam.GetPicture(index).convert("RGBA").resize((256, 224), Image.Resampling.BICUBIC if index == 31 else resampler))
		else:
			self.CUR_PIC = ImageQt(cam.GetPicture(index).convert("RGBA").resize((256, 224), resampler))
			self.lblPhoto[index].setStyleSheet("border: 3px solid green; padding: 1px;")
		
		qpixmap = QtGui.QPixmap.fromImage(self.CUR_PIC)
		self.lblPhotoViewer.setPixmap(qpixmap)
	
	def SavePicture(self, index, path=""):
		if path == "":
			path = self.CUR_EXPORT_PATH + "/IMG_PC{:02d}.png".format(index+1)
			path = QtWidgets.QFileDialog.getSaveFileName(self, "Save Photo", path, "PNG files (*.png);;BMP files (*.bmp);;GIF files (*.gif);;JPEG files (*.jpg);;All files (*.*)")[0]
			if path != "": self.CUR_EXPORT_PATH = os.path.dirname(path)
		if path == "": return
		
		cam = self.CUR_PC

		frame = False
		if self.chkFrame.isChecked():
			frame = True
			own_frame = self.CONFIG_PATH + "/pc_frame.png"
			if not os.path.exists(own_frame):
				shutil.copy(self.APP_PATH + "/res/pc_frame.png", own_frame)
			with open(own_frame, "rb") as f: frame = f.read()
		
		if index == 31: frame = False # last seen image
		cam.ExportPicture(index=index, path=path, scale=self.spnZoom.value(), frame=frame)
	
	def dragEnterEvent(self, e):
		if self._dragEventHover(e):
			e.accept()
		else:
			e.ignore()

	def dragMoveEvent(self, e):
		if self._dragEventHover(e):
			e.accept()
		else:
			e.ignore()
	
	def _dragEventHover(self, e):
		if e.mimeData().hasUrls:
			for url in e.mimeData().urls():
				if platform.system() == 'Darwin':
					# pylint: disable=undefined-variable
					fn = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())
				else:
					fn = str(url.toLocalFile())
				
				fn_split = os.path.splitext(os.path.abspath(fn))
				if fn_split[1] == ".sav":
					return True
		return False
	
	def dropEvent(self, e):
		if e.mimeData().hasUrls:
			e.setDropAction(QtCore.Qt.CopyAction)
			e.accept()
			for url in e.mimeData().urls():
				if platform.system() == 'Darwin':
					# pylint: disable=undefined-variable
					fn = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())
				else:
					fn = str(url.toLocalFile())
				
				fn_split = os.path.splitext(os.path.abspath(fn))
				if fn_split[1] == ".sav":
					self.OpenFile(fn)
		else:
			e.ignore()
