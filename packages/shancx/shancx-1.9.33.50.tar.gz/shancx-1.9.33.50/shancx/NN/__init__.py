#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
def start():
    print("import successful")
# constants
__author__ = 'shancx'
 
__author_email__ = 'shancx@126.com'

# @Time : 2023/09/27 下午8:52
# @Author : shanchangxi
# @File : util_log.py
 

import logging
from logging.handlers import RotatingFileHandler
import os
from shancx import crDir 
def _loggers(logger_name="loggers", root="./logs", phase="project", level=logging.INFO, screen=True, max_bytes=10*1024*1024, backup_count=5, overwrite=False):
    '''set up logger with rotating file handler'''
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s", datefmt='%Y-%m-%d %H:%M:%S') 
    log_file = os.path.join(root, '{}.log'.format(phase))
    crDir(log_file)
    # Use RotatingFileHandler with 'w' mode to overwrite log file if needed
    mode = 'w' if overwrite else 'a'
    fh = RotatingFileHandler(log_file, mode=mode, maxBytes=max_bytes, backupCount=backup_count)
    fh.setFormatter(formatter)    
    l.setLevel(level)
    l.addHandler(fh)    
    if screen:
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        l.addHandler(sh)    
    return l


"""
logger = _loggers(logger_name="test_logger", root=curpathplus, phase="test_log", overwrite=True, screen=True)
# 测试日志输出
for i in range(5):
    logger.info(f"这是日志消息 {i+1}")
    time.sleep(1)
"""
 