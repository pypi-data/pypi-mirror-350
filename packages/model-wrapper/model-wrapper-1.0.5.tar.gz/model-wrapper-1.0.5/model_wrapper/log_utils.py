from logging import basicConfig, INFO, getLogger, Formatter, StreamHandler

logger = getLogger(__name__)
formatter = Formatter('[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

handler = StreamHandler()
handler.setLevel(INFO)
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.setLevel(INFO)


def info(message):
	logger.info(message)


def warn(message):
	logger.warning(message)
