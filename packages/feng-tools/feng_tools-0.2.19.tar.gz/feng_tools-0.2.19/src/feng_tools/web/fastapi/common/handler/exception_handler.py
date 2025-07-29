import json
import logging
import traceback

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

from feng_tools.web.fastapi.common.schema.api_response import ApiResponse


async def value_exception_handle(request: Request, exc: ValueError):
    """
    全局所有异常
    :param request:
    :param exc:
    :return:
    """
    logging.warning(f'[{request.method}] {request.url} 错误提示：{json.dumps(exc.args)}')
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(ApiResponse(success=False, message=exc.args[0]))
    )
async def validation_exception_handle(request: Request, exc: RequestValidationError):
    """
    请求参数验证异常
    :param request: 请求信息
    :param exc: 异常对象
    :return:
    """
    logging.warning(f'[{request.method}] {request.url} 参数校验失败！失败信息：{json.dumps(exc.errors())}')
    required_fields = []
    error_msg = []
    for error_item in exc.errors():
        field_name = error_item.get('loc')[1]
        if error_item.get('msg') == 'Field required':
            required_fields.append(field_name)
        else:
            error_msg.append(error_item.get('msg'))
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(ApiResponse(success=False, message="参数校验失败!", data={
            'required': required_fields,
            'msg': '<br>'.join(error_msg)
        }))
    )

async def starlette_http_exception_handle(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_307_TEMPORARY_REDIRECT:
        return RedirectResponse(url=exc.headers.get("location"))
    if exc.status_code == 404:
        if request.url.path.startswith('/api/v1'):
            return JSONResponse(status_code=200, content=[])
        return JSONResponse(
            status_code=404,
            content={"success": False, "error": "资源未找到，请检查请求路径是否正确。"}
        )
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(ApiResponse(success=False, message="服务出现异常，请联系管理员!"))
    )

async def exception_handle(request: Request, exc: Exception):
    """
    全局异常
    :param request:
    :param exc:
    :return:
    """
    traceback_msg = traceback.format_exc()
    logging.error(f'[{request.method}] {request.url} 服务出现异常：{traceback_msg}')
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(ApiResponse(success=False, message="服务出现异常，请联系管理员!"))
    )

