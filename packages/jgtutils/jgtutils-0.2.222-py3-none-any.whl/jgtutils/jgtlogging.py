import logging
import sys
import traceback

_loglevel = logging.WARNING


_logger_name = __name__

logger = None
console_handler = None

errHandler = None

# Create a log format using Log Record attributes
fmt = logging.Formatter(
    "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s"
)

fmt2 = "%(asctime)s %(levelname)s %(message)s"

datefmt = "%Y.%m.%d %H:%M:%S"


def _proto():
    global _loglevel, logger, console_handler,fmt,fmt2,datefmt
    try:
        log_file = __main__.__file__
    except:
        log_file = "jgt"
    try:
        import __main__

        logging.basicConfig(
            filename="{0}.log".format(log_file),
            level=logging.INFO,
            format=fmt,
            datefmt=datefmt,
        )
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(_loglevel)
        logger = logging.getLogger(_logger_name)
        logger.addHandler(console_handler)
        # return logger
    except Exception as e:
        print("Exception: {0}\n{1}".format(e, traceback.format_exc()))
        print("logging failed - dont worry")
        logger = None


def _add_error_handler():
    global logger, errHandler,fmt
    try:
        errHandler = logging.FileHandler("error.log")
        errHandler.setLevel(logging.ERROR)
        errHandler.setFormatter(fmt)
        logger.addHandler(errHandler)
    except:
        print("Failed to add error handler")
        pass




def set_log_level(loglevel: str = "WARNING", logger_name=""):
    global _loglevel, _logger_name, logger
    if logger_name == "":
        logger_name = _logger_name
    _loglevel = getattr(logging, loglevel)
    logger.setLevel(_loglevel)
    # console_handler.setLevel(_loglevel)
    logger.info(f"Log level set to {_loglevel}")


def write_log(msg: str, loglevel: str = "INFO"):
    global _loglevel, logger
    loglevel = getattr(logging, loglevel)
    if loglevel >= _loglevel:
        logger.log(loglevel, msg)


def info(msg: str,*args):
  logger.info(msg,*args)
  #write_log(msg, "INFO")


def warning(msg: str,*args):
  logger.warning(msg,*args)
  


def error(msg: str,*args):
  logger.error(msg,*args)


def critical(msg: str,*args):
  logger.critical(msg,*args)


def debug(msg: str,*args):
  logger.debug(msg,*args)




try: 

    #_proto()
    #_add_error_handler() #BUGGED

    if logger is None:
        logger = logging.getLogger(_logger_name)
    # Create a logger object
    # log = logging.getLogger("jgt.log")
    #logger.setLevel(_loglevel)
except:
    print("Failed to create logger object. Dont worry")