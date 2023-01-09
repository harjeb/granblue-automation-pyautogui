# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ga.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from check_combo import CheckableComboBox
from PyQt5.QtWidgets import QLineEdit,QDesktopWidget
from PyQt5.QtCore import pyqtSignal,QEvent

# Add clicked function for QLineEdit
# https://stackoverflow.com/questions/35047349/pyqt-5-how-to-make-qlineedit-clickable
class cQLineEdit(QLineEdit):
    clicked= pyqtSignal()
    def __init__(self,widget):
        super().__init__(widget)
    def mousePressEvent(self,QMouseEvent):
        self.clicked.emit()


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(924, 479)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.TabWidget = QtWidgets.QTabWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TabWidget.sizePolicy().hasHeightForWidth())
        self.TabWidget.setSizePolicy(sizePolicy)
        self.TabWidget.setMaximumSize(QtCore.QSize(10000, 10000))
        self.TabWidget.setObjectName("TabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.comboBox = QtWidgets.QComboBox(self.tab)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.comboBox_2 = QtWidgets.QComboBox(self.tab)
        self.comboBox_2.setObjectName("comboBox_2")
        self.horizontalLayout_2.addWidget(self.comboBox_2)

        self.comboBox_3 = QtWidgets.QComboBox(self.tab)
        self.comboBox_3.setObjectName("comboBox_3")
        self.horizontalLayout_2.addWidget(self.comboBox_3)
        self.comboBox_6 = QtWidgets.QComboBox(self.tab)
        self.comboBox_6.setObjectName("comboBox_6")
        self.horizontalLayout_2.addWidget(self.comboBox_6)

        self.lineEdit_3 = cQLineEdit(self.tab)
        self.lineEdit_3.setObjectName("main_script")
        self.horizontalLayout_2.addWidget(self.lineEdit_3)
        self.checkBox_12 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_12.setObjectName("checkBox_12")
        self.horizontalLayout_2.addWidget(self.checkBox_12)
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(self.tab)
        self.spinBox.setMaximumSize(QtCore.QSize(60, 16777215))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(999)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_2.addWidget(self.spinBox)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.spinBox_3 = QtWidgets.QSpinBox(self.tab)
        self.spinBox_3.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBox_3.setMinimum(1)
        self.spinBox_3.setMaximum(14)
        self.spinBox_3.setObjectName("spinBox_3")
        self.horizontalLayout_4.addWidget(self.spinBox_3)
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.spinBox_2 = QtWidgets.QSpinBox(self.tab)
        self.spinBox_2.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(6)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout_4.addWidget(self.spinBox_2)
        self.comboBox_4 = CheckableComboBox(self.tab)
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.setMinimumWidth(90)
        self.horizontalLayout_4.addWidget(self.comboBox_4)
        self.checkBox_13 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_13.setObjectName("checkBox_13")
        self.horizontalLayout_4.addWidget(self.checkBox_13)
        self.checkBox_14 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_14.setObjectName("checkBox_14")
        self.horizontalLayout_4.addWidget(self.checkBox_14)
        self.lineEdit_4 = cQLineEdit(self.tab)
        self.lineEdit_4.setObjectName("nightmare_script")
        self.horizontalLayout_4.addWidget(self.lineEdit_4)
        self.label_19 = QtWidgets.QLabel(self.tab)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_4.addWidget(self.label_19)
        self.spinBox_9 = QtWidgets.QSpinBox(self.tab)
        self.spinBox_9.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBox_9.setMinimum(1)
        self.spinBox_9.setMaximum(14)
        self.spinBox_9.setObjectName("spinBox_9")
        self.horizontalLayout_4.addWidget(self.spinBox_9)
        self.label_20 = QtWidgets.QLabel(self.tab)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_4.addWidget(self.label_20)
        self.spinBox_10 = QtWidgets.QSpinBox(self.tab)
        self.spinBox_10.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBox_10.setMinimum(1)
        self.spinBox_10.setMaximum(6)
        self.spinBox_10.setObjectName("spinBox_10")
        self.horizontalLayout_4.addWidget(self.spinBox_10)
        self.comboBox_5 = CheckableComboBox(self.tab)
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.setMinimumWidth(90)
        self.horizontalLayout_4.addWidget(self.comboBox_5)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setMinimumSize(QtCore.QSize(80, 0))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.textBrowser = QtWidgets.QPlainTextEdit(self.tab)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.TabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 912, 421))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.checkBox_2 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_2.setMaximumSize(QtCore.QSize(10000, 10000))
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout_6.addWidget(self.checkBox_2)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_6.addWidget(self.label_7)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget)
        self.doubleSpinBox.setMaximumSize(QtCore.QSize(50, 16777215))
        self.doubleSpinBox.setDecimals(1)
        self.doubleSpinBox.setSingleStep(0.1)
        self.doubleSpinBox.setProperty("value", 0.2)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.horizontalLayout_6.addWidget(self.doubleSpinBox)
        self.checkBox_3 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_3.setObjectName("checkBox_3")
        self.horizontalLayout_6.addWidget(self.checkBox_3)
        self.spinBox_4 = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_4.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBox_4.setProperty("value", 15)
        self.spinBox_4.setObjectName("spinBox_4")
        self.horizontalLayout_6.addWidget(self.spinBox_4)
        self.checkBox_4 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_4.setObjectName("checkBox_4")
        self.horizontalLayout_6.addWidget(self.checkBox_4)
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_6.addWidget(self.label_8)
        self.spinBox_6 = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_6.setMaximumSize(QtCore.QSize(50, 10000))
        self.spinBox_6.setObjectName("spinBox_6")
        self.horizontalLayout_6.addWidget(self.spinBox_6)
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_6.addWidget(self.label_9)
        self.spinBox_7 = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_7.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBox_7.setObjectName("spinBox_7")
        self.horizontalLayout_6.addWidget(self.spinBox_7)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.checkBox_5 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_5.setObjectName("checkBox_5")
        self.horizontalLayout_7.addWidget(self.checkBox_5)
        self.label_10 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_7.addWidget(self.label_10)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem4)
        self.label_11 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_11.setMaximumSize(QtCore.QSize(120, 16777215))
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_7.addWidget(self.label_11)
        self.spinBox_8 = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_8.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBox_8.setObjectName("spinBox_8")
        self.horizontalLayout_7.addWidget(self.spinBox_8)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.checkBox_6 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_6.setObjectName("checkBox_6")
        self.horizontalLayout_8.addWidget(self.checkBox_6)
        self.label_12 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_8.addWidget(self.label_12)
        self.checkBox_7 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_7.setObjectName("checkBox_7")
        self.horizontalLayout_8.addWidget(self.checkBox_7)
        self.label_13 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_8.addWidget(self.label_13)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem6)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.checkBox_8 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_8.setObjectName("checkBox_8")
        self.horizontalLayout_9.addWidget(self.checkBox_8)
        self.label_14 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_9.addWidget(self.label_14)
        self.checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_9.addWidget(self.checkBox)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_9.addWidget(self.label_4)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem7)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.checkBox_9 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_9.setObjectName("checkBox_9")
        self.horizontalLayout_10.addWidget(self.checkBox_9)
        self.label_15 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_10.addWidget(self.label_15)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem8)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.checkBox_10 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_10.setObjectName("checkBox_10")
        self.horizontalLayout_11.addWidget(self.checkBox_10)
        self.label_16 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_11.addWidget(self.label_16)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem9)
        self.verticalLayout_3.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.checkBox_11 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_11.setObjectName("checkBox_11")
        self.horizontalLayout_12.addWidget(self.checkBox_11)
        self.label_17 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_12.addWidget(self.label_17)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem10)
        self.verticalLayout_3.addLayout(self.horizontalLayout_12)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox_15 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_15.setObjectName("checkBox_15")
        self.horizontalLayout.addWidget(self.checkBox_15)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_5.setMaximumSize(QtCore.QSize(120, 16777215))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.horizontalLayout.addWidget(self.lineEdit_5)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem11)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_18 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_13.addWidget(self.label_18)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem12)
        self.verticalLayout_3.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.checkBox_17 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_17.setObjectName("checkBox_17")
        self.horizontalLayout_14.addWidget(self.checkBox_17)
        self.checkBox_18 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_18.setToolTip("")
        self.checkBox_18.setObjectName("checkBox_18")
        self.horizontalLayout_14.addWidget(self.checkBox_18)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_14.addWidget(self.label_5)
        self.spinBox_5 = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_5.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBox_5.setObjectName("spinBox_5")
        self.horizontalLayout_14.addWidget(self.spinBox_5)
        self.lineEdit_6 = cQLineEdit(self.verticalLayoutWidget)
        self.lineEdit_6.setMaximumSize(QtCore.QSize(120, 16777215))
        self.lineEdit_6.setObjectName("defender_script")
        self.horizontalLayout_14.addWidget(self.lineEdit_6)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_14.addWidget(self.label_6)
        self.spinBox_11 = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_11.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBox_11.setObjectName("spinBox_11")
        self.spinBox_11.setMinimum(1)
        self.spinBox_11.setMaximum(7)
        self.horizontalLayout_14.addWidget(self.spinBox_11)
        self.label_21 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_14.addWidget(self.label_21)
        self.spinBox_12 = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_12.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBox_12.setObjectName("spinBox_12")
        self.spinBox_12.setMinimum(1)
        self.spinBox_12.setMaximum(6)
        self.horizontalLayout_14.addWidget(self.spinBox_12)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem13)
        self.verticalLayout_3.addLayout(self.horizontalLayout_14)
        spacerItem14 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem14)

        self.TabWidget.addTab(self.tab_2, "")
        self.horizontalLayout_5.addWidget(self.TabWidget)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(Form)
        self.TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "钢铁侠再再生"))
        self.lineEdit_3.setPlaceholderText(_translate("Form", "选择战斗脚本"))
        self.checkBox_12.setText(_translate("Form", "Raid默认召唤石"))
        self.checkBox_12.setToolTip("舔表时默认选第一个召唤石（加快速度），会覆盖召唤石选择的配置")
        self.label.setText(_translate("Form", "次数"))
        self.pushButton_2.setText(_translate("Form", "添加到队列"))
        self.label_2.setText(_translate("Form", "选择编成"))
        self.label_3.setText(_translate("Form", "选择队伍"))
        self.checkBox_13.setText(_translate("Form", "Debug模式"))
        self.checkBox_13.setToolTip("Enables debugging messages to show up in the log")
        self.checkBox_14.setText(_translate("Form", "Nightmare"))
        self.lineEdit_4.setPlaceholderText(_translate("Form", "战斗脚本"))
        self.label_19.setText(_translate("Form", "编成"))
        self.label_20.setText(_translate("Form", "队伍"))
        self.lineEdit.setPlaceholderText(_translate("Form", "任务队列"))
        self.pushButton.setText(_translate("Form", "开始"))
        self.textBrowser.moveCursor(QtGui.QTextCursor.End)
        initialMessage = """****************************************\nWelcome to Granblue Automation EXReborn!\n****************************************\nInstructions\n----------------\n
    1. Have your game window and the Bottom Menu visible. Set the game window size set to the second "notch".
    2. Go to the Settings Page of the bot and fill out the sections until the status at the top says "Ready".
    3. You can now head back to the Home Page of the bot and click START.
    \nWarning: Do not refresh/F5 the program's "page" while the bot process is running. Otherwise in order to stop it, you will need to kill it by completely exiting the program.\n****************************************\n"""
        self.textBrowser.appendPlainText(_translate("Form", initialMessage))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.tab), _translate("Form", "主页"))
        self.checkBox_2.setText(_translate("Form", "模拟人类鼠标移动"))
        self.checkBox_2.setToolTip("Enable this option to have slow but human-like mouse movement. Disable this for fast but bot-like mouse movement. Note that enabling this will disable the Mouse Speed setting.")
        self.label_7.setText(_translate("Form", "鼠标移动速度(秒)"))
        self.label_7.setToolTip("Set how fast a mouse operation finishes.")
        self.checkBox_3.setText(_translate("Form", "开启运行间隔"))
        self.checkBox_3.setToolTip("Enable delay in seconds between runs to serve as a resting period.")
        self.checkBox_4.setText(_translate("Form", "开启随机运行间隔"))
        self.checkBox_4.setToolTip("Enable randomized delay in seconds between runs to serve as a resting period.")
        self.label_8.setText(_translate("Form", "最短"))
        self.label_9.setText(_translate("Form", "最长"))
        self.checkBox_5.setText(_translate("Form", "开启自动退本"))
        self.label_10.setToolTip("Enables backing out of a Raid without retreating while under Semi/Full Auto after a certain period of time has passed.")
        self.label_10.setText(_translate("Form", "指定时间后退出Raid转下只，仅适用auto/FA模式"))
        self.label_11.setText(_translate("Form", "最大时间（分钟）"))
        self.label_11.setToolTip("Set the maximum amount of minutes to be in a Raid while under Semi/Full Auto before moving on to the next Raid.")
        self.checkBox_6.setText(_translate("Form", "开启不超时模式"))
        self.label_12.setText(_translate("Form", "伐木稀有Raid时不启用超时判断(?)"))
        self.label_12.setToolTip("Enable no timeouts when attempting to farm Raids that appear infrequently.")
        self.checkBox_7.setText(_translate("Form", "开启战斗刷新"))
        self.label_13.setText(_translate("Form", "在auto/FA模式时攻击后刷新，不影响战斗脚本"))
        self.label_13.setToolTip("Enables the ability to refresh to speed up Combat Mode whenever the Attack button disappears when it is pressed or during Full/Semi Auto. This option takes precedence above anyother related setting to reloading during combat except via the reload command in a script.")
        self.checkBox_8.setText(_translate("Form", "开启自动施放快速召唤石"))
        self.label_14.setText(_translate("Form", "开启战斗刷新后才有效，会在auto/FA模式下自动施放快速召唤石"))
        self.label_14.setToolTip("Enables the ability to automatically use Quick Summon during Full/Semi Auto. Note that this option only takes into effect when 'Enable Refreshing during Combat' is turned onand that the bot is fighting a battle that is compatible with refreshing during combat.")
        self.checkBox.setText(_translate("Form", "开启忽略重置召唤石"))
        self.label_4.setText(_translate("Form", "开启后若找不到召唤石会默认选第一个"))
        self.label_4.setToolTip("Enables bypassing the bot resetting Summons if there are none of your chosen found during Summon Selection. The bot will reload the page and select the very first summon at the top of the list.")
        self.checkBox_9.setText(_translate("Form", "开启静态窗口校准"))
        self.label_15.setText(_translate("Form", "开启后不能移动游戏窗口，禁用时会把整个计算机屏幕视做游戏窗口，可以在运行时自由移动鼠标"))
        self.label_15.setToolTip("Enable calibration of game window to be static. This will assume that you do not move the game window around during the bot process. Otherwise, the bot will not see where to go next. Disable to have the whole computer screen act as the game window and you can move around the window during the bot process as you wish.")
        self.checkBox_10.setText(_translate("Form", "开启防机器人检测"))
        self.label_16.setText(_translate("Form", "每次运行后将鼠标移出游戏窗口，并等待几秒后恢复操作"))
        self.label_16.setToolTip("Enable attempt at bypassing possible bot detection via mouse. What this does is moves the mouse off of the game window after every run and waits several seconds there before resuming bot operations.")
        self.checkBox_11.setText(_translate("Form", "开启战斗脚本替代选择功能"))
        self.label_17.setText(_translate("Form", "无法正常使用战斗脚本时会选择系统默认脚本"))
        self.label_17.setToolTip("Enable this if the regular method of combat script selection failed.")
        self.checkBox_15.setText(_translate("Form", "超级鹰验证码识别"))
        self.checkBox_15.setToolTip("付费api，如需要请自行注册充值")
        self.lineEdit_2.setPlaceholderText(_translate("Form", "账号"))
        self.lineEdit_5.setPlaceholderText(_translate("Form", "密码"))
        self.label_18.setText(_translate("Form", "转世沙盒设置"))
        self.checkBox_17.setToolTip(_translate("Form", "Experimental, it uses default party and the chosen script for combat."))
        self.checkBox_17.setText(_translate("Form", "开启gold chest opening"))
        self.checkBox_18.setText(_translate("Form", "开始Defender怪配置"))
        self.label_5.setText(_translate("Form", "打几次"))
        self.lineEdit_6.setPlaceholderText(_translate("Form", "选择战斗脚本"))
        self.label_6.setText(_translate("Form", "编成"))
        self.label_21.setText(_translate("Form", "队伍"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.tab_2), _translate("Form", "设置"))
        self.textBrowser.setReadOnly(True)


