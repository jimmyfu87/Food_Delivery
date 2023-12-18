from sqlalchemy.sql import text

from ..env.config import engine, get_logger

logger = get_logger('restaurant_dao')


def get_all_restaurants_dao():
    logger.info('get_all_restaurants_dao()')
    query = "SELECT restaurant_id, restaurant_name, restaurant_address FROM Restaurant"
    try:
        result = engine.execute(text(query)).mappings().all()
        return result
    except Exception as e:
        logger.error("Error occurs when get_all_restaurants_dao(), error message: {}".format(e))


def get_restaurant_name_by_restaurant_id_dao(restaurant_id: str):
    logger.info('get_restaurant_name_by_restaurant_id_dao()')
    query = "SELECT restaurant_name FROM Restaurant WHERE restaurant_id=:restaurant_id"
    try:
        result = engine.execute(text(query), {"restaurant_id": restaurant_id}).mappings().all()
        return result
    except Exception as e:
        logger.error("Error occurs when get_restaurant_name_dao(), error message: {}".format(e))


def get_restaurant_name_by_food_id_dao(food_id: str):
    logger.info('get_restaurant_name_by_restaurant_id_dao()')
    logger.info(f'food_id: {food_id}')
    query = "SELECT r.restaurant_name FROM Restaurant as r \
             LEFT JOIN Food as f ON f.restaurant_id = r.restaurant_id WHERE f.food_id = :food_id"
    try:
        result = engine.execute(text(query), {"food_id": food_id}).mappings().all()
        return result
    except Exception as e:
        logger.error("Error occurs when get_restaurant_name_dao(), error message: {}".format(e))
