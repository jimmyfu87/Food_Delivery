from sqlalchemy.sql import text

from ..env.config import engine, get_logger

logger = get_logger('payment_dao')


def get_all_payment_dao():
    logger.info('get_all_payment_dao()')
    query = "SELECT payment_name FROM Payment"
    try:
        result = engine.execute(text(query)).mappings().all()
        return result
    except Exception as e:
        logger.error("Error occurs when get_all_payment_dao(), error message: {}".format(e))


