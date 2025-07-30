import atexit
import json
import os
import sys
import threading
import time
import uuid
import datetime
from pathlib import Path
import traceback
from typing import Optional

import requests
from loguru import logger
import socket


MONITOR_ENDPOINT = "http://127.0.0.1:14000/endpoint"
LOG_PATH = Path("C:\\logs") if sys.platform == "win32" else Path("/logs")
MAX_RETRY = 100
MONITOR_INTERVAL = 10

class SpiderInfo:
    def __init__(self, name=None, group_name=None, monitor=True,task_type=0, show_debug=False,monitor_endpoint='http://127.0.0.1:14000/endpoint'):
        self._monitor_endpoint = monitor_endpoint
        self.pid = str(os.getpid())
        self.uid = str(uuid.uuid4())
        self.parent_uid = None
        self.name = name
        self.group_name = group_name
        self.start_time = datetime.datetime.now()
        self.end_time = None
        self.run_time = None
        self.log_file = None
        self.file = None
        self.interpreter = sys.executable
        self.status = 0
        self.insert_count = 0
        self.progress = 0
        self.total_progress = 0
        self.exception = None
        self.exception_stack = None
        self.msg = ''
        self.data = ''
        self.task_type = task_type
        self.server = os.getenv("SERVER_NAME")
        self._show_debug = show_debug
        self._is_monitor = monitor
        self._today = datetime.date.today()
        self._lock = threading.Lock()
        self.lan_ip = '127.0.0.1'
        self.wan_ip = '0.0.0.0'
        self._monitor_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

        sys.excepthook = self.__global_exception_handler
        atexit.register(self.__before_exit)

        self.__initialize_log_file()

        if self._is_monitor:
            self.start_monitor()
            self.notice()

        self.__init_ip()


    def __initialize_log_file(self):
        self.__get_script_info()
        if self.log_file:
            logger.add(self.log_file, rotation="50 MB")
        self.status = 1

    def __get_script_info(self):
        main_module = sys.modules.get('__main__')
        filepath = main_module.__file__
        self.file = filepath
        self.log_file = self.__get_log_path(filepath)

    def __get_log_path(self, file_path: str) -> str:
        # 基础日志目录
        base_log_path = LOG_PATH
        original_path = Path(file_path).resolve()
        stem_name = original_path.stem
        timestamp = datetime.datetime.now().strftime("%m%d-%H%M%S.%f")[:-3].replace('.', '')
        log_filename = f"{stem_name}-{timestamp}.log"

        # 获取脚本路径相对于根目录的结构
        rel_path = original_path.parent.relative_to(original_path.anchor)
        full_path = base_log_path / rel_path / log_filename
        full_path.parent.mkdir(parents=True, exist_ok=True)
        return str(full_path)

    def __global_exception_handler(self, exc_type, exc_value, exc_traceback):
        self.debug('全局异常捕获')
        stack_trace = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logger.error(f"发生异常: {exc_type.__name__}: {exc_value}\n堆栈信息:\n{stack_trace}")
        self.exception_stack = stack_trace
        self.exception = f"{exc_type}:{exc_value}"
        self.status = -1
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    def __before_exit(self):
        self.debug('程序退出')
        self.end_time = datetime.datetime.now()
        self.run_time = self.end_time - self.start_time
        if self.status != -1:
            self.status = 2
        logger.warning(f'运行时长: {self.run_time} 秒')
        if self._is_monitor:
            self.notice()
        logger.warning(self)

    def __init_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("223.5.5.5", 80))
            self.lan_ip = s.getsockname()[0]
            s.close()
        except Exception:
            try:
                self.lan_ip = socket.gethostbyname(socket.gethostname())
            except:
                pass
        self.wan_ip = os.getenv("WAN_IP", '0.0.0.0')
        if self.wan_ip == '0.0.0.0':
            try:
                response = requests.get('https://ipinfo.io/json', timeout=5)
                self.wan_ip = response.json()['ip']
            except:
                pass

    def debug(self, msg):
        if self._show_debug:
            logger.warning(msg)

    def to_dict(self):
        data = {}
        for k, v in self.__dict__.items():
            if k.startswith('_'):
                continue
            if isinstance(v, datetime.datetime):
                data[k] = v.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(v, datetime.timedelta):
                data[k] = v.total_seconds()
            elif k == 'data' and v:
                data[k] = json.dumps(v, ensure_ascii=False)
            else:
                data[k] = v
        return data

    def __repr__(self):
        return (
            f"SpiderInfo(pid={self.pid}, uid={self.uid}, name={self.name}, group={self.group_name}, "
            f"lan_ip={self.lan_ip}, wan_ip={self.wan_ip}, start_time={self.start_time}, "
            f"end_time={self.end_time}, run_time={self.run_time}, log_file={self.log_file}, "
            f"file={self.file}, interpreter={self.interpreter}, status={self.status}, "
            f"insert_count={self.insert_count}, progress={self.progress}, "
            f"total_progress={self.total_progress}, exception={self.exception})")

    def __monitor(self):
        num = 0
        while not self._stop_event.is_set():
            if datetime.date.today() > self._today:
                self.reset()
            result = self.notice()
            if not result:
                num += 1
                if num >= MAX_RETRY:
                    logger.error(f'上传数据失败，超过最大重试次数 {MAX_RETRY} 次，终止上报')
                    break
            else:
                num = 0
            time.sleep(MONITOR_INTERVAL)

    def notice(self):
        try:
            self.debug('上报数据')
            data = self.to_dict()
            self.debug(data)
            response = requests.post(url=self._monitor_endpoint, json=data, timeout=4)
            self.debug(response.text)
            return True
        except requests.exceptions.RequestException as e:
            self.debug(f'上报失败: {e}')
            return False

    def start_monitor(self):
        self.debug('启动监控')
        self._monitor_thread = threading.Thread(target=self.__monitor)
        self._monitor_thread.setDaemon(True)
        self._monitor_thread.start()

    def update_count(self, v: int = 1):
        with self._lock:
            self.insert_count += v

    def add_count(self, v: int = 1):
        with self._lock:
            self.insert_count += v
    def add_progress(self, v: int = 1):
        with self._lock:
            self.progress += v


    def stop(self):
        self._stop_event.set()
        self.__before_exit()

    def reset(self,msg=''):
        # 重置
        now = datetime.datetime.now()
        data = self.to_dict()
        data['run_time'] = (now - self.start_time).total_seconds()
        data['end_time'] = now.strftime("%Y-%m-%d %H:%M:%S")
        data['msg'] = data['msg'] + msg
        data['status'] = 2
        is_notice = False
        for _ in range(5):
            try:
                self.debug('上报数据reset')
                self.debug(data)
                response = requests.post(url=self._monitor_endpoint, json=data, timeout=4)
                self.debug(response.text)
                is_notice = True
                break
            except Exception as e:
                self.debug(f'上报失败: {e}')
                continue

        if is_notice:
            if not self.parent_uid:
                self.parent_uid = self.uid
            self.uid = str(uuid.uuid4())
            self.start_time = now
            self.insert_count = 0
            self._today = datetime.date.today()


