from feng_tools.base.encrypt import password_tools


class ModelValueTransformer:
    @staticmethod
    def lower_case(value):
        """转换为小写"""
        if value and isinstance(value, str):
            return value.lower()
        return value

    @staticmethod
    def password(value):
        """密码转换加密"""
        return password_tools.encrypt_password(value)
