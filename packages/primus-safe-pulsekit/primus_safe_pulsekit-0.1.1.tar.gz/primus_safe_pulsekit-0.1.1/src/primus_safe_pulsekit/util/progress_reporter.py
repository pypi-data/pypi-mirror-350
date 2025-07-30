import threading
import queue
import time
from typing import Iterator, Tuple, Optional


class ProgressReporter:
    def __init__(self):
        self._progress = 0.0  # 范围：[0.0, 1.0]
        self._done = False
        self._lock = threading.Lock()
        self._log_queue = queue.Queue()
        self._condition = threading.Condition()
        self._result = ''

    def report_progress(self, progress: float):
        with self._lock:
            self._progress = min(max(progress, 0.0), 1.0)
        with self._condition:
            self._condition.notify_all()  # 通知监听线程有更新

    def log(self, message: str):
        self._log_queue.put(message)
        with self._condition:
            self._condition.notify_all()

    def mark_done(self, result:str=''):
        if result != '':
            self._result = result
        with self._lock:
            self._done = True
        with self._condition:
            self._condition.notify_all()

    def get_latest_progress(self) -> float:
        with self._lock:
            return self._progress

    def is_done(self) -> bool:
        with self._lock:
            return self._done
    def set_result(self, result: str):
        self._result = result

    def get_result(self)-> str:
        return self._result

    def stream_updates(self, timeout: Optional[float] = None) -> Iterator[Tuple[float, Optional[str]]]:
        """
        监听线程调用此方法，流式获取进度和日志更新。
        每次迭代返回一个元组：(progress, log_message)，其中 log_message 可以为 None 表示仅进度更新。
        监听线程应在遍历时检查 is_done() 是否为 True 以决定是否退出。
        """
        latest_progress = 0.0
        while True:
            with self._condition:
                self._condition.wait(timeout=timeout)

            while not self._log_queue.empty():
                latest_progress = self.get_latest_progress()
                yield (latest_progress, self._log_queue.get())

            if self.is_done():
                # 任务结束后仍然处理队列中剩余日志
                while not self._log_queue.empty():
                    print('deal with reamin logs')
                    yield (self.get_latest_progress(), self._log_queue.get())
                break
            if latest_progress != self.get_latest_progress():
                yield (self.get_latest_progress(), None)

    def wait_for_done(self):
        while not self.is_done():
            try:
                with self._lock:
                    self._condition.wait(0.5)
            except RuntimeError:
                pass


