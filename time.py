# -*- coding: utf-8 -*-
"""
ZGIRC时间同步工具 v4.2
功能：
  - 一键同步系统时间（使用阿里云NTP服务器）
  - 一键更新程序（自动下载最新版本）
  - 查看运行日志
  - 清理过期日志

作者：kuangxing4250
仓库：https://github.com/kuangxing4250/zgirc-time-sync
"""

import os
import sys
import json
import time
import struct
import ctypes
import logging
import subprocess
import threading
import requests
import urllib3
from datetime import datetime
from pathlib import Path

# ==================== 配置信息 ====================
APP_NAME = "ZGIRC时间同步"
VERSION = "4.2"
UPDATE_URL = "http://time.zgric.top/update/lastupdate_time.exe"  # 更新服务器地址

# NTP服务器列表（阿里云）
NTP_SERVERS = [
    "time1.aliyun.com",
    "time2.aliyun.com", 
    "time3.aliyun.com",
    "time4.aliyun.com",
    "time5.aliyun.com",
    "time6.aliyun.com",
    "ntp1.aliyun.com",
    "ntp2.aliyun.com",
]

# 禁用警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 禁用代理
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['NO_PROXY'] = '*'


class TimeSyncApp:
    """时间同步程序主类"""
    
    def __init__(self):
        """
        初始化程序
        设置日志、加载配置
        """
        # 程序所在目录（用于存放日志和配置文件）
        self.program_dir = Path(sys.executable).parent
        self.log_dir = self.program_dir / "log"
        self.log_dir.mkdir(exist_ok=True, parents=True)
        
        # 加载配置
        self.config = self.load_config()
        
        # 设置日志
        self.setup_logging()
        
        # 初始化变量
        self.root = None
        self.last_sync_time = None
        
        self.logger.info(f"程序启动，版本: {VERSION}")
    
    def load_config(self):
        """
        加载配置文件
        返回：配置字典
        """
        config_path = self.program_dir / "config.json"
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"加载配置失败: {e}")
        
        # 默认配置
        return {
            "auto_check_update": True,  # 启动时自动检查更新
            "save_log": True,           # 保存日志
            "log_days": 7              # 日志保留天数
        }
    
    def save_config(self):
        """
        保存配置到文件
        """
        config_path = self.program_dir / "config.json"
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"保存配置失败: {e}")
    
    def setup_logging(self):
        """
        设置日志系统
        根据配置决定是否保存日志文件
        """
        save_log = self.config.get("save_log", True)
        
        if not save_log:
            # 只输出到控制台
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)
            return
        
        # 输出到文件和控制台
        log_file = self.log_dir / f"time_sync_{datetime.now().strftime('%Y%m%d')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def is_admin(self):
        """
        检查是否具有管理员权限
        返回：True=有管理员权限，False=没有
        """
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def check_startup(self):
        """
        检查是否已设置开机自启动
        返回：True=已启用，False=未启用
        """
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, 
                r"Software\Microsoft\Windows\CurrentVersion\Run", 
                0, 
                winreg.KEY_READ
            )
            try:
                winreg.QueryValueEx(key, APP_NAME)
                return True
            except FileNotFoundError:
                return False
        except Exception as e:
            self.logger.error(f"检查启动项失败: {e}")
            return False
    
    def set_startup(self, enable):
        """
        设置开机自启动
        enable: True=启用，False=禁用
        返回：True=成功，False=失败
        """
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, 
                r"Software\Microsoft\Windows\CurrentVersion\Run", 
                0, 
                winreg.KEY_WRITE
            )
            
            if enable:
                exe_path = sys.executable
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{exe_path}"')
            else:
                try:
                    winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError:
                    pass
            
            self.logger.info(f"开机自启动设置{'成功' if enable else '取消成功'}")
            return True
            
        except Exception as e:
            self.logger.error(f"设置启动项失败: {e}")
            return False
    
    def get_ntp_time(self):
        """
        从NTP服务器获取网络时间
        返回：时间字符串(格式: YYYY-MM-DD HH:MM:SS) 或 None
        """
        import socket
        
        for server in NTP_SERVERS:
            try:
                self.logger.info(f"正在连接 {server}...")
                
                # 创建UDP socket连接NTP服务器
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(5)
                
                # 发送NTP请求
                sock.sendto(b'\x1b' + 47 * b'\0', (server, 123))
                
                # 接收响应
                data, _ = sock.recvfrom(1024)
                sock.close()
                
                if data:
                    # 解析NTP时间戳
                    timestamp = struct.unpack('!12I', data)[10]
                    timestamp -= 2208988800  # 转换为Unix时间戳
                    
                    dt = datetime.fromtimestamp(timestamp)
                    result = dt.strftime('%Y-%m-%d %H:%M:%S')
                    
                    self.logger.info(f"获取时间成功: {result}")
                    return result
                    
            except Exception as e:
                self.logger.warning(f"从 {server} 获取时间失败: {e}")
                continue
        
        self.logger.error("所有NTP服务器都无法连接")
        return None
    
    def set_system_time(self, datetime_str):
        """
        设置系统时间
        datetime_str: 时间字符串
        返回：True=成功，False=失败
        """
        try:
            if not self.is_admin():
                self.logger.warning("无管理员权限，尝试使用命令行方式设置时间")
            
            dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            
            # 使用Windows API设置时间
            class SYSTEMTIME(ctypes.Structure):
                _fields_ = [
                    ('wYear', ctypes.c_uint16),
                    ('wMonth', ctypes.c_uint16),
                    ('wDayOfWeek', ctypes.c_uint16),
                    ('wDay', ctypes.c_uint16),
                    ('wHour', ctypes.c_uint16),
                    ('wMinute', ctypes.c_uint16),
                    ('wSecond', ctypes.c_uint16),
                    ('wMilliseconds', ctypes.c_uint16)
                ]
            
            kernel32 = ctypes.windll.kernel32
            systime = SYSTEMTIME()
            systime.wYear = dt.year
            systime.wMonth = dt.month
            systime.wDay = dt.day
            systime.wHour = dt.hour
            systime.wMinute = dt.minute
            systime.wSecond = dt.second
            
            if kernel32.SetLocalTime(ctypes.byref(systime)):
                self.logger.info(f"系统时间已设置为: {datetime_str}")
                return True
            else:
                raise Exception("SetLocalTime返回失败")
                
        except Exception as e:
            self.logger.error(f"设置时间失败: {e}")
            
            # 备用方案：使用命令行
            try:
                date_cmd = f'date {dt.strftime("%Y-%m-%d")}'
                time_cmd = f'time {dt.strftime("%H:%M:%S")}'
                subprocess.run(date_cmd, shell=True, capture_output=True)
                subprocess.run(time_cmd, shell=True, capture_output=True)
                self.logger.info("使用命令行方式设置时间成功")
                return True
            except Exception as e2:
                self.logger.error(f"命令行方式也失败: {e2}")
                return False
    
    def sync_time(self, callback=None):
        """
        同步时间（在线程中执行）
        callback: 回调函数(result, datetime_str)
        """
        def sync_thread():
            self.logger.info("开始同步时间...")
            
            # 获取网络时间
            datetime_str = self.get_ntp_time()
            
            if datetime_str:
                # 设置系统时间
                if self.set_system_time(datetime_str):
                    self.last_sync_time = datetime_str
                    self.logger.info("时间同步完成！")
                    if callback:
                        callback("success", datetime_str)
                    return
            
            # 同步失败
            if callback:
                callback("failed", None)
        
        thread = threading.Thread(target=sync_thread, daemon=True)
        thread.start()
    
    def check_update(self, callback=None):
        """
        检查更新（在线程中执行）
        callback: 回调函数(has_update, latest_version)
        """
        def check_thread():
            self.logger.info(f"正在检查更新... 当前版本: {VERSION}")
            
            try:
                # 获取最新版本信息
                response = requests.get(UPDATE_URL, timeout=10, verify=False)
                
                # 从响应头获取版本
                # 假设更新服务器返回302重定向到最新exe
                # 或者直接返回版本号
                
                if response.status_code == 200:
                    # 下载exe
                    exe_path = self.program_dir / "time_new.exe"
                    
                    with open(exe_path, 'wb') as f:
                        f.write(response.content)
                    
                    exe_size = exe_path.stat().st_size
                    self.logger.info(f"下载完成，大小: {exe_size} bytes")
                    
                    if exe_size > 100000:  # 大于100KB才是有效exe
                        self.logger.info("有新版本可更新")
                        if callback:
                            callback(True, "新版本")
                    else:
                        self.logger.warning("下载的文件太小，可能是错误页面")
                        exe_path.unlink(missing_ok=True)
                        
                        # 备用方案：检查版本号
                        if callback:
                            callback(False, None)
                else:
                    self.logger.warning(f"检查更新失败，HTTP状态码: {response.status_code}")
                    if callback:
                        callback(False, None)
                        
            except Exception as e:
                self.logger.error(f"检查更新失败: {e}")
                if callback:
                    callback(False, None)
        
        thread = threading.Thread(target=check_thread, daemon=True)
        thread.start()
    
    def do_update(self, callback=None):
        """
        执行更新：下载新版本并替换
        callback: 回调函数(result, message)
        """
        def update_thread():
            self.logger.info("开始更新程序...")
            
            try:
                # 下载最新exe
                exe_path = self.program_dir / "time_new.exe"
                old_exe_path = self.program_dir / "time_old.exe"
                current_exe = sys.executable
                
                self.logger.info(f"下载更新: {UPDATE_URL}")
                
                response = requests.get(UPDATE_URL, timeout=120, verify=False, stream=True)
                
                if response.status_code != 200:
                    self.logger.error(f"下载失败，HTTP状态码: {response.status_code}")
                    if callback:
                        callback("failed", f"HTTP {response.status_code}")
                    return
                
                # 保存文件
                total_size = 0
                with open(exe_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            total_size += len(chunk)
                
                self.logger.info(f"下载完成，大小: {total_size} bytes")
                
                # 检查文件有效性
                if total_size < 100000:
                    self.logger.error("文件太小，不是有效的exe")
                    exe_path.unlink(missing_ok=True)
                    if callback:
                        callback("failed", "文件无效")
                    return
                
                # 替换文件
                self.logger.info("替换程序文件...")
                
                try:
                    # 删除旧备份（如果存在）
                    if old_exe_path.exists():
                        old_exe_path.unlink()
                    
                    # 备份当前exe
                    if Path(current_exe).exists():
                        Path(current_exe).rename(old_exe_path)
                    
                    # 重命名新exe
                    exe_path.rename(current_exe)
                    
                    self.logger.info("更新成功！程序将在3秒后重启...")
                    
                    if callback:
                        callback("success", "更新完成")
                    
                    # 3秒后重启
                    threading.Timer(3, self.restart_app).start()
                    
                except PermissionError:
                    self.logger.error("文件替换失败：权限不足")
                    self.logger.info("尝试使用命令行方式替换...")
                    
                    # 备用方案：使用copy命令
                    try:
                        subprocess.run(f'copy /y "{exe_path}" "{current_exe}_new.exe"', shell=True)
                        subprocess.run(f'move /y "{current_exe}_new.exe" "{current_exe}"', shell=True)
                        
                        self.logger.info("更新成功")
                        if callback:
                            callback("success", "更新完成")
                        threading.Timer(3, self.restart_app).start()
                        
                    except Exception as e2:
                        self.logger.error(f"备用方案也失败: {e2}")
                        if callback:
                            callback("failed", str(e2))
                        
                except Exception as e:
                    self.logger.error(f"替换文件失败: {e}")
                    if callback:
                        callback("failed", str(e))
                        
            except Exception as e:
                self.logger.error(f"更新异常: {e}")
                if callback:
                    callback("failed", str(e))
        
        thread = threading.Thread(target=update_thread, daemon=True)
        thread.start()
    
    def restart_app(self):
        """
        重启程序
        """
        try:
            subprocess.Popen([sys.executable])
            self.logger.info("程序已重启")
        except Exception as e:
            self.logger.error(f"重启失败: {e}")
    
    def clean_old_logs(self, days=None):
        """
        清理过期日志文件
        days: 保留天数，默认从配置读取
        返回：清理的文件数量
        """
        if days is None:
            days = self.config.get("log_days", 7)
        
        try:
            from datetime import timedelta
            cutoff = datetime.now() - timedelta(days=days)
            deleted_count = 0
            
            for log_file in self.log_dir.glob("time_sync_*.log"):
                if log_file.stat().st_mtime < cutoff.timestamp():
                    log_file.unlink()
                    deleted_count += 1
            
            self.logger.info(f"已清理 {deleted_count} 个过期日志文件")
            return deleted_count
            
        except Exception as e:
            self.logger.error(f"清理日志失败: {e}")
            return 0
    
    def show_logs(self):
        """
        显示日志查看器窗口
        """
        from tkinter import Toplevel
        from tkinter import scrolledtext
        
        if not self.root:
            return
            
        log_window = Toplevel(self.root)
        log_window.title("日志查看器")
        log_window.geometry("700x500")
        
        text_area = scrolledtext.ScrolledText(log_window, wrap="word")
        text_area.pack(expand=True, fill='both', padx=10, pady=10)
        
        try:
            # 读取最近的日志文件
            log_files = sorted(self.log_dir.glob("time_sync_*.log"), reverse=True)
            
            for log_file in log_files[:5]:
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    text_area.insert("end", f"\n=== {log_file.name} ===\n")
                    text_area.insert("end", content)
                    
                except Exception as e:
                    text_area.insert("end", f"读取{log_file.name}失败: {e}\n")
                    
        except Exception as e:
            text_area.insert("end", f"读取日志失败: {e}\n")
        
        text_area.config(state='disabled')
    
    def create_gui(self):
        """
        创建GUI界面
        """
        from tkinter import Tk, Toplevel, StringVar, BooleanVar, N, S, E, W, HORIZONTAL
        from tkinter import ttk, messagebox, scrolledtext
        
        # 创建主窗口
        self.root = Tk()
        self.root.title(f"{APP_NAME} v{VERSION}")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # 状态变量
        status_var = StringVar(value="就绪")
        last_sync_var = StringVar(value="从未同步")
        startup_var = BooleanVar(value=self.check_startup())
        save_log_var = BooleanVar(value=self.config.get("save_log", True))
        
        # 回调函数：同步完成
        def on_sync_complete(result, datetime_str):
            if result == "success":
                status_var.set("同步成功")
                last_sync_var.set(datetime_str)
            else:
                status_var.set("同步失败")
            self.root.update_idletasks()
        
        # 回调函数：更新完成
        def on_update_complete(result, message):
            if result == "success":
                status_var.set("更新成功，重启中...")
            else:
                status_var.set(f"更新失败: {message}")
            self.root.update_idletasks()
        
        # 回调函数：检查更新完成
        def on_check_update_complete(has_update, version):
            if has_update:
                status_var.set("发现新版本，正在更新...")
                self.root.update()
                self.do_update(callback=on_update_complete)
            else:
                status_var.set("当前是最新版本")
                self.root.update_idletasks()
        
        # 样式设置
        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("TLabel", padding=2)
        
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(W, E))
        
        # 标题
        title_label = ttk.Label(
            main_frame, 
            text=f"🔧 {APP_NAME} v{VERSION}", 
            font=("Microsoft YaHei", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # 状态
        ttk.Label(main_frame, text="状态:").grid(row=1, column=0, sticky=W, pady=5)
        status_label = ttk.Label(
            main_frame, 
            textvariable=status_var, 
            foreground="blue"
        )
        status_label.grid(row=1, column=1, sticky=W, pady=5)
        
        # 上次同步时间
        ttk.Label(main_frame, text="上次同步:").grid(row=2, column=0, sticky=W, pady=5)
        last_sync_label = ttk.Label(main_frame, textvariable=last_sync_var)
        last_sync_label.grid(row=2, column=1, sticky=W, pady=5)
        
        # 分隔线
        separator = ttk.Separator(main_frame, orient=HORIZONTAL)
        separator.grid(row=3, column=0, columnspan=2, sticky=(W, E), pady=15)
        
        # ========== 按钮功能 ==========
        
        # 同步时间按钮
        def sync_action():
            status_var.set("正在同步时间...")
            self.root.update()
            self.sync_time(callback=on_sync_complete)
        
        sync_button = ttk.Button(
            main_frame, 
            text="立即同步时间", 
            command=sync_action
        )
        sync_button.grid(row=4, column=0, columnspan=2, sticky=(W, E), pady=5)
        
        # 一键更新按钮
        def update_action():
            status_var.set("正在检查更新...")
            self.root.update()
            self.check_update(callback=on_check_update_complete)
        
        update_button = ttk.Button(
            main_frame, 
            text="一键更新程序", 
            command=update_action
        )
        update_button.grid(row=5, column=0, columnspan=2, sticky=(W, E), pady=5)
        
        # 开机自启动开关
        def toggle_startup():
            enable = startup_var.get()
            if self.set_startup(enable):
                self.logger.info(f"开机自启动{'已启用' if enable else '已禁用'}")
            else:
                startup_var.set(not enable)
        
        startup_check = ttk.Checkbutton(
            main_frame, 
            text="开机自启动", 
            variable=startup_var,
            command=toggle_startup
        )
        startup_check.grid(row=6, column=0, columnspan=2, sticky=W, pady=5)
        
        # 日志保存开关
        def toggle_save_log():
            self.config["save_log"] = save_log_var.get()
            self.save_config()
            self.logger.info(f"日志保存{'已启用' if save_log_var.get() else '已禁用'}")
        
        save_log_check = ttk.Checkbutton(
            main_frame, 
            text="保存日志", 
            variable=save_log_var,
            command=toggle_save_log
        )
        save_log_check.grid(row=7, column=0, columnspan=2, sticky=W, pady=5)
        
        # 清理日志按钮
        def clean_logs_action():
            count = self.clean_old_logs()
            status_var.set(f"已清理 {count} 个日志文件")
        
        clean_log_button = ttk.Button(
            main_frame, 
            text="清理日志", 
            command=clean_logs_action
        )
        clean_log_button.grid(row=8, column=0, sticky=(W, E), pady=10)
        
        # 查看日志按钮
        view_log_button = ttk.Button(
            main_frame, 
            text="查看日志", 
            command=self.show_logs
        )
        view_log_button.grid(row=8, column=1, sticky=(W, E), pady=10)
        
        # 退出按钮
        quit_button = ttk.Button(
            main_frame, 
            text="退出", 
            command=self.quit_app
        )
        quit_button.grid(row=9, column=1, sticky=(W, E), pady=10)
        
        # 列配置
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        
        # 关闭窗口事件
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        
        self.logger.info("GUI界面已启动")
        
        # 启动主循环
        self.root.mainloop()
    
    def quit_app(self):
        """
        退出程序
        """
        self.logger.info("程序退出")
        if self.root:
            self.root.destroy()
        sys.exit(0)


def main():
    """
    程序入口
    """
    try:
        app = TimeSyncApp()
        app.create_gui()
        
    except KeyboardInterrupt:
        print("\n用户中断，程序退出")
    except Exception as e:
        print(f"\n程序异常: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
