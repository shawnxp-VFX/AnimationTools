
from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

from PySide2.QtGui import *
from PySide2.QtUiTools import *

import os
import webbrowser
import maya.OpenMayaUI as omui
import maya.cmds as cmds

PC_system = "MACOS"
#PC_system = "windows"
python_version = "3.x"
#python_version = "2.x"




# MAIN DIALOG UI
# RUN DIALOG
# PAGE_A
# BASIC FUNCTIONS
def parent_window():
	#Return the Maya main window widget as a Python object
	main_window_ptr = omui.MQtUtil.mainWindow()
	if python_version == "3.x":
		return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
	elif python_version == "2.x":
		return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


########## ########## ##########  ==============================  MAIN DIALOG UI  ==============================  ########## ########## ##########
class MAIN_DIALOG(QtWidgets.QDialog):
	#Dialog used to demonstrates many of the standard dialogs available in Qt
	FILE_FILTERS = "Maya (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
	selected_filter = "All Files (*.*)"

	if PC_system == "windows":
		parentwindow = parent_window()
	else:
		parentwindow = None

	def __init__(self, parent=parentwindow):
		super(MAIN_DIALOG, self).__init__(parent)
		if PC_system == "windows":
			self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
		else:
			self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.prefs_directory = cmds.internalVar(userPrefDir=True)
		vlayout = QtWidgets.QVBoxLayout(self)

		self.setWindowTitle("Sean_rigbox")
		vlayout.addSpacing(5)
		vlayout.addSpacing(5)
		
		self.add_pages(vlayout)

		self.add_main_page_botton(vlayout)



	# ===== windows always on top fnc ===== #


	def add_pages(self, parentLayout):
		self.tabs = QtWidgets.QTabWidget()

		self.page_1 = PAGE_01("FUNCTION")

		self.page_info = PAGE_INFO("INFO")
		
		self.tabs.addTab(self.page_1, self.page_1.name)
		self.tabs.addTab(self.page_info, self.page_info.name)

		parentLayout.addWidget(self.tabs)

	def add_main_page_botton(self, parentLayout):

		self.button_apply = QtWidgets.QPushButton("Mirror")
		self.button_apply.setFixedHeight(30)
		self.button_close = QtWidgets.QPushButton("Undo")
		self.button_close.setFixedHeight(30)

		self.button_apply.clicked.connect(self.button_apply_Fnc)
		#self.button_close.clicked.connect(lambda:self.close())
		self.button_close.clicked.connect(self.button_undo_Fnc)
		
		hlayout = QtWidgets.QHBoxLayout()
		hlayout.setSpacing(4)

		hlayout.addWidget(self.button_apply)
		hlayout.addWidget(self.button_close)
		parentLayout.addLayout(hlayout)


	
	def button_apply_Fnc(self):

		TX = self.page_1.box_02_button_01_fnc()
		TY = self.page_1.box_02_button_02_fnc()
		TZ = self.page_1.box_02_button_03_fnc()
		RX = self.page_1.box_02_button_04_fnc()
		RY = self.page_1.box_02_button_05_fnc()
		RZ = self.page_1.box_02_button_06_fnc()
		Mirrorbyname = self.page_1.box_02_button_07_fnc()

		cmds.undoInfo( openChunk=True )
		self.page_1.reverse_Ctrls_value1(TX,TY,TZ,RX,RY,RZ,Mirrorbyname)
		cmds.undoInfo( closeChunk=True )

	def button_undo_Fnc(self):
		cmds.undo()


########## ########## ##########  ==============================  PAGE_01  ==============================  ########## ########## ##########

