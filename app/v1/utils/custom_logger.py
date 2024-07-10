""" Implementazione della classe custom logger per gestire i log in modo personalizzato."""

import logging
import json
import os
import sys


class LogSetupper:
    def __init__(self, name: str):
        self._env = os.getenv("ENV", "local")
        self._name = name
        assert self._env in [
            "test",
            "local",
            "prod",
        ], "Valore non valido per la variabile ambientale ENV. Got {}".format(self._env)

    def setup(self) -> logging.Logger:
        app_logger = logging.getLogger(self._name)
        if self._env == "test":
            # Settings per il logger in ambiente test
            app_logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler(sys.stdout)
            formatter = self._setup_local_formatter()

        elif self._env == "local":
            # Settings per il logger in ambiente locale
            # TODO modificare i settings per l'ambiente prod se necessario
            app_logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler(sys.stdout)
            formatter = self._setup_local_formatter()

        else:
            # Settings per il logger in ambiente locale
            # TODO modificare i settings per l'ambiente prod se necessario
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
