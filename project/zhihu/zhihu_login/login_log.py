import logging
import logging.handlers
import configparser

logger = logging.getLogger(__name__)

def set_log():
    config = configparser.ConfigParser()
    config.read(r"E:\python\spider\project\zhihu\cnf\login.cnf", encoding='utf-8')
    log_path = config['log']['path']
    level = config['log']['level']
    level_json = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    fromatter = logging.Formatter(
        fmt='[%(levelname)s] %(asctime)s  %(filename)s[line:%(lineno)d]  %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_path,
        maxBytes=1024 * 1024 * 5,
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(fromatter)
    logger.setLevel(level_json[level])
    logger.addHandler(file_handler)

set_log()