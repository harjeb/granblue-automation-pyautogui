# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ga.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(859, 479)
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
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)

        self.checkBox_15 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_15.setObjectName("checkBox_15")
        self.horizontalLayout_2.addWidget(self.checkBox_15)

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
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.horizontalLayout_4.addWidget(self.label_2)
        self.spinBox_3 = QtWidgets.QSpinBox(self.tab)
        self.spinBox_3.setMinimum(1)
        self.spinBox_3.setMaximum(14)
        self.spinBox_3.setObjectName("spinBox_3")
        self.horizontalLayout_4.addWidget(self.spinBox_3)
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.horizontalLayout_4.addWidget(self.label_3)
        self.spinBox_2 = QtWidgets.QSpinBox(self.tab)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(6)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout_4.addWidget(self.spinBox_2)
        self.comboBox_4 = QtWidgets.QComboBox(self.tab)
        self.comboBox_4.setObjectName("comboBox_4")
        self.horizontalLayout_4.addWidget(self.comboBox_4)
        self.checkBox_13 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_13.setObjectName("checkBox_13")
        self.horizontalLayout_4.addWidget(self.checkBox_13)
        self.checkBox_14 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_14.setObjectName("checkBox_14")
        self.horizontalLayout_4.addWidget(self.checkBox_14)

        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.horizontalLayout_4.addWidget(self.label_4)
        self.spinBox_4 = QtWidgets.QSpinBox(self.tab)
        self.spinBox_4.setMinimum(1)
        self.spinBox_4.setMaximum(14)
        self.spinBox_4.setObjectName("spinBox_4")
        self.horizontalLayout_4.addWidget(self.spinBox_4)
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.horizontalLayout_4.addWidget(self.label_5)
        self.spinBox_5 = QtWidgets.QSpinBox(self.tab)
        self.spinBox_5.setMinimum(1)
        self.spinBox_5.setMaximum(14)
        self.spinBox_5.setObjectName("spinBox_5")
        self.horizontalLayout_4.addWidget(self.spinBox_5)
        
        self.comboBox_5 = QtWidgets.QComboBox(self.tab)
        self.comboBox_5.setObjectName("comboBox_5")
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
        self.textBrowser = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.TabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayoutWidget = QtWidgets.QWidget(self.tab_2)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 0, 751, 421))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox_10 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBox_10.setObjectName("checkBox_10")
        self.gridLayout.addWidget(self.checkBox_10, 4, 1, 1, 1)
        self.checkBox_7 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBox_7.setObjectName("checkBox_7")
        self.gridLayout.addWidget(self.checkBox_7, 4, 0, 1, 1)
        self.checkBox_3 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout.addWidget(self.checkBox_3, 3, 0, 1, 1)
        self.checkBox_6 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBox_6.setObjectName("checkBox_6")
        self.gridLayout.addWidget(self.checkBox_6, 3, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 6, 0, 1, 1)
        self.checkBox_5 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBox_5.setObjectName("checkBox_5")
        self.gridLayout.addWidget(self.checkBox_5, 2, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 6, 1, 1, 1)
        self.checkBox_8 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBox_8.setObjectName("checkBox_8")
        self.gridLayout.addWidget(self.checkBox_8, 1, 0, 1, 1)
        self.checkBox_4 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout.addWidget(self.checkBox_4, 0, 1, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 2, 0, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 0, 0, 1, 1)
        self.checkBox_9 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBox_9.setObjectName("checkBox_9")
        self.gridLayout.addWidget(self.checkBox_9, 1, 1, 1, 1)
        self.checkBox_11 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBox_11.setObjectName("checkBox_11")
        self.gridLayout.addWidget(self.checkBox_11, 5, 0, 1, 1)
        self.checkBox_12 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBox_12.setObjectName("checkBox_12")
        self.gridLayout.addWidget(self.checkBox_12, 5, 1, 1, 1)
        self.TabWidget.addTab(self.tab_2, "")
        self.horizontalLayout_5.addWidget(self.TabWidget)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(Form)
        self.TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "钢铁侠再再生"))
        self.label.setText(_translate("Form", "次数"))
        self.label.setToolTip(_translate("Form", "执行任务次数，最高999"))
        self.lineEdit.setPlaceholderText(_translate("Form", "任务队列"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "选择动作脚本"))
        self.pushButton_2.setText(_translate("Form", "添加到队列"))
        self.pushButton_2.setToolTip(_translate("Form", "添加执行任务到队列"))
        self.label_2.setText(_translate("Form", "选择编成"))
        self.label_2.setToolTip(_translate("Form", "编成序号，默认为1-14，从左往右Set A 是1-7，Set B是8-14"))
        self.label_3.setText(_translate("Form", "选择队伍"))
        self.label_3.setToolTip(_translate("Form", "队伍序号，默认为1-6，从左往右1-6"))
        self.label_4.setText(_translate("Form", "编成"))
        self.label_4.setToolTip(_translate("Form", "编成序号，默认为1-14，从左往右Set A 是1-7，Set B是8-14"))
        self.label_5.setText(_translate("Form", "队伍"))
        self.label_5.setToolTip(_translate("Form", "队伍序号，默认为1-6，从左往右1-6"))
        self.checkBox_13.setText(_translate("Form", "Debug模式"))
        self.checkBox_13.setToolTip(_translate("Form", "是否开启Debug日志输出"))
        self.checkBox_14.setText(_translate("Form", "Nightmare"))
        self.checkBox_14.setToolTip(_translate("Form", "是否开启活动Nightmare难度设置，需要在设置界面设置"))
        self.checkBox_15.setText(_translate("Form", "团本默认召唤石"))
        self.checkBox_15.setToolTip(_translate("Form", "团本(舔表)时默认选择第一个召唤石，提高进本速度"))
        self.pushButton.setText(_translate("Form", "开始"))
        initialMessage = """****************************************\nWelcome to Granblue Automation!\n****************************************\nInstructions\n----------------\nNote: The START button is disabled until the following steps are followed through.\n
    1. Have your game window and the Bottom Menu visible. Set the game window size set to the second "notch". 
    2. Go to the Settings Page of the bot and fill out the sections until the status at the top says "Ready".
    3. You can now head back to the Home Page of the bot and click START.
    \nWarning: Do not refresh/F5 the program's "page" while the bot process is running. Otherwise in order to stop it, you will need to kill it by completely exiting the program.\n****************************************\n"""

        self.textBrowser.setText(_translate("Form", initialMessage))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.tab), _translate("Form", "主页"))
        self.checkBox_10.setText(_translate("Form", "CheckBox"))
        self.checkBox_7.setText(_translate("Form", "CheckBox"))
        self.checkBox_3.setText(_translate("Form", "CheckBox"))
        self.checkBox_6.setText(_translate("Form", "CheckBox"))
        self.checkBox_5.setText(_translate("Form", "CheckBox"))
        self.checkBox_8.setText(_translate("Form", "CheckBox"))
        self.checkBox_4.setText(_translate("Form", "CheckBox"))
        self.checkBox_2.setText(_translate("Form", "CheckBox"))
        self.checkBox.setText(_translate("Form", "CheckBox"))
        self.checkBox_9.setText(_translate("Form", "CheckBox"))
        self.checkBox_11.setText(_translate("Form", "CheckBox"))
        self.checkBox_12.setText(_translate("Form", "CheckBox"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.tab_2), _translate("Form", "设置"))


