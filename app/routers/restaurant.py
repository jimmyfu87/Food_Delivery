from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from ..dao.food_dao import get_restaurant_food_dao
from ..dao.restaurant_dao import (get_all_restaurants_dao,
                                  get_restaurant_name_by_restaurant_id_dao)
from ..env.config import get_logger, root_url
from ..tool.authentication import verify_cookies

router = APIRouter()
templates = Jinja2Templates(directory="templates")
logger = get_logger('restaurant')


@router.get("/", response_class=HTMLResponse, tags=['restaurant'])
def get_all_restaurants_view(request: Request):
    logger.info('get_all_restaurants_view()')
    verify_response = verify_cookies(request)
    if verify_response['success']:
        member_id = verify_response['member_id']
        all_restaurants = get_all_restaurants_dao()
        restaurant_rows = []
        # Add hyperlink to restaurant menu
        for restaurant in all_restaurants:
            restaurant_row = dict(restaurant)
            restaurant_row['restaurant_url'] = root_url + 'restaurant/' + str(restaurant_row['restaurant_id'])
            restaurant_rows.append(restaurant_row)
        return templates.TemplateResponse("Restaurant.html", {"request": request, 
                                                             "restaurant_rows": restaurant_rows,
                                                             "member_id": member_id})
    else:
        logger.error('Error occurs when get_member_product_view(), '
                     'error message: {}'.format(verify_response['message']))
        return JSONResponse(content={'message':
                                     'Error occurs when get restaurants list view, '
                                     'please login again'})


@router.get("/{restaurant_id}", response_class=HTMLResponse, tags=['restaurant'])
def get_restaurant_menu_view(request: Request, restaurant_id: str):
    logger.info('get_restaurant_menu_view()')
    logger.info(f'restaurant_id: {restaurant_id}')
    verify_response = verify_cookies(request)
    if verify_response['success']:
        member_id = verify_response['member_id']
        food_rows = get_restaurant_food_dao(restaurant_id)
        restaurant_name = get_restaurant_name_by_restaurant_id_dao(restaurant_id)[0]['restaurant_name']
        return templates.TemplateResponse("Menu.html",{"request": request, 
                                                       "food_rows": food_rows, 
                                                       "restaurant_name": restaurant_name,
                                                       "member_id": member_id})
    else:
        logger.error('Error occurs when get_restaurant_menu_view(), '
                     'error message: {}'.format(verify_response['message']))
        return JSONResponse(content={'message':
                                     'Error occurs when get menu list view, '
                                     'please login again'})
