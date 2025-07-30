"""
pip install passlib
"""
from passlib.hash import pbkdf2_sha256

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pbkdf2_sha256.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pbkdf2_sha256.hash(password)

def encrypt_password(password: str) -> str:
    """加密密码"""
    return get_password_hash(password)


if __name__ == '__main__':
    pwd_hash = get_password_hash('123456')
    print(verify_password('123456', pwd_hash))