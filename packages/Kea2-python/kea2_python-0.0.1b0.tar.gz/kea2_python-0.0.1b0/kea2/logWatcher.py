import re
import os
import threading
import time


PATTERN_EXCEPTION = re.compile(r"\[Fastbot\].+Internal\serror\n([\s\S]*)")
PATTERN_STATISTIC = re.compile(r".+Monkey\sis\sover!\n([\s\S]+)")


def thread_excepthook(args):
    print(args.exc_value, flush=True)
    os._exit(1)



class LogWatcher:

    def watcher(self, poll_interval=1):
        self.buffer = ""
        self.last_pos = 0

        while True:
            self.read_log()
            time.sleep(poll_interval)
        
    def read_log(self):
        time.sleep(0.02)
        with open(self.log_file, 'r', encoding='utf-8') as f:
            f.seek(self.last_pos)
            new_data = f.read()
            self.last_pos = f.tell()

            if new_data:
                self.buffer += new_data
            self.parse_log()

    def parse_log(self):
        buffer = self.buffer
        exception_match = PATTERN_EXCEPTION.search(buffer)
        if exception_match:
            exception_body = exception_match.group(1).strip()
            if exception_body:
                raise RuntimeError(
                    "[Error] Execption while running fastbot:\n" + 
                    exception_body + 
                    "\nSee fastbot.log for details."
                )
        statistic_match = PATTERN_STATISTIC.search(buffer)
        if statistic_match:
            statistic_body = statistic_match.group(1).strip()
            if statistic_body:
                print(
                    "[INFO] Fastbot exit:\n" + 
                    statistic_body
                , flush=True)

    def __init__(self, log_file):
        self.log_file = log_file

        threading.excepthook = thread_excepthook
        t = threading.Thread(target=self.watcher, daemon=True)
        t.start()
    
    def close(self):
        time.sleep(0.2) # wait for the written logfile close
        self.read_log()


if __name__ == "__main__":
    LogWatcher("fastbot.log")