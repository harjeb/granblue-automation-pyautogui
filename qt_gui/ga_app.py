from ga_ui import *
import sys
import time
import os
import json
from PyQt5.QtWidgets import (QApplication,
                            QWidget,
                            QTableWidgetItem,
                            QTableWidget,
                            QFileDialog,
                            QHeaderView,
                            QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal,QProcess
from PyQt5 import QtGui, QtCore
from io import StringIO
import traceback
import socket
import shutil
import re
import logging
import ctypes
import uuid
CP_console = f"cp{ctypes.cdll.kernel32.GetConsoleOutputCP()}"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

if not os.path.exists('log'):
    os.makedirs('log')

current_date = time.strftime("%m_%d_%H_%M_%S_", time.localtime())
logname = 'log/' + current_date + 'ga.log'  # 指定输出的日志文件名

fh = logging.FileHandler(logname, encoding='utf-8', mode='a')
fh.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
custom_format = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'
# formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
formatter = logging.Formatter(custom_format)
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


def excepthook(excType, excValue, tracebackobj):
    """
    Global function to catch unhandled exceptions.
    @param excType exception type
    @param excValue exception value
    @param tracebackobj traceback object
    """
    separator = '-' * 80
    logFile = "error.log"
    notice = \
        """An unhandled exception occurred. Please report the problem\n"""\
        """using the error reporting dialog or via email to <%s>.\n"""\
        """A log has been written to "%s".\n\nError information:\n""" % \
        ("harjeb@outlook.com", "")
    versionInfo="2.0.3c"
    timeString = time.strftime("%Y-%m-%d, %H:%M:%S")
    tbinfofile = StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: \n%s' % (str(excType), str(excValue))
    sections = [separator, timeString, separator, errmsg, separator, tbinfo]
    msg = '\n'.join(sections)
    try:
        f = open(logFile, "w")
        f.write(msg)
        f.write(versionInfo)
        f.close()
    except IOError:
        pass
    errorbox = QMessageBox()
    errorbox.setText(str(notice)+str(msg)+str(versionInfo))
    errorbox.exec_()

sys.excepthook = excepthook


def iconFromBase64(base64):
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
    icon = QtGui.QIcon(pixmap)
    return icon


image_base64 = b"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"


class Sleep_Thread(QThread):
    status = QtCore.pyqtSignal()

    def __init__(self, _time):
        super(Sleep_Thread,self).__init__()
        self.sleep_time = _time

    def run(self):
        time.sleep(self.sleep_time)
        self.status.emit()


class GBF_AutoTool(QWidget, Ui_Form):
    def __init__(self,parent=None):
        super(GBF_AutoTool, self).__init__(parent)
        self.setupUi(self)
        # UI初始化
        icon = iconFromBase64(image_base64)
        self.setWindowIcon(icon)
        try:
            if getattr(sys, 'frozen', False):
                application_path = os.path.dirname(sys.executable)
            elif __file__:
                application_path = os.path.dirname(__file__)
            self.ROOT_PATH = application_path
            #print(self.ROOT_PATH)
            _file = open(f"{self.ROOT_PATH}/data/data_zhcn.json",encoding='utf-8')
            _summon = open(f"{self.ROOT_PATH}/data/summons_zhcn.json",encoding='utf-8')
            _translate = open(f"{self.ROOT_PATH}/data/translate.json",encoding='utf-8')
        except FileNotFoundError:
            QMessageBox.warning(self,
                                "错误",
                                "没找到资源文件",
                                QMessageBox.Yes)
            sys.exit(1)

        self.gamemode_dict = json.load(_file)
        self.summons_dict = json.load(_summon)
        self.translate_dict = json.load(_translate)

        self.summons_list = []
        for v in self.summons_dict.values():
            self.summons_list.extend(v["summons"])

        self.comboBox.addItems(list(self.gamemode_dict.keys()))
        #self.comboBox.activated[str].connect(self.onActivatedText)

        # 战斗脚本内容
        self.mainscript = []
        self.mainscript_name = ''
        self.nmscript = []
        self.nmscript_name = ''
        self.defenderscript_name = ''
        self.defenderscript = []

        # 任务队列
        self.action_queue = [0]
        # 任务列表 - 新的拖拽任务管理
        self.task_items = []

        # 脚本缓存相关
        self._script_cache = {}
        self._script_cache_timestamp = 0
        self._cache_validity_seconds = 30  # 缓存30秒

        # 初始化脚本组合框
        self.populate_script_combo()
        
        # 执行系统健康检查
        self.check_system_health()

        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.add_task_to_list)
        self.remove_task_button.clicked.connect(self.remove_task_from_list)
        self.clear_tasks_button.clicked.connect(self.clear_all_tasks)
        self.task_list_widget.model().rowsMoved.connect(self.handle_task_reorder)
        self.task_list_widget.itemSelectionChanged.connect(self.handle_task_list_selection_change)

        dirs = self.ROOT_PATH+'/backend/farm_queue'
        if os.path.exists(dirs):
            shutil.rmtree(dirs)

        # 保持与旧版本的兼容性 - 保留lineEdit_3的文件对话框功能  
        if hasattr(self, 'lineEdit_3'):
            self.lineEdit_3.clicked.connect(self.openFileNameDialog)

        # 游戏状态
        self.running = False

        self.process = QtCore.QProcess()
        self.process.readyReadStandardError.connect(self.onReadyReadStandardError)
        self.process.readyReadStandardOutput.connect(self.onReadyReadStandardOutput)
        self.process.finished.connect(self.onFinished)
        # self.main_thread = Game_Thread()
    
    def _find_scripts_directory(self):
        """智能查找scripts目录 - 支持开发环境和编译后环境"""
        possible_script_dirs = [
            # 编译后环境优先：exe同目录下的scripts文件夹
            os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "scripts"),
            # 编译后环境：当前工作目录下的scripts  
            os.path.join(os.getcwd(), "scripts"),
            # PyInstaller环境：相对于当前文件的scripts
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"),
            # 开发环境：../src-tauri/scripts路径（仅开发时存在）
            os.path.join(self.ROOT_PATH, "..", "src-tauri", "scripts"),
            # 备选路径：Python可执行文件目录
            os.path.join(os.path.dirname(sys.executable), "scripts"),
        ]
        
        for dir_path in possible_script_dirs:
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                logger.info(f"找到脚本目录: {dir_path}")
                return dir_path
        
        logger.warning(f"未找到scripts目录。尝试过的路径: {possible_script_dirs}")
        return None

    def check_system_health(self):
        """执行系统健康检查"""
        issues = []
        
        try:
            # 检查脚本目录 - 支持多种部署环境
            scripts_dir = self._find_scripts_directory()
            if not scripts_dir:
                issues.append("脚本目录不存在，某些功能可能无法正常工作")
            elif not os.access(scripts_dir, os.R_OK):
                issues.append("脚本目录无读取权限")
            
            # 检查必需的JSON文件
            required_files = [
                "data/data_zhcn.json",
                "data/summons_zhcn.json", 
                "data/translate.json"
            ]
            
            for file_path in required_files:
                full_path = os.path.join(self.ROOT_PATH, file_path)
                if not os.path.exists(full_path):
                    issues.append(f"缺少必需文件: {file_path}")
            
            # 检查backend目录写入权限
            backend_dir = os.path.join(self.ROOT_PATH, "backend")
            if os.path.exists(backend_dir) and not os.access(backend_dir, os.W_OK):
                issues.append("backend目录无写入权限，任务保存可能失败")
            
            # 检查日志目录
            log_dir = os.path.join(self.ROOT_PATH, "log")
            if not os.path.exists(log_dir):
                try:
                    os.makedirs(log_dir)
                except Exception:
                    issues.append("无法创建日志目录")
            
            if issues:
                warning_text = "系统检查发现以下问题：\n\n" + "\n".join(f"• {issue}" for issue in issues)
                warning_text += "\n\n建议检查安装和权限设置。"
                logger.warning("系统健康检查发现问题: " + ", ".join(issues))
                
                # 不阻塞启动，只记录警告
                if len(issues) > 2:  # 只在问题较多时显示警告
                    QMessageBox.warning(self, "系统检查警告", warning_text, QMessageBox.Yes)
            else:
                logger.info("系统健康检查通过")
                
        except Exception as e:
            logger.error(f"系统健康检查失败: {str(e)}")
            QMessageBox.warning(self, "系统检查失败", 
                              f"无法完成系统健康检查：\n{str(e)}\n\n"
                              "程序将继续运行，但某些功能可能受影响。", 
                              QMessageBox.Yes)
    
    def scan_combat_scripts(self, force_refresh=False):
        """扫描src-tauri/scripts目录中的.txt文件 - 带缓存"""
        current_time = time.time()
        
        # 检查缓存是否有效
        if (not force_refresh and 
            self._script_cache and 
            (current_time - self._script_cache_timestamp) < self._cache_validity_seconds):
            logger.info("使用脚本缓存数据")
            return self._script_cache.get('scripts', [])
        
        scripts_dir = self._find_scripts_directory()
        if not scripts_dir:
            logger.warning("未找到scripts目录")
            return []
            
        try:
            if os.path.exists(scripts_dir) and os.path.isdir(scripts_dir):
                scripts = []
                script_details = {}
                
                for f in os.listdir(scripts_dir):
                    if f.endswith('.txt'):
                        script_path = os.path.join(scripts_dir, f)
                        try:
                            # 验证文件可读性
                            if os.path.isfile(script_path) and os.access(script_path, os.R_OK):
                                scripts.append(f)
                                # 缓存文件修改时间以供后续验证
                                try:
                                    script_details[f] = {
                                        'path': script_path,
                                        'mtime': os.path.getmtime(script_path),
                                        'size': os.path.getsize(script_path)
                                    }
                                except OSError:
                                    # 如果获取文件信息失败，仍然包含该文件但不缓存详细信息
                                    script_details[f] = {'path': script_path}
                        except (OSError, IOError) as e:
                            logger.warning(f"无法访问脚本文件 {f}: {str(e)}")
                            continue
                
                # 更新缓存
                self._script_cache = {
                    'scripts': scripts,
                    'details': script_details,
                    'scripts_dir': scripts_dir
                }
                self._script_cache_timestamp = current_time
                
                logger.info(f"扫描到 {len(scripts)} 个脚本文件，已更新缓存")
                return scripts
            else:
                logger.warning(f"脚本目录不存在或不可访问: {scripts_dir}")
                # 清空缓存
                self._script_cache = {}
                self._script_cache_timestamp = 0
                return []
        except (OSError, IOError, PermissionError) as e:
            logger.error(f"扫描脚本目录时出错: {str(e)}")
            # 在出错时，如果有缓存数据且不是强制刷新，返回缓存数据
            if not force_refresh and self._script_cache:
                logger.info("扫描出错，使用缓存数据")
                return self._script_cache.get('scripts', [])
            return []
    
    def refresh_script_cache(self):
        """手动刷新脚本缓存"""
        logger.info("手动刷新脚本缓存")
        return self.scan_combat_scripts(force_refresh=True)
    
    def populate_script_combo(self, force_refresh=False):
        """动态填充战斗脚本下拉框"""
        try:
            scripts = self.scan_combat_scripts(force_refresh)
            
            self.combat_script_combo.clear()
            if scripts:
                for script in sorted(scripts):
                    try:
                        display_name = script.replace('.txt', '')
                        self.combat_script_combo.addItem(display_name, script)
                    except Exception as e:
                        logger.warning(f"添加脚本 {script} 到下拉框时出错: {str(e)}")
                        continue
                
                if self.combat_script_combo.count() == 0:
                    self.combat_script_combo.addItem("无可用脚本", "")
            else:
                self.combat_script_combo.addItem("未找到脚本", "")
                logger.info("未在脚本目录中找到任何.txt文件")
        except Exception as e:
            logger.error(f"填充脚本下拉框时出错: {str(e)}")
            self.combat_script_combo.clear()
            self.combat_script_combo.addItem("加载失败", "")
    
    def get_task_display_text(self, task_type, script, count):
        """生成任务显示文本"""
        script_name = script.replace('.txt', '') if script else "无脚本"
        return f"{task_type} | {script_name} | {count}次"
    
    def add_task_to_list(self):
        """添加任务到列表 - 增强错误反馈"""
        # 检查任务数量限制
        if len(self.task_items) >= 10:
            QMessageBox.warning(self, "任务数量限制", 
                              "任务列表已达到最大限制（10个）。\n请先删除一些任务再添加新任务。", 
                              QMessageBox.Yes)
            return
        
        # 获取用户输入
        task_type = self.comboBox.currentText()
        script_data = self.combat_script_combo.currentData()
        script_name = self.combat_script_combo.currentText()
        count = self.spinBox.value()
        
        # 验证任务类型
        if not task_type:
            QMessageBox.warning(self, "选择错误", 
                              "请选择一个有效的游戏模式。", 
                              QMessageBox.Yes)
            return
        
        # 验证脚本选择
        if not script_data or script_data == "":
            error_msg = "请选择一个战斗脚本。\n\n"
            if self.combat_script_combo.count() == 0:
                scripts_dir = self._find_scripts_directory()
                error_msg += "系统未找到任何脚本文件。请确保：\n"
                error_msg += f"• scripts目录存在：{scripts_dir or '未找到scripts目录'}\n"
                error_msg += "• 目录中包含.txt格式的脚本文件\n"
                error_msg += "• 脚本文件可读且非空"
            elif script_name in ["未找到脚本", "无可用脚本", "加载失败"]:
                error_msg += "脚本加载出现问题。请尝试：\n"
                error_msg += "• 检查scripts目录是否存在\n"
                error_msg += "• 重启应用程序\n"
                error_msg += "• 检查脚本文件权限"
            
            QMessageBox.warning(self, "脚本选择错误", error_msg, QMessageBox.Yes)
            return
        
        # 验证执行次数
        if count < 1 or count > 9999:
            QMessageBox.warning(self, "次数设置错误", 
                              f"执行次数必须在1-9999范围内。\n当前设置：{count}", 
                              QMessageBox.Yes)
            return
            
        # 创建任务数据
        task_item = {
            "type": task_type,
            "script": script_data,
            "script_name": script_name,
            "count": count,
            "id": str(uuid.uuid4())
        }
        
        # 读取和验证脚本内容 - 使用智能路径检测
        scripts_dir = self._find_scripts_directory()
        if not scripts_dir:
            QMessageBox.critical(self, "脚本目录错误", 
                               "无法找到scripts目录。请检查应用程序安装。",
                               QMessageBox.Yes)
            return
            
        script_path = os.path.join(scripts_dir, script_data)
        try:
            if not os.path.exists(script_path):
                QMessageBox.critical(self, "脚本文件错误", 
                                   f"脚本文件不存在：\n{script_path}\n\n"
                                   "请确认脚本文件是否已删除或移动。",
                                   QMessageBox.Yes)
                # 刷新脚本列表
                self.populate_script_combo(force_refresh=True)
                return
            
            if not os.path.isfile(script_path):
                QMessageBox.critical(self, "脚本文件错误", 
                                   f"路径不是有效文件：\n{script_path}",
                                   QMessageBox.Yes)
                return
            
            if not os.access(script_path, os.R_OK):
                QMessageBox.critical(self, "脚本文件权限错误", 
                                   f"无法读取脚本文件：\n{script_path}\n\n"
                                   "请检查文件权限设置。",
                                   QMessageBox.Yes)
                return
            
            # 读取脚本内容
            with open(script_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                script_content = [line.strip() for line in lines]
                
                if not script_content or all(not line for line in script_content):
                    QMessageBox.warning(self, "脚本内容错误", 
                                      f"脚本文件为空：\n{script_name}\n\n"
                                      "请检查脚本文件是否包含有效内容。",
                                      QMessageBox.Yes)
                    return
                
                task_item["script_content"] = script_content
                
        except UnicodeDecodeError as e:
            QMessageBox.critical(self, "脚本编码错误", 
                               f"无法解析脚本文件编码：\n{script_name}\n\n"
                               f"错误详情：{str(e)}\n\n"
                               "请确保脚本文件使用UTF-8编码。",
                               QMessageBox.Yes)
            return
        except PermissionError:
            QMessageBox.critical(self, "权限错误", 
                               f"没有权限访问脚本文件：\n{script_name}\n\n"
                               "请检查文件权限或以管理员身份运行程序。",
                               QMessageBox.Yes)
            return
        except Exception as e:
            QMessageBox.critical(self, "读取脚本失败", 
                               f"读取脚本文件时发生未知错误：\n{script_name}\n\n"
                               f"错误详情：{str(e)}\n\n"
                               "请检查文件是否损坏或被其他程序占用。",
                               QMessageBox.Yes)
            logger.error(f"读取脚本文件失败: {script_path}, 错误: {str(e)}")
            return
            
        self.task_items.append(task_item)
        
        # 更新UI显示
        display_text = self.get_task_display_text(task_type, script_data, count)
        self.task_list_widget.addItem(display_text)
        
        # 更新任务队列字符串以保持兼容性
        self.update_task_queue_string()
    
    def remove_task_from_list(self):
        """从列表中删除选中的任务 - 增强错误反馈"""
        current_row = self.task_list_widget.currentRow()
        
        if len(self.task_items) == 0:
            QMessageBox.information(self, "任务列表为空", 
                                  "任务列表中没有任何任务。\n请先添加任务后再进行删除操作。", 
                                  QMessageBox.Yes)
            return
        
        if current_row < 0:
            QMessageBox.warning(self, "未选择任务", 
                              f"请先选择要删除的任务。\n\n"
                              f"操作方法：\n"
                              f"• 在任务列表中点击选中要删除的任务\n"
                              f"• 然后点击「删除选中」按钮\n\n"
                              f"当前任务总数：{len(self.task_items)}", 
                              QMessageBox.Yes)
            return
        
        if current_row >= len(self.task_items):
            QMessageBox.warning(self, "索引错误", 
                              "选中的任务索引超出范围，任务列表可能已发生变化。\n"
                              "请重新选择任务后再试。", 
                              QMessageBox.Yes)
            self.refresh_task_list_display()
            return
        
        # 直接删除任务，无需确认
        try:
            self.task_items.pop(current_row)
            self.task_list_widget.takeItem(current_row)
            self.update_task_queue_string()
        except Exception as e:
            QMessageBox.critical(self, "删除失败", 
                               f"删除任务时发生错误：\n{str(e)}\n\n"
                               "任务列表可能不同步，正在刷新...", 
                               QMessageBox.Yes)
            self.refresh_task_list_display()
    
    def clear_all_tasks(self):
        """清空所有任务 - 增强错误反馈"""
        if len(self.task_items) == 0:
            QMessageBox.information(self, "任务列表为空", 
                                  "任务列表中没有任何任务，无需清空操作。", 
                                  QMessageBox.Yes)
            return
        
        # 直接清空所有任务，无需确认
        try:
            self.task_items.clear()
            self.task_list_widget.clear()
            self.update_task_queue_string()
        except Exception as e:
            QMessageBox.critical(self, "清空失败", 
                               f"清空任务时发生错误：\n{str(e)}\n\n"
                               "正在尝试恢复任务列表状态...", 
                               QMessageBox.Yes)
            self.refresh_task_list_display()
    
    def handle_task_list_selection_change(self):
        """处理任务列表选择变化"""
        # 可以在这里添加选择变化的处理逻辑
        pass
    
    def handle_task_reorder(self, parent, start, end, destination, row):
        """处理任务列表重排序 - 改进的安全实现"""
        try:
            # 验证参数有效性
            if not hasattr(self, 'task_items') or not isinstance(self.task_items, list):
                logger.error("任务列表不存在或类型错误")
                return
            
            # 验证索引边界
            if not (0 <= start < len(self.task_items)):
                logger.error(f"起始索引 {start} 超出范围 [0, {len(self.task_items)})")
                return
            
            # 计算目标插入位置，确保边界安全
            target_row = max(0, min(row, len(self.task_items)))
            
            # 如果目标位置和起始位置相同，则无需移动
            if start == target_row or (target_row == start + 1):
                return
            
            # 安全地执行移动操作
            if target_row > start:
                # 向后移动
                insert_index = target_row - 1
            else:
                # 向前移动
                insert_index = target_row
            
            # 确保插入索引在有效范围内
            insert_index = max(0, min(insert_index, len(self.task_items) - 1))
            
            # 执行移动
            item = self.task_items.pop(start)
            self.task_items.insert(insert_index, item)
            
            # 更新队列字符串
            self.update_task_queue_string()
            
            logger.info(f"任务从位置 {start} 移动到位置 {insert_index}")
            
        except Exception as e:
            logger.error(f"任务重排序时出错: {str(e)}")
            # 尝试恢复UI状态
            try:
                self.refresh_task_list_display()
            except Exception as recovery_error:
                logger.error(f"恢复任务列表显示失败: {str(recovery_error)}")
    
    def refresh_task_list_display(self):
        """刷新任务列表显示"""
        try:
            self.task_list_widget.clear()
            for task in self.task_items:
                display_text = self.get_task_display_text(
                    task.get('type', '未知类型'),
                    task.get('script', ''),
                    task.get('count', 0)
                )
                self.task_list_widget.addItem(display_text)
        except Exception as e:
            logger.error(f"刷新任务列表显示失败: {str(e)}")
    
    def update_task_queue_string(self):
        """更新任务队列字符串以保持向后兼容性"""
        if not self.task_items:
            self.lineEdit.setText("")
            return
        
        task_strings = []
        for i, task in enumerate(self.task_items, 1):
            task_strings.append(f"任务{i}")
        
        queue_string = "，".join(task_strings)
        self.lineEdit.setText(queue_string)
    
    def highlight_current_task(self, task_index):
        """高亮当前执行的任务"""
        for i in range(self.task_list_widget.count()):
            item = self.task_list_widget.item(i)
            if i == task_index:
                # 设置高亮颜色
                item.setBackground(QtGui.QColor(200, 255, 200))  # 浅绿色
                original_text = item.text()
                if " [执行中]" not in original_text:
                    item.setText(original_text + " [执行中]")
            else:
                # 恢复正常颜色
                item.setBackground(QtGui.QColor(255, 255, 255))  # 白色
                text = item.text()
                if " [执行中]" in text:
                    item.setText(text.replace(" [执行中]", ""))


    def saveFarmList(self):
        """保存农场任务列表 - 已修改为使用新的任务列表格式"""
        if not self.task_items:
            QMessageBox.warning(self, "错误", "任务列表为空", QMessageBox.Yes)
            return
        
        if len(self.task_items) > 10:
            QMessageBox.warning(self, "错误", "最多支持10个任务", QMessageBox.Yes)
            return
        
        # 验证每个任务
        for i, task in enumerate(self.task_items, 1):
            is_valid, error_message = self.validate_task(task)
            if not is_valid:
                QMessageBox.warning(self, "错误", f"任务{i}配置错误: {error_message}", QMessageBox.Yes)
                return
        
        # 保存每个任务为单独的JSON文件
        dirs = self.ROOT_PATH + '/backend/farm_queue'
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        
        # 清除现有队列编号
        self.action_queue = [0]
        
        try:
            for i, task in enumerate(self.task_items, 1):
                self.action_queue.append(i)
                # 设置当前任务配置
                self.set_task_configuration(task)
                # 使用现有逻辑保存
                self.saveSettings(dirs, f'settings{i}')
            
            # 更新任务队列字符串
            self.update_task_queue_string()
            
            logger.info(f"已保存{len(self.task_items)}个任务到队列")
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"保存任务时出错: {str(e)}", QMessageBox.Yes)
    
    def validate_task(self, task):
        """验证任务配置 - 增强版本，提供详细验证"""
        if not isinstance(task, dict):
            logger.error("任务配置不是有效的字典类型")
            return False, "任务配置格式错误"
        
        # 验证必需字段
        required_fields = ['type', 'script', 'count']
        for field in required_fields:
            if field not in task or not task[field]:
                logger.error(f"任务缺少必需字段: {field}")
                return False, f"缺少必需字段: {field}"
        
        # 验证任务类型
        task_type = task.get('type', '')
        if task_type not in list(self.gamemode_dict.keys()):
            logger.error(f"无效的任务类型: {task_type}")
            return False, f"无效的任务类型: {task_type}"
        
        # 验证脚本文件名
        script_name = task.get('script', '')
        if not script_name.endswith('.txt'):
            logger.error(f"脚本文件名格式错误: {script_name}")
            return False, f"脚本文件必须是.txt格式: {script_name}"
        
        # 验证脚本文件存在性和可读性
        scripts_dir = self._find_scripts_directory()
        if not scripts_dir:
            logger.error("无法找到scripts目录")
            return False, "无法找到scripts目录，请检查安装"
            
        script_path = os.path.join(scripts_dir, script_name)
        try:
            if not os.path.exists(script_path):
                logger.error(f"脚本文件不存在: {script_path}")
                return False, f"脚本文件不存在: {script_name}"
            
            if not os.path.isfile(script_path):
                logger.error(f"脚本路径不是文件: {script_path}")
                return False, f"脚本路径不是文件: {script_name}"
            
            if not os.access(script_path, os.R_OK):
                logger.error(f"脚本文件不可读: {script_path}")
                return False, f"脚本文件不可读: {script_name}"
            
            # 验证脚本文件内容不为空
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content:
                        logger.error(f"脚本文件为空: {script_path}")
                        return False, f"脚本文件为空: {script_name}"
            except Exception as e:
                logger.error(f"读取脚本文件失败: {script_path}, 错误: {str(e)}")
                return False, f"无法读取脚本文件: {script_name}"
                
        except Exception as e:
            logger.error(f"验证脚本文件时出错: {str(e)}")
            return False, f"验证脚本文件时出错: {str(e)}"
        
        # 验证执行次数
        count = task.get('count', 0)
        try:
            count_int = int(count)
            if count_int < 1 or count_int > 9999:
                logger.error(f"执行次数超出范围 [1-9999]: {count}")
                return False, f"执行次数必须在1-9999范围内，当前值: {count}"
        except (ValueError, TypeError):
            logger.error(f"执行次数不是有效数字: {count}")
            return False, f"执行次数必须是有效数字: {count}"
        
        # 验证可选字段格式
        if 'id' in task and not isinstance(task['id'], str):
            logger.warning(f"任务ID不是字符串类型: {type(task['id'])}")
        
        if 'script_name' in task and not isinstance(task['script_name'], str):
            logger.warning(f"脚本显示名称不是字符串类型: {type(task['script_name'])}")
        
        if 'script_content' in task and not isinstance(task['script_content'], list):
            logger.warning(f"脚本内容不是列表类型: {type(task['script_content'])}")
        
        logger.info(f"任务验证通过: {task_type} - {script_name} - {count}次")
        return True, "验证通过"
    
    def set_task_configuration(self, task):
        """为保存设置当前任务配置"""
        # 设置脚本内容
        self.defenderscript = task.get('script_content', [])
        self.defenderscript_name = task.get('script', '')
        
        # 设置任务类型 - 需要在comboBox中找到对应项
        task_type = task.get('type', '')
        index = self.comboBox.findText(task_type)
        if index >= 0:
            self.comboBox.setCurrentIndex(index)
        
        # 设置次数
        self.spinBox.setValue(task.get('count', 1))

    def update_queue(self,quest):
        tmp = self.lineEdit.text() + quest
        self.lineEdit.setText(tmp)

    def start(self):
        """开始执行任务 - 增强错误反馈"""
        if not self.running:
            # 检查任务列表
            if len(self.task_items) == 0:
                QMessageBox.warning(self, "无任务可执行",
                                  "任务列表为空，请先添加任务。\n\n"
                                  "操作步骤：\n"
                                  "1. 选择游戏模式\n"
                                  "2. 选择战斗脚本\n"
                                  "3. 设置执行次数\n"
                                  "4. 点击「添加任务」\n"
                                  "5. 点击「开始」执行",
                                  QMessageBox.Yes)
                return
            
            # 验证所有任务
            invalid_tasks = []
            for i, task in enumerate(self.task_items, 1):
                is_valid, error_msg = self.validate_task(task)
                if not is_valid:
                    invalid_tasks.append(f"任务{i}: {error_msg}")
            
            if invalid_tasks:
                error_text = "以下任务配置有误，请修正后再试：\n\n" + "\n".join(invalid_tasks[:5])
                if len(invalid_tasks) > 5:
                    error_text += f"\n... 还有{len(invalid_tasks) - 5}个任务有误"
                
                QMessageBox.warning(self, "任务配置错误", error_text, QMessageBox.Yes)
                return
            
            # 保存任务列表
            try:
                self.saveFarmList()
            except Exception as e:
                QMessageBox.critical(self, "保存任务失败",
                                   f"保存任务配置时发生错误：\n{str(e)}\n\n"
                                   "请检查磁盘空间和写入权限。",
                                   QMessageBox.Yes)
                return
            
            # 启动执行
            try:
                self.pushButton.setText("停止")
                self.running = True
                queue = self.lineEdit.text()
                if not queue:
                    queue = "自动任务队列"
                    
                logger.info(f"开始执行任务队列: {len(self.task_items)}个任务")
                self.process.start('python controller.py %s' % queue)
                
                QMessageBox.information(self, "开始执行",
                                      f"任务已开始执行！\n\n"
                                      f"任务总数：{len(self.task_items)}\n"
                                      f"执行状态将在下方日志区域显示。\n\n"
                                      f"如需停止，请点击「停止」按钮。",
                                      QMessageBox.Yes)
                                      
            except Exception as e:
                self.running = False
                self.pushButton.setText("开始")
                QMessageBox.critical(self, "启动失败",
                                   f"启动任务执行器时发生错误：\n{str(e)}\n\n"
                                   "请检查系统环境和依赖是否正确安装。",
                                   QMessageBox.Yes)
                logger.error(f"启动任务执行器失败: {str(e)}")
        else:
            # 停止执行
            reply = QMessageBox.question(self, '确认停止', 
                                       '确定要停止当前正在执行的任务吗？\n\n'
                                       '停止后当前任务进度将丢失。',
                                       QMessageBox.Yes | QMessageBox.No, 
                                       QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.stop()

    def check_settings(self):
        """检查设置 - 已修改为与新UI兼容"""
        flag = True
        # 新版本使用任务列表，不再检查lineEdit_3
        if hasattr(self, 'combat_script_combo') and self.combat_script_combo.currentData() == "":
            flag = False
            self.combat_script_combo.setStyleSheet("border: 1px solid red;")
        elif hasattr(self, 'lineEdit_3') and self.lineEdit_3.text() == '':
            flag = False
            self.lineEdit_3.setStyleSheet("border: 1px solid red;")
        return flag

    def stop(self):
        self.process.close()
        self.pushButton.setText("开始")
        self.running = False

    def _update_sleep_status(self):
        self.sleep_over = True

    def getElement(self, summons_list):
        # 返回召唤石属性列表
        elements = []
        for s in summons_list:
            for k,v in self.summons_dict.items():
                if s in v["summons"]:
                    elements.append(k)
                    break
        return elements

    def saveSettings(self,save_path,setname):
        # 保存运行配置
        setting_dict = {"game":{},
                        "twitter":{},
                        "discord":{},
                        "api":{},
                        "configuration":{},
                        "misc":{},
                        "nightmare":{},
                        "event":{},
                        "raid":{},
                        "arcarum":{},
                        "generic":{},
                        "xenoClash":{},
                        "adjustment":{},
                        "sandbox":{},
                        "chaojiying":{},
                        "rotb":{}}
        setting_dict["game"]["combatScriptName"] = self.defenderscript_name
        setting_dict["game"]["combatScript"] = self.defenderscript
        setting_dict["game"]["farmingMode"] = self.translate(self.comboBox.currentText())
        setting_dict["game"]["item"] = ""
        setting_dict["game"]["mission"] = ""
        setting_dict["game"]["map"] = ""
        setting_dict["game"]["itemAmount"] = self.spinBox.value()
        setting_dict["game"]["summons"] = []
        setting_dict["game"]["summonDefault"] = False
        setting_dict["game"]["summonElements"] = []
        setting_dict["game"]["groupNumber"] = 0
        setting_dict["game"]["partyNumber"] = 0
        setting_dict["game"]["debugMode"] = False
        setting_dict["twitter"]["twitterUseVersion2"] = False
        setting_dict["twitter"]["twitterAPIKey"] = ''
        setting_dict["twitter"]["twitterAPIKeySecret"] = ''
        setting_dict["twitter"]["twitterAccessToken"] = ''
        setting_dict["twitter"]["twitterAccessTokenSecret"] = ''
        setting_dict["twitter"]["twitterBearerToken"] = ''
        setting_dict["discord"]["enableDiscordNotifications"] = False
        setting_dict["discord"]["discordToken"] = ''
        setting_dict["discord"]["discordUserID"] = ''
        setting_dict["api"]["enableOptInAPI"] = self.checkBox_rest.isChecked()
        setting_dict["api"]["username"] = ''
        setting_dict["api"]["password"] = ''
        setting_dict["configuration"]["enableBezierCurveMouseMovement"] = self.checkBox_2.isChecked()
        setting_dict["configuration"]["mouseSpeed"] = self.doubleSpinBox.value()
        setting_dict["configuration"]["enableDelayBetweenRuns"] = self.checkBox_3.isChecked()
        setting_dict["configuration"]["delayBetweenRuns"] = self.spinBox_4.value()
        setting_dict["configuration"]["enableRandomizedDelayBetweenRuns"] = self.checkBox_4.isChecked()
        setting_dict["configuration"]["delayBetweenRunsLowerBound"] = self.spinBox_6.value()
        setting_dict["configuration"]["delayBetweenRunsUpperBound"] = self.spinBox_7.value()
        setting_dict["configuration"]["enableRefreshDuringCombat"] = self.checkBox_7.isChecked()
        setting_dict["configuration"]["enableAutoQuickSummon"] = self.checkBox_8.isChecked()
        setting_dict["configuration"]["enableBypassResetSummon"] = self.checkBox.isChecked()
        setting_dict["configuration"]["staticWindow"] = self.checkBox_9.isChecked()
        setting_dict["configuration"]["enableMouseSecurityAttemptBypass"] = self.checkBox_10.isChecked()
        setting_dict["misc"]["guiLowPerformanceMode"] = self.checkBox_rest.isChecked()
        setting_dict["misc"]["alternativeCombatScriptSelector"] = self.checkBox_11.isChecked()
        setting_dict["nightmare"]["enableNightmare"] = False
        setting_dict["nightmare"]["enableCustomNightmareSettings"] = True
        setting_dict["nightmare"]["nightmareCombatScriptName"] = self.nmscript_name
        setting_dict["nightmare"]["nightmareCombatScript"] = self.nmscript
        setting_dict["nightmare"]["nightmareSummons"] = []
        setting_dict["nightmare"]["nightmareSummonElements"] = []
        setting_dict["nightmare"]["nightmareGroupNumber"] = 0
        setting_dict["nightmare"]["nightmarePartyNumber"] = 1
        setting_dict["event"]["enableLocationIncrementByOne"] = False
        setting_dict["event"]["selectBottomCategory"] = False
        setting_dict["raid"]["enableAutoExitRaid"] = self.checkBox_5.isChecked()
        setting_dict["raid"]["timeAllowedUntilAutoExitRaid"] = self.spinBox_8.value()
        setting_dict["raid"]["enableNoTimeout"] = self.checkBox_6.isChecked()
        setting_dict["raid"]["hpRemain"] = self.spinBox_hp.value()
        setting_dict["arcarum"]["enableStopOnArcarumBoss"] = True
        setting_dict["generic"]["enableForceReload"] = False
        setting_dict["xenoClash"]["selectTopOption"] = True
        setting_dict["adjustment"]["enableCalibrationAdjustment"] = False
        setting_dict["adjustment"]["adjustCalibration"] = 5
        setting_dict["adjustment"]["enableGeneralAdjustment"] = False
        setting_dict["adjustment"]["adjustButtonSearchGeneral"] = 5
        setting_dict["adjustment"]["adjustHeaderSearchGeneral"] = 5
        setting_dict["adjustment"]["enablePendingBattleAdjustment"] = False
        setting_dict["adjustment"]["adjustBeforePendingBattle"] = 1
        setting_dict["adjustment"]["adjustPendingBattle"] = 2
        setting_dict["adjustment"]["enableCaptchaAdjustment"] = False
        setting_dict["adjustment"]["adjustCaptcha"] = 5
        setting_dict["adjustment"]["enableSupportSummonSelectionScreenAdjustment"] = False
        setting_dict["adjustment"]["adjustSupportSummonSelectionScreen"] = 30
        setting_dict["adjustment"]["enableCombatModeAdjustment"] = False
        setting_dict["adjustment"]["adjustCombatStart"] = 50
        setting_dict["adjustment"]["adjustDialog"] = 2
        setting_dict["adjustment"]["adjustSkillUsage"] = 5
        setting_dict["adjustment"]["adjustSummonUsage"] = 5
        setting_dict["adjustment"]["adjustWaitingForReload"] = 3
        setting_dict["adjustment"]["adjustWaitingForAttack"] = 100
        setting_dict["adjustment"]["adjustCheckForNoLootScreen"] = 1
        setting_dict["adjustment"]["adjustCheckForBattleConcludedPopup"] = 1
        setting_dict["adjustment"]["adjustCheckForExpGainedPopup"] = 1
        setting_dict["adjustment"]["adjustCheckForLootCollectionScreen"] = 1
        setting_dict["adjustment"]["enableArcarumAdjustment"] = False
        setting_dict["adjustment"]["adjustArcarumAction"] = 3
        setting_dict["adjustment"]["adjustArcarumStageEffect"] = 10
        setting_dict["sandbox"]["enableDefender"] = False
        setting_dict["sandbox"]["enableGoldChest"] = True
        setting_dict["sandbox"]["enableCustomDefenderSettings"] = False
        setting_dict["sandbox"]["numberOfDefenders"] = 0
        setting_dict["sandbox"]["defenderCombatScriptName"] = self.defenderscript_name
        setting_dict["sandbox"]["defenderCombatScript"] = self.defenderscript
        setting_dict["sandbox"]["defenderGroupNumber"] = 0
        setting_dict["sandbox"]["defenderPartyNumber"] = 0
        setting_dict["chaojiying"]["username"] = ""
        setting_dict["chaojiying"]["password"] = ""
        setting_dict["event"]["first"] = True
        setting_dict["rotb"]["first"] = int(self.comboBox_rotb_first.currentText())
        setting_dict["rotb"]["method"] = int(self.comboBox_rotb_method.currentText())

        json_str = json.dumps(setting_dict, indent=4)
        with open(save_path+'/%s.json' % setname, 'w') as json_file:
            json_file.write(json_str)

    def translate(self, obj):
        tmp = []
        if type(obj) is str:
            if self.is_contain_chinese(obj):
                return self.translate_dict[obj]
            else:
                return obj
        else:
            for o in obj:
                if self.is_contain_chinese(o):
                    tmp.append(self.translate_dict[o])
                else:
                    tmp.append(o)
            return tmp

    def is_contain_chinese(self,check_str):
        """
        判断字符串中是否包含中文
        :param check_str: {str} 需要检测的字符串
        :return: {bool} 包含返回True， 不包含返回False
        """
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def openFileNameDialog(self):
        """文件选择对话框 - 增强错误处理"""
        lineedit = self.sender()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        
        try:
            fileName, _ = QFileDialog.getOpenFileName(self,"打开文件", "","TXT Files (*.txt)", options=options)
            if not fileName:
                return
            
            # 验证文件
            if not os.path.exists(fileName):
                QMessageBox.warning(self, "文件错误", f"选择的文件不存在：\n{fileName}", QMessageBox.Yes)
                return
            
            if not os.path.isfile(fileName):
                QMessageBox.warning(self, "文件错误", f"选择的路径不是文件：\n{fileName}", QMessageBox.Yes)
                return
            
            if not os.access(fileName, os.R_OK):
                QMessageBox.warning(self, "权限错误", f"无法读取选择的文件：\n{fileName}", QMessageBox.Yes)
                return
            
            lineedit.setText(fileName)
            self.txtFile = lineedit.text()
            
            # 根据控件名称处理不同的脚本类型
            script_content = []
            script_name = os.path.split(fileName)[1]
            
            try:
                with open(self.txtFile, encoding='utf-8') as f:
                    lines = f.readlines()
                    script_content = [line.strip() for line in lines]
                
                if not script_content:
                    QMessageBox.warning(self, "文件错误", f"选择的文件为空：\n{script_name}", QMessageBox.Yes)
                    return
                
            except UnicodeDecodeError:
                QMessageBox.critical(self, "编码错误", 
                                   f"无法读取文件，请确保文件使用UTF-8编码：\n{script_name}", 
                                   QMessageBox.Yes)
                return
            except Exception as e:
                QMessageBox.critical(self, "读取错误", 
                                   f"读取文件时发生错误：\n{script_name}\n\n错误：{str(e)}", 
                                   QMessageBox.Yes)
                return
            
            # 根据控件类型设置相应的脚本变量
            object_name = lineedit.objectName()
            if object_name == 'main_script':
                self.mainscript = script_content
                self.mainscript_name = script_name
                logger.info(f"加载主脚本: {script_name}, 行数: {len(script_content)}")
            elif object_name == 'nightmare_script':
                self.nmscript = script_content
                self.nmscript_name = script_name
                logger.info(f"加载噩梦脚本: {script_name}, 行数: {len(script_content)}")
            elif object_name == 'lineEdit_3':
                # 处理战斗脚本选择 - 向后兼容性
                self.defenderscript = script_content
                self.defenderscript_name = script_name
                logger.info(f"加载战斗脚本: {script_name}, 行数: {len(script_content)}")
            else:
                # 默认作为战斗脚本处理
                self.defenderscript = script_content
                self.defenderscript_name = script_name
                logger.info(f"加载默认脚本: {script_name}, 行数: {len(script_content)}")
            
            # 清除错误样式
            lineedit.setStyleSheet("")
            
        except Exception as e:
            QMessageBox.critical(self, "文件选择错误", 
                               f"选择文件时发生未知错误：\n{str(e)}", 
                               QMessageBox.Yes)
            logger.error(f"文件选择对话框错误: {str(e)}")

    @QtCore.pyqtSlot(str)
    def onActivatedText(self, text):
        self.comboBox.addItems(list(self.gamemode_dict.keys()))

    def onStateChanged(self):
        if self.checkBox_2.isChecked():
            self.doubleSpinBox.setEnabled(True)
        else:
            self.doubleSpinBox.setEnabled(False)
        if self.checkBox_4.isChecked():
            self.spinBox_6.setEnabled(True)
            self.spinBox_7.setEnabled(True)
        else:
            self.spinBox_6.setEnabled(False)
            self.spinBox_7.setEnabled(False)
        if self.checkBox_3.isChecked():
            self.spinBox_4.setEnabled(True)
        else:
            self.spinBox_4.setEnabled(False)
        if self.checkBox_5.isChecked():
            self.spinBox_8.setEnabled(True)
        else:
            self.spinBox_8.setEnabled(False)

    def onReadyReadStandardError(self):
        try:
            error = self.process.readAllStandardError().data().decode('GBK')
            self.textBrowser.appendPlainText(error.strip())
            logger.error(error.strip())
        except:
            error = self.process.readAllStandardError().data().decode()
            self.textBrowser.appendPlainText(error.strip())
            logger.error(error.strip())
        self.textBrowser.moveCursor(QtGui.QTextCursor.End)

    def onReadyReadStandardOutput(self):
        try:
            result = self.process.readAllStandardOutput().data().decode('GBK')
            self.textBrowser.appendPlainText(result.strip())
            logger.info(result.strip())
        except:
            error = self.process.readAllStandardError().data().decode()
            self.textBrowser.appendPlainText(error.strip())
            logger.error(error.strip())
        self.textBrowser.moveCursor(QtGui.QTextCursor.End)

    def onFinished(self, exitCode, exitStatus):
        if exitStatus == 0:
            try:
                self.textBrowser.appendPlainText("---------")
                self.textBrowser.appendPlainText("========Farm 结束========")
                self.textBrowser.moveCursor(QtGui.QTextCursor.End)
                logger.info("---------")
                logger.info("========Farm 结束========")
                self.process.close()
                self.running = False
                self.pushButton.setText('开始')
            except:
                logger.info("---------")
                logger.info("========Farm 结束========")
                self.process.close()
                self.textBrowser.moveCursor(QtGui.QTextCursor.End)
                self.running = False
                self.pushButton.setText('开始')


if __name__ == "__main__":
    app=QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    win=GBF_AutoTool()
    win.show()
    sys.exit(app.exec_())