from pydantic import BaseModel
from sqlalchemy.sql import text

from ..env.config import engine, get_logger

logger = get_logger('order_dao')


class Order (BaseModel):
    payment_name: str
    total_price: int


def create_order_dao(member_id: str, total_price: int, payment_name: str):
    logger.info('create_order_dao()')
    logger.info(f'member_id: {member_id}')
    logger.info(f'total_price: {total_price}')
    logger.info(f'payment_name: {payment_name}')
    query = """INSERT INTO `Order` (member_id, total_price, payment_name, order_status, book_time)
            VALUES
                (:member_id, :total_price, :payment_name, "submit", CONVERT_TZ(NOW(), 'UTC', 'Asia/Taipei'))
            """
    try:
        result = engine.execute(text(query), {"member_id": member_id,
                                              "total_price": total_price,
                                              "payment_name": payment_name})
        # Get auto increment id
        order_id = result.lastrowid
        if order_id:
            return {"success": True,
                    "message": "Add cart to order successfully!", "order_id": order_id}
        else:
            return {"success": False,
                    "message": "Add cart to order unsuccessfully!"}
    except Exception as e:
        logger.error(f"Error occurs when create_order_dao(), error message: {e}")
        return {"success": False, "message": str(e)}


def get_submit_order_dao(member_id: str):
    logger.info('get_order_dao()')
    logger.info(f'member_id: {member_id}')
    query = "SELECT * FROM `Order` WHERE member_id=:member_id AND order_status='submit'"
    try:
        result = engine.execute(text(query), {"member_id": member_id}).mappings().all()
        return result
    except Exception as e:
        logger.error(f"Error occurs when get_order_dao(), error message: {e}")


def cancel_order_dao(order_id: int):
    logger.info('cancel_order_dao()')
    logger.info(f'order_id: {order_id}')
    query = "UPDATE `Order` SET order_status = 'cancelled' WHERE order_id = :order_id"
    try:
        result = engine.execute(text(query), {"order_id": order_id})
        if result.rowcount >= 1:
            return {"success": True, "message": "Cancel Order Successfully"} 
        else:
            return {"success": False, "message": "No Order to cancel"} 
    except Exception as e:
        logger.error(f"Error occurs when cancel_order_dao(), error message: {e}")
        return {"success": False, "message": e} 
