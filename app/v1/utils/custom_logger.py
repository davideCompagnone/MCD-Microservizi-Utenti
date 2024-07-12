""" Implementazione della classe custom logger per gestire i log in modo personalizzato."""

import logging
import json
import os
import sys


class LogSetupper:
    def __init__(self, name: str):
        self._name = name

    def setup(self) -> logging.Logger:
        app_logger = logging.getLogger(self._name)
        app_logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        formatter = self._setup_local_formatter()
        handler.setFormatter(formatter)
        app_logger.handlers = []
        app_logger.addHandler(handler)
        return app_logger

    def _setup_test_formatter(self) -> logging.Formatter:
        formatter = CustomFormatter()
        return formatter

    def _setup_local_formatter(self) -> logging.Formatter:
        format_msg = "[%(asctime)s] [%(module)s] %(levelname)s --- %(message)s (%(filename)s:%(lineno)s)"
        formatter = logging.Formatter(format_msg, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter


class CustomFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super(CustomFormatter, self).__init__(*args, **kwargs)

    def format(self, record: logging.LogRecord):
        log_data = {
            "severity": record.levelname,
            "message": f"{record.filename} - {record.funcName}() line: {record.lineno} - {record.getMessage()}",
            "name": record.name,
            "function_name": f"{record.filename} - {record.funcName}() line: {record.lineno}",
        }
        return json.dumps(log_data)
