import logging


logger = logging.getLogger("app_loger")
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] : %(message)s")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)