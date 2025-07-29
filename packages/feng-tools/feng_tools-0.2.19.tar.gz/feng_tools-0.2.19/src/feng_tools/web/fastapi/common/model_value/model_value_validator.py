from typing import Optional

from pydantic import BaseModel

from feng_tools.base.re import re_tools

class ValidateResult(BaseModel):
    is_passed:Optional[bool] = True
    error_msg:Optional[str] = None

class ModelValueValidator:
    """模型值校验器"""
    @staticmethod
    def is_email(value) -> ValidateResult:
        return ValidateResult(is_passed=True if re_tools.match_email(value) else False,
                              error_msg='邮箱格式不正确！')
    @staticmethod
    def is_phone(value) -> ValidateResult:
        return ValidateResult(is_passed=True if re_tools.match_phone(value) else False,
                              error_msg='手机号格式不正确！')
    @staticmethod
    def is_ip(value) -> ValidateResult:
        return ValidateResult(is_passed=True if re_tools.match_ip(value) else False,
                              error_msg='IP格式不正确！')
