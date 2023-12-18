from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from ..dao.cart_item_dao import (Cart_items, add_food_tocart_dao,
                                 delete_all_cart_items_dao, get_cart_item_dao,
                                 get_cart_total_price)
from ..dao.food_dao import get_food_dao
from ..dao.payment_dao import get_all_payment_dao
from ..dao.restaurant_dao import get_restaurant_name_by_food_id_dao
from ..env.config import get_logger
from ..tool.authentication import verify_cookies

router = APIRouter()
templates = Jinja2Templates(directory="templates")
logger = get_logger('cart_item')


@router.get("/", response_class=HTMLResponse, tags=['cart_item'])
def get_cart_item_view(request: Request):
    logger.info('get_cart_item_view()')
    verify_response = verify_cookies(request)
    if verify_response['success']:
        member_id = verify_response['member_id']
        cart_item_rows = get_cart_item_dao(member_id)
        payment_rows = get_all_payment_dao()
        # If no food in cart, cart_total_price is 0
        if len(get_cart_total_price(member_id)) != 0:
            cart_total_price = get_cart_total_price(member_id)[0]['cart_total_price']
        else:
            cart_total_price = 0
        return templates.TemplateResponse("Cart_item.html", {"request": request, "cart_item_rows": cart_item_rows,
                                                             "payment_rows": payment_rows, "member_id": member_id, 
                                                             "cart_total_price": cart_total_price})
    else:
        logger.error('Error occurs when get_member_product_view(), error message: {}'.format(verify_response['message']))
        return JSONResponse(content={'message': 'Error occurs when get restaurants list view, please login again'})


@router.post("/add_food_tocart", tags=["cart_item"])
def add_food_tocart(request: Request, cart_items_model: Cart_items):  
    logger.info('add_food_tocart()')
    logger.info(f'cart_items_model: {cart_items_model}')
    verify_response = verify_cookies(request)
    if verify_response['success']:
        cart_items = cart_items_model.cart_items
        # Filter food with 0 quantity
        cart_items = [cart_item for cart_item in cart_items if int(cart_item.food_quantity) > 0]
        # Add restaurant_name, food_name, food_price, cart_item_price to list
        for cart_item in cart_items:
            restaurant_name = get_restaurant_name_by_food_id_dao(cart_item.food_id)
            cart_item.restaurant_name = restaurant_name[0]['restaurant_name']
            food_info = get_food_dao(cart_item.food_id)[0]
            food_name = food_info['food_name']
            food_price = food_info['food_price']
            cart_item_price = int(food_price) * int(cart_item.food_quantity)
            cart_item.food_price = food_price
            cart_item.cart_item_price = cart_item_price
            cart_item.food_name = food_name
        # Put food to cart
        response = add_food_tocart_dao(cart_items)
        if response["success"]:          
            logger.info(f"response: {response}")
            return JSONResponse(content={"success": True})
        else:
            logger.error(f"response: {response}")
            return JSONResponse(content={"success": False})
    else:
        logger.error('Error occurs when add_food_tocart(), error message: {}'.format(verify_response['message']))
        return JSONResponse(content={'message': 'Error occurs when add food to cart, please login again'})


@router.delete("/delete_all_cart_items", tags=['cart_item'])
def delete_all_cart_items(request: Request):
    logger.info('delete_all_cart_items()')
    verify_response = verify_cookies(request)
    if verify_response['success']:
        member_id = verify_response['member_id']
        response = delete_all_cart_items_dao(member_id)
        if response["success"]:          
            logger.info(f"response: {response}")
            return JSONResponse(content={"success": True})
        else:
            logger.error(f"response: {response}")
            return JSONResponse(content={"success": False})
    else:
        logger.error('Error occurs when delete_all_cart_items(), error message: {}'.format(verify_response['message']))
        return JSONResponse(content={'message': 'Error occurs when delete all cart items, please login again'})
