import logging
import logging.handlers

import configparser

logger = logging.getLogger(__name__)

def setup_logging():
    config_path = r'E:\python\spider\project\zhihu\cnf\task.cnf'
    config = configparser.ConfigParser()
    config.read(config_path)
    level_json = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    level = config['log']['level']
    logger.setLevel(level_json[level])
    formatter = logging.Formatter(
        fmt='[%(levelname)s] %(asctime)s  %(filename)s[line:%(lineno)d]  %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # 控制台打印
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    # 存入文件，自动轮转
    file_handler = logging.handlers.RotatingFileHandler(
        filename=config['log']['path'],
        maxBytes=1024 * 1024 * 5,
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

setup_logging()