class PAGE_01(QtWidgets.QWidget):
	def __init__(self, panelName):
		QtWidgets.QWidget.__init__(self, None)
		self.name = panelName

		#vlayout = QtWidgets.QVBoxLayout()
		#self.setLayout(vlayout)
		self.create_widgets()
		self.create_layout()
		self.create_connections()

	def create_widgets(self):

		# ===== layout_group_box_01 ===== #
		self.box_01_button_01 = QtWidgets.QPushButton("getExistingDirectory")
		self.box_01_button_02 = QtWidgets.QPushButton("getOpenFileName")
		self.box_01_button_03 = QtWidgets.QPushButton("getOpenFileNames")
		self.box_01_button_04 = QtWidgets.QPushButton("getSaveFileName")

		# ===== layout_group_box_02 ===== #
		self.box_02_button_01 = QtWidgets.QCheckBox("TX")
		self.box_02_button_02 = QtWidgets.QCheckBox("TY")
		self.box_02_button_03 = QtWidgets.QCheckBox("TZ")
		self.box_02_button_04 = QtWidgets.QCheckBox("RX")
		self.box_02_button_05 = QtWidgets.QCheckBox("RY")
		self.box_02_button_06 = QtWidgets.QCheckBox("RZ")
		self.box_02_button_07 = QtWidgets.QCheckBox("Mirror By Name")		
		self.ok_btn = QtWidgets.QPushButton("OK")
		self.cancel_btn = QtWidgets.QPushButton("Cancel")



	def create_layout(self):
		vlayout = QtWidgets.QVBoxLayout(self)

		'''
		# ===== layout_group_box_01 ===== #
		grp = QtWidgets.QGroupBox("QFileDialog")
		grp_layout = QtWidgets.QHBoxLayout()
		grp_layout.addWidget(self.box_01_button_01)
		grp_layout.addWidget(self.box_01_button_02)
		grp_layout.addWidget(self.box_01_button_03)
		grp_layout.addWidget(self.box_01_button_04)
		grp_layout.addStretch()
		grp.setLayout(grp_layout)
		vlayout.addWidget(grp)
		'''

		# ===== layout_group_box_02 ===== #
		grp = QtWidgets.QGroupBox("Reverse Options:")
		grp_layout = QtWidgets.QHBoxLayout()
		grp_layout.addWidget(self.box_02_button_01)
		grp_layout.addWidget(self.box_02_button_02)
		grp_layout.addWidget(self.box_02_button_03)
		grp_layout.addWidget(self.box_02_button_04)
		grp_layout.addWidget(self.box_02_button_05)
		grp_layout.addWidget(self.box_02_button_06)
		grp_layout.addWidget(self.box_02_button_07)
		grp_layout.addStretch()
		grp.setLayout(grp_layout)
		vlayout.addWidget(grp)



		vlayout.addStretch()

	def create_connections(self):

		# ===== layout_group_box_01 ===== #
		#self.box_01_button_01.clicked.connect(self.box_01_button_01_fnc)
		#self.box_01_button_02.clicked.connect(self.box_01_button_01_fnc)
		#self.box_01_button_03.clicked.connect(self.box_01_button_01_fnc)
		#self.box_01_button_04.clicked.connect(self.box_01_button_01_fnc)

		# ===== layout_group_box_02 ===== #
		self.box_02_button_01.toggled.connect(self.box_02_button_01_fnc)
		self.box_02_button_02.toggled.connect(self.box_02_button_02_fnc)
		self.box_02_button_03.toggled.connect(self.box_02_button_03_fnc)
		self.box_02_button_04.toggled.connect(self.box_02_button_04_fnc)
		self.box_02_button_05.toggled.connect(self.box_02_button_05_fnc)
		self.box_02_button_06.toggled.connect(self.box_02_button_06_fnc)
		self.box_02_button_07.toggled.connect(self.box_02_button_07_fnc)

	# ===== layout_group_box_01 ===== #


	# ===== layout_group_box_02 ===== #
	def box_02_button_01_fnc(self):
		checked = self.box_02_button_01.isChecked()
		if checked:
			box_02_button_01_checked = 1
		else:
			box_02_button_01_checked = 0
		return box_02_button_01_checked

	def box_02_button_02_fnc(self):
		checked = self.box_02_button_02.isChecked()
		if checked:
			box_02_button_02_checked = 1
		else:
			box_02_button_02_checked = 0
		return box_02_button_02_checked

	def box_02_button_03_fnc(self):
		checked = self.box_02_button_02.isChecked()
		if checked:
			box_02_button_03_checked = 1
		else:
			box_02_button_03_checked = 0
		return box_02_button_03_checked

	def box_02_button_04_fnc(self):
		checked = self.box_02_button_02.isChecked()
		if checked:
			box_02_button_04_checked = 1
		else:
			box_02_button_04_checked = 0
		return box_02_button_04_checked

	def box_02_button_05_fnc(self):
		checked = self.box_02_button_02.isChecked()
		if checked:
			box_02_button_05_checked = 1
		else:
			box_02_button_05_checked = 0
		return box_02_button_05_checked

	def box_02_button_06_fnc(self):
		checked = self.box_02_button_02.isChecked()
		if checked:
			box_02_button_06_checked = 1
		else:
			box_02_button_06_checked = 0
		return box_02_button_06_checked

	def box_02_button_07_fnc(self):
		checked = self.box_02_button_02.isChecked()
		if checked:
			box_02_button_07_checked = 1
		else:
			box_02_button_07_checked = 0
		return box_02_button_07_checked



	def reverse_Ctrls_value1(self,reverse_TX, reverse_TY, reverse_TZ, reverse_RX, reverse_RY, reverse_RZ, Attrlistbool):
	#Attrlistbool == 1 only copy same name attributes, Attrlistbool == 0 copy all attributes with sequence.

		Ctrl_prefix_list   = ["Lf_","L_","l_","_Lf","_L","_l","Rt_","R_","r_","_Rt","_R","_r"]
		OpCtrl_prefix_list = ["Rt_","R_","r_","_Rt","_R","_r","Lf_","L_","l_","_Lf","_L","_l"]

		CtrlGrp = []
		LRCtrlGrp = []
		OpCtrlGrp = []

		CtrlGrp = cmds.listRelatives(cmds.ls(cmds.listRelatives(cmds.ls(selection=1),shapes=1),type="nurbsCurve"),parent=1)
		for n in range(len(CtrlGrp)):
			prefix_S2 = CtrlGrp[n][:2]
			prefix_S3 = CtrlGrp[n][:3]
			prefix_E2 = CtrlGrp[n][-2:]
			prefix_E3 = CtrlGrp[n][-3:]
			OpCtrl = []

			for i in range(len(Ctrl_prefix_list)):
				if(prefix_S2 == Ctrl_prefix_list[i]) or (prefix_S3 == Ctrl_prefix_list[i]) or (prefix_E2 == Ctrl_prefix_list[i]) or (prefix_E3 == Ctrl_prefix_list[i]):
					OpCtrl = CtrlGrp[n].replace(Ctrl_prefix_list[i], OpCtrl_prefix_list[i])
					if cmds.objExists(OpCtrl) == 1:
						AttrVis = cmds.getAttr(OpCtrl + ".visibility")
						if AttrVis == 0:
							OpCtrl = []
							break
						else:
							LRCtrlGrp.append(CtrlGrp[n])
							OpCtrlGrp.append(OpCtrl)
					else:
						OpCtrl = []
					break

			if OpCtrl == []:
				print("containing incorrect naming ctrls, unsymmetrical or hidden ctrls")
				continue

		for n in range(len(LRCtrlGrp)):
			LRAttrlist = []
			OpAttrlist = []
			LRAttrlist = cmds.listAttr( LRCtrlGrp[n], keyable=1 )
			OpAttrlist = cmds.listAttr( OpCtrlGrp[n], keyable=1 )
			for i in range(len(LRAttrlist)):
				AttrLock = cmds.getAttr(LRCtrlGrp[n] + "." + LRAttrlist[i], lock=1)
				AttrKeyable = cmds.getAttr(LRCtrlGrp[n] + "." + LRAttrlist[i], keyable=1, channelBox=1)
				if (AttrKeyable == 1) and (AttrLock == 0):
					LRAttrValue = cmds.getAttr(LRCtrlGrp[n] + "." + LRAttrlist[i])
					if (reverse_TX == 1) and (LRAttrlist[i] == "translateX"):
						LRAttrValue = LRAttrValue * (-1)
						cmds.setAttr(OpCtrlGrp[n] + "." + OpAttrlist[i], LRAttrValue)
					elif (reverse_TY == 1) and (LRAttrlist[i] == "translateY"):
						LRAttrValue = LRAttrValue * (-1)
						cmds.setAttr(OpCtrlGrp[n] + "." + OpAttrlist[i], LRAttrValue)
					elif (reverse_TZ == 1) and (LRAttrlist[i] == "translateZ"):
						LRAttrValue = LRAttrValue * (-1)
						cmds.setAttr(OpCtrlGrp[n] + "." + OpAttrlist[i], LRAttrValue)
					elif (reverse_RX == 1) and (LRAttrlist[i] == "rotateX"):
						LRAttrValue = LRAttrValue * (-1)
						cmds.setAttr(OpCtrlGrp[n] + "." + OpAttrlist[i], LRAttrValue)
					elif (reverse_RY == 1) and (LRAttrlist[i] == "rotateY"):
						LRAttrValue = LRAttrValue * (-1)
						cmds.setAttr(OpCtrlGrp[n] + "." + OpAttrlist[i], LRAttrValue)
					elif (reverse_RZ == 1) and (LRAttrlist[i] == "rotateZ"):
						LRAttrValue = LRAttrValue * (-1)
						cmds.setAttr(OpCtrlGrp[n] + "." + OpAttrlist[i], LRAttrValue)
					elif LRAttrlist[i] == "visibility":
						pass
					else:
						if (Attrlistbool == 1) and (LRAttrlist[i] == OpAttrlist[i]):
							cmds.setAttr(OpCtrlGrp[n] + "." + LRAttrlist[i], LRAttrValue)
						elif Attrlistbool == 0:
							cmds.setAttr(OpCtrlGrp[n] + "." + OpAttrlist[i], LRAttrValue)
		cmds.select(OpCtrlGrp)

	#reverse_Ctrls_value1(1,1,1,1,1,1,1)




