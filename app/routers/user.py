from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from ..dao.user_dao import (User, check_member_id_email_exist_dao,
                            check_member_id_exist_dao, create_user_dao,
                            login_dao)
from ..env.config import get_logger, login_time_sec, redis
from ..tool.authentication import get_hash_password

router = APIRouter()
templates = Jinja2Templates(directory="templates")
logger = get_logger('user')


@router.post("/register", tags=["user"])
def register(user: User):
    logger.info('register()')
    logger.info(f'user: {user}')
    if user.member_id == "" \
       or user.member_password == "" \
       or user.member_email == "":
        return JSONResponse(content={"success": False,
                                     'message': "Value cannot be blank, "
                                                "please fill in!!"})
    if " " in user.member_id \
       or " " in user.member_password \
       or " " in user.member_email:
        return JSONResponse(content={"success": False,
                                     'message': "Value cannot contains blank, "
                                                 "please fill in!!"})
    check_member_id_email_exist_response = check_member_id_email_exist_dao(
                                            user.member_id, user.member_email)
    if len(check_member_id_email_exist_response) == 0:
        hash_password = get_hash_password(user.member_password)
        response = create_user_dao(user.member_id,
                                   hash_password, user.member_email)
        return JSONResponse(content=response)
    else:
        return JSONResponse(content={"success": False,
                                     'message': "This member id or email "
                                                 "has already been used "
                                                 ", please change it!!"})


@router.post("/login", tags=["user"])
def login(user: User):
    logger.info('login()')
    logger.info(f'user: {user}')
    check_member_id_exist_response = check_member_id_exist_dao(user.member_id)
    if len(check_member_id_exist_response) == 1:
        hash_password = get_hash_password(user.member_password)
        login_response = login_dao(user.member_id, hash_password)
        if len(login_response) == 1:
            hash_key = get_hash_password(user.member_id +
                                         datetime.now().strftime('%Y-%m-%d'))
            redis.setex(hash_key, login_time_sec, user.member_id)
            response = JSONResponse(content={"success": True})
            response.set_cookie(key="sid", value=hash_key)
            return response
        else:
            return JSONResponse(content={"success": False,
                                         'message': "Incorrect member id "
                                                     "or member password!!"})

    elif len(check_member_id_exist_response) == 0:
        return JSONResponse(content={"success": False,
                                     'message': f"{user.member_id} is "
                                                "not a valid member id,"
                                                "please register it!!"})


@router.get("/logout", tags=['user'])
def logout(request: Request):
    logger.info('logout()')
    if redis.exists(request.cookies['sid']):
        redis.delete(request.cookies['sid'])
        return JSONResponse(content={"success": True,
                                     'message': "Logout Successfully"})
    else:
        return JSONResponse(content={"success": False,
                                     'message': "Already logout!!"})
