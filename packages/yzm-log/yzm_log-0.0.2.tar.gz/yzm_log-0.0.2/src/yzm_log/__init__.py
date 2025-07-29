# -*- coding: utf-8 -*-

import datetime
import logging.config
import logging.config as log_conf
import os
import coloredlogs

'''
 * @Author       : Zhengmin Yu
 * @Description  : Log file configuration
'''

"""
Set the log output color style
"""
coloredlogs.DEFAULT_FIELD_STYLES = {
    'asctime': {
        'color': 'green'
    },
    'hostname': {
        'color': 'magenta'
    },
    'levelname': {
        'color': 'green',
        'bold': True
    },
    'request_id': {
        'color': 'yellow'
    },
    'name': {
        'color': 'blue'
    },
    'programname': {
        'color': 'cyan'
    },
    'threadName': {
        'color': 'yellow'
    }
}


class LoggerExec:
    """
    Log Set
    """

    def __init__(
        self,
        name: str = None,
        log_path: str = None,
        level: str = "INFO",
        is_solitary: bool = True,
        is_form_file: bool = False,
        size: int = 104857600,
        backup_count: int = 10,
        encoding: str = "UTF-8"
    ):
        """
        Log initialization
        :param name: Project Name
        :param log_path: Log file output path. Default is log_%Y%m%d.log.
        :param level: Log printing level. Default is INFO.
        :param is_solitary: When the file path is consistent (here, the log_path parameter is not a specific file name, but a file path), whether the file is formed independently according to the name parameter. Default is True.
        :param is_form_file: Whether to form a log file. Default is True.
        :param size: Setting the file size if a file is formed. Default is 104857600. (100MB)
        :param backup_count: Setting the number of rotating files if a file is formed. Default is 10.
        :param encoding: Setting of file encoding if a file is formed. Default is UTF-8.
        """
        self.name = name
        self.log_path = log_path
        self.level = level
        # Get Today's Time
        self.today = datetime.datetime.now().strftime("%Y%m%d")
        # Default File Name
        self.default_log_file = f"{name}_log_{self.today}.log" if name and is_solitary else f"log_{self.today}.log"

        self.log_path_name = self.get_log_path() if is_form_file else None

        # Define two log output formats
        standard_format = '[%(asctime)s] [%(threadName)s:%(thread)d] [task_id:%(name)s] [%(filename)s:%(lineno)d] [%(levelname)s] ===> %(message)s'
        simple_format = '[%(levelname)s] [%(asctime)s] [%(filename)s:%(lineno)d] ===> %(message)s'

        # Log printed to the terminal
        handlers_sh = {
            # Print to screen
            'class': 'logging.StreamHandler',
            'level': self.level,
            'formatter': 'simple'
        }
        # Print logs to files and collect logs with info and above
        handlers_fh = {
            'level': self.level,
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            # log file
            'filename': self.log_path_name,
            # Log size in bytes, default: 100MB
            'maxBytes': size,
            # Number of rotating files
            'backupCount': backup_count,
            # Encoding of log files
            'encoding': encoding,
        }

        # log Configuration Dictionary
        self.logging_dic = {
            # Version number
            'version': 1,
            # Fixed notation
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': standard_format
                },
                'simple': {
                    '()': 'coloredlogs.ColoredFormatter',
                    'format': simple_format,
                    'datefmt': '%Y-%m-%d  %H:%M:%S'
                }
            },
            'filters': {},
            'handlers': {
                'sh': handlers_sh,
                'fh': handlers_fh
            } if is_form_file else {
                'sh': handlers_sh
            },
            'loggers': {
                # Logger configuration obtained by logging.getLogger(__name__)
                '': {
                    # Here, we add the two handlers defined above, that is, log data is written to a file and printed to the screen
                    'handlers': ['sh', 'fh'] if is_form_file else ['sh'],
                    'level': self.level,
                    # Pass up (higher level loggers)
                    'propagate': True,
                },
            },
        }

        # Log level color input style
        self.level_style = {
            'debug': {
                'color': 'white'
            },
            'info': {
                'color': 'green'
            },
            'warn': {
                'color': 'yellow'
            },
            'error': {
                'color': 'red',
                'bold': True,
            }
        }

    def get_log_path(self) -> str:
        """
        Get log output path
        :return:
        """
        # Determine whether it exists
        if self.log_path:
            log_path_file = self.log_path if self.log_path.endswith(".log") else os.path.join(self.log_path, self.default_log_file)
            log_path = os.path.dirname(self.log_path) if self.log_path.endswith(".log") else self.log_path
            # create folder
            if not os.path.exists(log_path):
                os.makedirs(log_path)
            return log_path_file
        else:
            return os.path.join(self.default_log_file)

    def __setting__(self):
        """
        Log Settings
        :return:
        """
        # Import the logging configuration defined above to configure this log through the dictionary method
        log_conf.dictConfig(self.logging_dic)
        # Generate a log instance where parameters can be passed to the task_id
        logger = logging.getLogger(self.name)
        # Set Color
        coloredlogs.install(level=self.level, level_styles=self.level_style, logger=logger)
        return logger


class Logger:
    """
    Log initialization
    """

    def __init__(
        self,
        name: str = None,
        log_path: str = None,
        level: str = "INFO",
        is_solitary: bool = True,
        is_form_file: bool = False,
        size: int = 104857600,
        backup_count: int = 10,
        encoding: str = "UTF-8"
    ):
        """
        Log initialization
        :param name: Project Name
        :param log_path: Log file output path. Default is log_%Y%m%d.log.
        :param level: Log printing level. Default is INFO.
        :param is_solitary: When the file path is consistent (here, the log_path parameter is not a specific file name, but a file path), whether the file is formed independently according to the name parameter. Default is True.
        :param is_form_file: Whether to form a log file. Default is True.
        :param size: Setting the file size if a file is formed. Default is 104857600. (100MB)
        :param backup_count: Setting the number of rotating files if a file is formed. Default is 10.
        :param encoding: Setting of file encoding if a file is formed. Default is UTF-8.
        """
        self.name = name
        self.log_path = log_path
        self.level = level
        self.is_solitary = is_solitary
        self.is_form_file = is_form_file
        self.size = size
        self.backup_count = backup_count
        self.encoding = encoding
        self.log = self.logger()

    def logger(self):
        """
        Get log
        :return:
        """
        return LoggerExec(self.name, self.log_path, self.level, self.is_solitary, self.is_form_file, self.size, self.backup_count, self.encoding).__setting__()

    def debug(self, content: str):
        """
        Log debug information
        :param content: content
        :return:
        """
        return self.log.debug(content)

    def info(self, content: str):
        """
        log info information
        :param content: content
        :return:
        """
        return self.log.info(content)

    def warning(self, content: str):
        """
        log warn information
        :param content: content
        :return:
        """
        return self.log.warning(content)

    def error(self, content: str):
        """
        log error information
        :param content: content
        :return:
        """
        return self.log.error(content)

    def disabled(self):
        self.log.disabled = True

    def enabled(self):
        self.log.disabled = False
