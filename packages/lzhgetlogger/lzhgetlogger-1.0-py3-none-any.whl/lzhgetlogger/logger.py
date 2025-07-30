import logging
import os
import re
import sys
import uuid

class SmartPathFormatter(logging.Formatter):
    def format(self, record):
        path = record.pathname
        match = re.search(r"site-packages[\\/](.*)", path)
        if match:
            record.smart_path = match.group(1)
        else:
            try:
                record.smart_path = os.path.relpath(path, start=sys.path[0])
            except ValueError:
                record.smart_path = path
        return super().format(record)

def get_logger(level=logging.INFO, name: str=None) -> logging.Logger:
    if name is None:
        name = str(uuid.uuid4())  # 自动生成唯一名称
    
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setFormatter(SmartPathFormatter(
            "%(asctime)s | %(levelname)+7s | [%(smart_path)s:%(lineno)d] | %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        logger.addHandler(ch)
        logger.propagate = False  # 避免向 root logger 传播

    return logger

def get_file_logger(filename="log.csv", level=logging.INFO, name: str=None) -> logging.Logger:
    if name is None:
        name = str(uuid.uuid4())  # 自动生成唯一名称
    
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(level)
        ch = logging.FileHandler(filename=filename, mode="a", encoding="utf-8")
        ch.setFormatter(SmartPathFormatter(
            "%(asctime)s,%(levelname)s,%(smart_path)s:%(lineno)d,%(message)s",
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        logger.addHandler(ch)
        logger.propagate = False  # 避免向 root logger 传播

    return logger

if __name__ == "__main__":
    
    logger1 = get_logger(level = logging.INFO, name = "logger1")  # 定义一个普通`logger`
    logger2 = get_logger(level = logging.INFO)  # 如果未指定`name`，则会生成一个`uuid`给`name`
    logger3 = get_file_logger(filename="log.csv", level = logging.INFO, name = "logger3")  # 定义一个文件`logger`

    logger1.info("log from logger1")
    logger2.info("log from logger2")
    logger3.info("log from logger3")


