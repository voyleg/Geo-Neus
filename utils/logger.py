import logging


class Logger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        self.debug = RShiftLogFn(self.debug)
        self.info = RShiftLogFn(self.info)

    @classmethod
    def prepare_logger(cls, loglevel, logger_id):
        logging.setLoggerClass(cls)
        logger = logging.getLogger(logger_id)
        logger.setLevel(loglevel)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(loglevel)
        stream_handler.setFormatter(logger.formatter)
        logger.addHandler(stream_handler)

        return logger

    @property
    def formatter(self):
        return logging.Formatter(fmt='%(asctime)s %(levelname).1s %(filename)s:%(lineno)d  %(message)s')

    def add_logfile(self, file, loglevel):
        file_handler = logging.FileHandler(file)
        file_handler.setLevel(loglevel)
        file_handler.setFormatter(self.formatter)
        self.addHandler(file_handler)


class RShiftLogFn:
    def __init__(self, log_fn):
        self._log_fn = log_fn

    def __call__(self, msg, *args, **kwargs):
        kwargs['stacklevel'] = kwargs.get('stacklevel', 1) + 1
        self._log_fn(msg, *args, **kwargs)

    def __rrshift__(self, msg):
        return self._log_fn(msg, stacklevel=2)


logger = Logger.prepare_logger(loglevel='DEBUG', logger_id='geo_neus')
