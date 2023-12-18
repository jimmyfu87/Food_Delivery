
from sqlalchemy.sql import text

from ..env.config import engine, get_logger

logger = get_logger('order_item_dao')


def add_cart_to_order_item_dao(order_id: str, member_id: str):
    logger.info('add_food_tocart_dao()')
    logger.info(f'order_id: {order_id}')
    logger.info(f'member_id: {member_id}')
    query = """INSERT INTO Order_item (order_id, food_id, food_name, food_price, food_quantity, food_remark, restaurant_name, order_item_price)
            SELECT
                :order_id AS order_id,
                cart_item.food_id,
                cart_item.food_name,
                cart_item.food_price,
                cart_item.food_quantity,
                cart_item.food_remark,
                cart_item.restaurant_name,
                cart_item.cart_item_price AS order_item_price
            FROM
                Cart_item cart_item
            WHERE member_id =:member_id"""
    try:
        result = engine.execute(text(query),  {"member_id": member_id, "order_id": order_id})
        if result.rowcount > 0:
            return {"success": True, "message": "Add cart to order successfully!"}
        else:
            return {"success": False, "message": "Add cart to order unsuccessfully!"}
    except Exception as e:
        logger.error(f"Error occurs when add_food_tocart_dao(), error message: {e}")
        return {"success": False, "message": str(e)}


def get_order_item_dao(order_id: str):
    logger.info('get_order_item_dao()')
    logger.info(f'order_id: {order_id}')
    query = "SELECT * FROM Order_item WHERE order_id=:order_id"
    try:
        result = engine.execute(text(query), {"order_id": order_id}).mappings().all()
        return result
    except Exception as e:
        logger.error(f"Error occurs when get_order_item_dao(), error message: {e}")


def get_order_total_price(order_id: str):
    logger.info('get_order_total_price()')
    query = "SELECT SUM(order_item_price) as order_total_price FROM Order_item WHERE order_id=:order_id GROUP BY order_id"
    try:
        result = engine.execute(text(query), {"order_id": order_id}).mappings().all()
        return result
    except Exception as e:
        logger.error(f"Error occurs when get_cart_total_price(), error message: {e}")
