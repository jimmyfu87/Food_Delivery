from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy.sql import text

from ..env.config import engine, get_logger

logger = get_logger('cart_item_dao')


class Cart_item (BaseModel):
    member_id: Optional[str]
    food_id: Optional[str]
    food_name: Optional[str]
    food_price: Optional[int]
    food_quantity: Optional[str]
    food_remark: Optional[str]
    cart_item_price: Optional[int]
    restaurant_name: Optional[str]


class Cart_items(BaseModel):
    cart_items: List[Cart_item]


def add_food_tocart_dao(cart_items: Cart_items):
    logger.info('add_food_tocart_dao()')
    logger.info(f'cart_items:{cart_items}')
    data_to_insert = [
        {"member_id": cart_item.member_id, "food_id": cart_item.food_id, "food_name": cart_item.food_name,
         "food_price": cart_item.food_price,"food_quantity": cart_item.food_quantity,  "food_remark": cart_item.food_remark, 
         "cart_item_price": cart_item.cart_item_price, "restaurant_name": cart_item.restaurant_name}
        for cart_item in cart_items if int(cart_item.food_quantity) > 0]
    if len(data_to_insert) > 0:
        query = "INSERT INTO Cart_item (member_id, food_id, food_name, food_price, food_quantity, \
                food_remark, cart_item_price, restaurant_name) \
                VALUES (:member_id, :food_id, :food_name, :food_price, :food_quantity, :food_remark,  :cart_item_price, :restaurant_name)"
        try:
            result = engine.execute(text(query), data_to_insert)
            if result.rowcount > 0:
                return {"success": True}
            else:
                logger.info("Doesn't add any food!")
                return {"success": False}
        except Exception as e:
            logger.error(f"Error occurs when add_food_tocart_dao(), error message: {e}")
            return {"success": False}
    else:
        logger.info(f"No food to add")
        return {"success": False}


def get_cart_total_price(member_id: str):
    logger.info('get_cart_total_price()')
    logger.info(f'member_id:{member_id}')
    query = "SELECT SUM(cart_item_price) as cart_total_price FROM Cart_item WHERE member_id=:member_id GROUP BY member_id"
    try:
        result = engine.execute(text(query), {"member_id": member_id}).mappings().all()
        return result
    except Exception as e:
        logger.error("Error occurs when get_cart_total_price(), error message: {}".format(e))


def get_cart_item_dao(member_id: str):
    logger.info('get_cart_item_dao()')
    logger.info(f'member_id:{member_id}')
    query = "SELECT * FROM Cart_item WHERE member_id=:member_id"
    try:
        result = engine.execute(text(query), {"member_id": member_id}).mappings().all()
        return result
    except Exception as e:
        logger.error("Error occurs when get_cart_item_dao(), error message: {}".format(e))


def delete_all_cart_items_dao(member_id: str):
    logger.info('delete_all_cart_items_dao()')
    logger.info(f'member_id:{member_id}')
    query = "DELETE FROM Cart_item WHERE member_id=:member_id"
    try:
        result = engine.execute(text(query), {"member_id":member_id})
        if result.rowcount >= 1:
            return {"success": True, "message": "Delete Successfully!"} 
        else:
            return {"success": False, "message": "Nothing in cart!"} 
    except Exception as e:
        logger.error(f"Error occurs when delete_all_cart_items_dao(), error message: {e}")
        return {"success": False, "message": e} 