########## ########## ##########  ==============================  PAGE_INFO  ==============================  ########## ########## ##########
class PAGE_INFO(QtWidgets.QWidget):
	def __init__(self, panelName):
		QtWidgets.QWidget.__init__(self, None)
		self.name = panelName

		formlayout = QtWidgets.QFormLayout()
		self.label_info = QtWidgets.QLabel("by shawnxp")
		formlayout.addRow("AnimationToolv1.0 Dec_15_2021",self.label_info)
		main_layout = QtWidgets.QVBoxLayout(self)
		main_layout.addLayout(formlayout)

		main_layout.addStretch()
		self.addButtonPanel(main_layout)

	#--------------------------------------------------------------
	def addButtonPanel(self, parentLayout):
		self.button_demo01 = QtWidgets.QPushButton("More Plugins")
		self.button_demo01.setFixedHeight(30)
		self.button_demo01.clicked.connect(self.buttonAction_link01)

		hlayout = QtWidgets.QHBoxLayout()
		hlayout.addWidget(self.button_demo01)
		parentLayout.addLayout(hlayout)

	#--------------------------------------------------------------
	def buttonAction_link01(self):
		webbrowser.open("https://github.com/shawnxp-VFX")



########## ########## ##########  ==============================  BASIC FUNCTIONS  ==============================  ########## ########## ##########




########## ########## ##########  ==============================  RUN DIALOG  ==============================  ########## ########## ##########

if __name__ == "__main__":
	#app = QApplication(sys.argv)

	try:
		RUN_DIALOG.close() # pylint: disable=E0601
		RUN_DIALOG.deleteLater()
	except:
		pass

	cmds.undoInfo( state=True, infinity=True )
	RUN_DIALOG = MAIN_DIALOG()
	RUN_DIALOG.show()

	#sys.exit(app.exec_())


