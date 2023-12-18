from sqlalchemy.sql import text

from ..env.config import engine, get_logger

logger = get_logger('food_dao')


def get_restaurant_food_dao(restaurant_id: str):
    logger.info('get_restaurant_food_dao()')
    logger.info(f'restaurant_id:{restaurant_id}')
    query = "SELECT food_id, restaurant_id, food_name, food_price FROM Food WHERE restaurant_id=:restaurant_id"
    try:
        result = engine.execute(text(query), {"restaurant_id": restaurant_id}).mappings().all()
        return result
    except Exception as e:
        logger.error(f"Error occurs when get_restaurant_food_dao(), error message: {e}")


def get_food_dao(food_id: str):
    logger.info('get_food_dao()')
    logger.info(f'food_id:{food_id}')
    query = "SELECT * FROM Food WHERE food_id=:food_id"
    try:
        result = engine.execute(text(query), {"food_id": food_id}).mappings().all()
        return result
    except Exception as e:
        logger.error(f"Error occurs when get_food_dao(), error message: {e}")
