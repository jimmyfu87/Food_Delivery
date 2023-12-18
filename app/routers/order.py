from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from ..dao.cart_item_dao import delete_all_cart_items_dao
from ..dao.order_dao import (Order, cancel_order_dao, create_order_dao,
                             get_submit_order_dao)
from ..dao.order_item_dao import (add_cart_to_order_item_dao,
                                  get_order_item_dao, get_order_total_price)
from ..env.config import get_logger, root_url
from ..tool.authentication import verify_cookies

router = APIRouter()
templates = Jinja2Templates(directory="templates")
logger = get_logger('order')


@router.get("/", response_class=HTMLResponse, tags=['order'])
def get_order_view(request: Request):
    logger.info('get_order_view()')
    verify_response = verify_cookies(request)
    if verify_response['success']:
        member_id = verify_response['member_id']
        submit_order_rows = get_submit_order_dao(member_id)
        all_orders = []
        for data in submit_order_rows:
            arr_dict = dict(data)
            arr_dict['order_url'] = root_url + \
                                    'order/' + str(arr_dict['order_id'])
            all_orders.append(arr_dict)
        return templates.TemplateResponse("Order.html",
                                          {"request": request,
                                           "submit_order_rows": all_orders,
                                           "member_id": member_id})
    else:
        logger.error('Error occurs when get_order_view(), error message: {}'
                     .format(verify_response['message']))
        return JSONResponse(content={'message': 'Error occurs when get order list view, '
                                                'please login again'})


@router.get("/{order_id}", response_class=HTMLResponse, tags=['order'])
def get_order_item_view(request: Request, order_id: int):
    logger.info('get_order_item_view()')
    logger.info(f'order_id: {order_id}')
    verify_response = verify_cookies(request)
    if verify_response['success']:
        member_id = verify_response['member_id']
        order_item_rows = get_order_item_dao(order_id)
        order_total_price = get_order_total_price(order_id)[0]['order_total_price']
        return templates.TemplateResponse("Order_item.html", {"request": request,
                                                            "order_item_rows": order_item_rows,
                                                            'order_total_price': order_total_price, 
                                                            'order_id': order_id,
                                                            "member_id": member_id})
    else:
        logger.error('Error occurs when get_order_item_view(), '
                     'error message: {}'.format(verify_response['message']))
        return JSONResponse(content={'message':
                                     'Error occurs when get order item view, please login again'})


@router.post("/submit_order", tags=["order"])
def submit_order(request: Request, order: Order):
    logger.info('add_food_tocart()')
    logger.info(f'order: {order}')
    verify_response = verify_cookies(request)
    if verify_response['success']:
        member_id = verify_response['member_id']
        payment_name = order.payment_name
        total_price = int(order.total_price)
        response = create_order_dao(member_id, total_price, payment_name)
        if response["success"]:
            order_id = response["order_id"]
            response = add_cart_to_order_item_dao(order_id, member_id)
            if response["success"]:
                response = delete_all_cart_items_dao(member_id)
                if response["success"]:
                    return JSONResponse(content={"success": True})
                else:
                    logger.error('Error occurs when delete_all_cart_items_dao(), '
                                 'error message: {}'.format(response['message']))
                    return JSONResponse(content={"success": False})
            else:
                 logger.error('Error occurs when add_cart_to_order_item_dao(), '
                              'error message: {}'.format(response['message']))
                 return JSONResponse(content={"success": False})
        else:
            logger.error('Error occurs when create_order_dao(), '
                         'error message: {}'.format(response['message']))
            return JSONResponse(content={"success": False})
    else:
        logger.error('Error occurs when submit_order(), '
                     'error message: {}'.format(verify_response['message']))
        return JSONResponse(content={'message':
                                     'Error occurs when submit order, please login again'})


@router.patch("/cancel_order", tags=['order'])
def cancel_order(request: Request, order_id: str):
    logger.info('cancel_order()')
    logger.info(f'order_id: {order_id}')
    verify_response = verify_cookies(request)
    if verify_response['success']:
        response = cancel_order_dao(order_id)
        if response["success"]:
            return JSONResponse(content=response)
        else:
            logger.error('Error occurs when cancel_order_dao(), '
                         'error message: {}'.format(response['message']))
            return JSONResponse(content={"success": False})
    else:
        logger.error('Error occurs when cancel_order(), '
                     'error message: {}'.format(verify_response['message']))
        return JSONResponse(content={'message':
                                     'Error occurs when cancel order, please login again'})
