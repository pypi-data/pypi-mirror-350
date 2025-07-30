"""
AES加密工具
相关知识:
- 关键词：
    - 密钥（Key）：AES加密和解密使用相同的密钥。
    - 初始化向量（IV）：AES在CBC模式下使用相同的IV进行加密和解密。
- AES加密分类：
    - AES-128需要16字节的密钥和IV。
    - AES-192需要24字节的密钥和IV。
    - AES-256需要32字节的密钥和IV。
- 加密模式
    - ECB（Electronic Codebook）模式
        特点：每个块独立加密，相同的明文块会生成相同的密文块。
        优点：简单，易于实现。
        缺点：不安全，容易受到模式攻击，不适合加密大量数据。
        适用场景：不推荐用于加密大量数据，仅适用于小块数据或需要快速加密的场景。
    - CBC（Cipher Block Chaining）模式
        特点：每个明文块与前一个密文块进行异或操作后再加密。
        优点：安全性高，每个密文块依赖于前一个密文块，相同的明文块也会生成不同的密文块。
        缺点：需要初始化向量（IV），且IV必须保密且随机。
        适用场景：广泛应用于需要高安全性的加密场景。
    - CFB（Cipher Feedback）模式
        特点：前一个密文块用于生成密钥流，密钥流与明文块进行异或操作。
        优点：可以处理任意长度的数据，适合流加密。
        缺点：实现相对复杂。
        适用场景：适用于需要流加密的场景，如实时通信。
    - OFB（Output Feedback）模式
        特点：前一个密文块用于生成密钥流，密钥流与明文块进行异或操作。
        优点：可以处理任意长度的数据，适合流加密。
        缺点：实现相对复杂。
        适用场景：适用于需要流加密的场景，如实时通信。
    - CTR（Counter）模式
        特点：使用计数器生成密钥流，密钥流与明文块进行异或操作。
        优点：可以并行化处理，适合高性能需求。
        缺点：需要唯一的计数器值。
        适用场景：适用于需要高性能和并行化的加密场景。
    - GCM（Galois/Counter Mode）模式
        特点：结合了CTR模式和Galois域乘法，提供认证加密。
        优点：提供数据完整性检查，适合需要认证的场景。
        缺点：实现相对复杂。
        适用场景：适用于需要认证加密的场景，如网络通信。
        相关概念：
            - tag: 在 GCM 模式下，tag 是一种用于验证数据完整性和真实性的认证标签（Authentication Tag）
                - 它是由加密算法生成的一个固定长度的值（通常为 128 位，即 16 字节），附带在密文之后。
                - 它是由加密算法生成的一个固定长度的值（通常为 128 位，即 16 字节），附带在密文之后。
                - 原理：
                    - 加密时：GCM 模式会在加密过程中生成一个 tag，并将其附加到密文上。
                    -解密时：GCM 模式会重新计算 tag，并与接收到的 tag 进行比较。如果两者匹配，则说明密文未被篡改；否则，解密将失败。
            - nonce: 在 GCM 模式下，nonce 是一种用于生成密钥流的随机数（Nonce）。
- 填充方式
    - PKCS7
- 编码方式
    - Base64 URL安全编码
如果要解密其他人使用AES算法加密的内容，前提是：
- 使用相同的密钥和IV。
- 使用相同的加密模式（CBC）。
- 使用相同的填充方式（PKCS7）。
- 使用相同的编码方式（Base64 URL安全编码）。
"""
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Util import Counter
import base64

def get_key(length: int = 16) -> bytes:
    """
    生成密钥
        - AES-128需要16字节的密钥和IV。
        - AES-192需要24字节的密钥和IV。
        - AES-256需要32字节的密钥和IV。
    :return: 密钥 """
    return get_random_bytes(length)

def get_iv(length: int = 16) -> bytes:
    """
    生成初始化向量
        - AES-128需要16字节的密钥和IV。
        - AES-192需要24字节的密钥和IV。
        - AES-256需要32字节的密钥和IV。
    :return: 初始化向量 """
    return get_random_bytes(length)

def get_nonce(length: int = 12) -> bytes:
    """
    生成随机的nonce（用于GCM模式）
    :param length: nonce的长度，默认为12字节
    :return: nonce """
    return get_random_bytes(length)

def get_counter(nonce: bytes, initial_value: int = 0) -> Counter:
    """
    生成计数器（用于CTR模式）
    :param nonce: 计数器的前8字节
    :param initial_value: 计数器的初始值
    :return: 计数器对象 """
    if len(nonce) != 8:
        raise ValueError("nonce长度必须为8字节")
    return Counter.new(64, prefix=nonce, initial_value=initial_value)

def _encode_base64(data: bytes) -> str:
    """
    将字节数据编码为URL安全的Base64字符串
    :param data: 字节数据
    :return: URL安全的Base64字符串 """
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def _decode_base64(data: str) -> bytes:
    """
    将URL安全的Base64字符串解码为字节数据
    :param data: URL安全的Base64字符串
    :return: 字节数据 """
    return base64.urlsafe_b64decode(data)

def _validate_key(key: bytes):
    """验证密钥长度是否合法"""
    if not isinstance(key, bytes) or len(key) not in [16, 24, 32]:
        raise ValueError("密钥必须是16、24或32字节的字节类型")

def _validate_iv(iv: bytes):
    """验证初始化向量长度是否合法"""
    if not isinstance(iv, bytes) or len(iv) != AES.block_size:
        raise ValueError(f"初始化向量长度必须为 {AES.block_size} 字节")

def encrypt(key: bytes, iv: bytes, text: str, mode: int = AES.MODE_CBC) -> str:
    """
    AES加密（支持多种模式）
    :param key: 密钥
    :param iv: 初始化向量（仅适用于CBC、CFB等模式）
    :param text: 明文
    :param mode: 加密模式（默认为CBC）, 分为：AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB
    :return: 密文
    """
    try:
        _validate_key(key)
        if mode in [AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB]:
            _validate_iv(iv)
        if not isinstance(text, str):
            raise ValueError("明文必须是字符串类型")

        text_bytes = pad(text.encode('utf-8'), AES.block_size)
        cipher = AES.new(key, mode, iv) if mode in [AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB] else AES.new(key, mode)
        encrypted_bytes = cipher.encrypt(text_bytes)
        return _encode_base64(encrypted_bytes)

    except Exception as e:
        raise RuntimeError(f"加密过程中发生错误: {e}")

def decrypt(key: bytes, iv: bytes, text: str, mode: int = AES.MODE_CBC) -> str:
    """
    AES解密（支持多种模式）
    :param key: 密钥
    :param iv: 初始化向量（仅适用于CBC、CFB等模式）
    :param text: 密文
    :param mode: 解密模式（默认为CBC） ，分为：AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB
    :return: 明文
    """
    try:
        _validate_key(key)
        if mode in [AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB]:
            _validate_iv(iv)
        if not isinstance(text, str):
            raise ValueError("密文必须是字符串类型")

        encrypted_bytes = _decode_base64(text)
        cipher = AES.new(key, mode, iv) if mode in [AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB] else AES.new(key, mode)
        decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        return decrypted_bytes.decode('utf-8')

    except Exception as e:
        raise RuntimeError(f"解密过程中发生错误: {e}")

def encrypt_ecb(key: bytes, text: str) -> str:
    """
    AES加密（ECB模式）
    :param key: 密钥
    :param text: 明文
    :return: 密文 """
    try:
        _validate_key(key)
        if not isinstance(text, str):
            raise ValueError("明文必须是字符串类型")

        text_bytes = pad(text.encode('utf-8'), AES.block_size)
        cipher = AES.new(key, AES.MODE_ECB)
        encrypted_bytes = cipher.encrypt(text_bytes)
        return _encode_base64(encrypted_bytes)

    except Exception as e:
        raise RuntimeError(f"ECB加密过程中发生错误: {e}")

def decrypt_ecb(key: bytes, text: str) -> str:
    """
    AES解密（ECB模式）
    :param key: 密钥
    :param text: 密文
    :return: 明文 """
    try:
        if not isinstance(key, bytes) or len(key) not in [16, 24, 32]:
            raise ValueError("密钥必须是16、24或32字节的字节类型")
        if not isinstance(text, str):
            raise ValueError("密文必须是字符串类型")

        encrypted_bytes = _decode_base64(text)
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        return decrypted_bytes.decode('utf-8')

    except Exception as e:
        raise RuntimeError(f"ECB解密过程中发生错误: {e}")

def encrypt_ctr(key: bytes, nonce: bytes, counter: Counter, text: str) -> str:
    """
    AES加密（CTR模式）
    :param key: 密钥
    :param nonce: 计数器的前8字节
    :param counter: 计数器对象
    :param text: 明文
    :return: 密文 """
    try:
        _validate_key(key)
        if not isinstance(nonce, bytes) or len(nonce) != 8:
            raise ValueError("nonce长度必须为8字节")
        if not isinstance(counter, Counter):
            raise ValueError("counter必须是Crypto.Util.Counter对象")
        if not isinstance(text, str):
            raise ValueError("明文必须是字符串类型")

        text_bytes = pad(text.encode('utf-8'), AES.block_size)
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce, counter=counter)
        encrypted_bytes = cipher.encrypt(text_bytes)
        return _encode_base64(encrypted_bytes)

    except Exception as e:
        raise RuntimeError(f"CTR加密过程中发生错误: {e}")

def decrypt_ctr(key: bytes, nonce: bytes, counter: Counter, text: str) -> str:
    """
    AES解密（CTR模式）
    :param key: 密钥
    :param nonce: 计数器的前8字节
    :param counter: 计数器对象
    :param text: 密文
    :return: 明文 """
    try:
        _validate_key(key)
        if not isinstance(nonce, bytes) or len(nonce) != 8:
            raise ValueError("nonce长度必须为8字节")
        if not isinstance(counter, Counter):
            raise ValueError("counter必须是Crypto.Util.Counter对象")
        if not isinstance(text, str):
            raise ValueError("密文必须是字符串类型")

        encrypted_bytes = _decode_base64(text)
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce, counter=counter)
        decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        return decrypted_bytes.decode('utf-8')

    except Exception as e:
        raise RuntimeError(f"CTR解密过程中发生错误: {e}")

def encrypt_gcm(key: bytes, iv: bytes, text: str) -> (bytes, bytes):
    """
    AES加密（GCM模式）
    :param key: 密钥
    :param iv: 初始化向量（GCM模式通常使用12字节的IV）
    :param text: 明文
    :return: 密文, 校验和 """
    try:
        _validate_key(key)
        if not isinstance(iv, bytes) or len(iv) != 12:
            raise ValueError("GCM模式的初始化向量长度必须为12字节")
        if not isinstance(text, str):
            raise ValueError("明文必须是字符串类型")

        text_bytes = text.encode('utf-8')
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        encrypted_bytes, tag = cipher.encrypt_and_digest(text_bytes)
        return encrypted_bytes, tag

    except Exception as e:
        raise RuntimeError(f"GCM加密过程中发生错误: {e}")

def decrypt_gcm(key: bytes, iv: bytes, encrypted_bytes: bytes, tag: bytes, aad: bytes = None) -> str:
    """
    AES解密（GCM模式）
    :param key: 密钥
    :param iv: 初始化向量（GCM模式通常使用12字节的IV）
    :param encrypted_bytes: 密文
    :param tag: 校验和
    :param aad: 附加数据（可选）
    :return: 明文 """
    try:
        _validate_key(key)
        if not isinstance(iv, bytes) or len(iv) != 12:
            raise ValueError("GCM模式的初始化向量长度必须为12字节")
        if not isinstance(encrypted_bytes, bytes):
            raise ValueError("密文必须是字节类型")
        if not isinstance(tag, bytes):
            raise ValueError("tag必须是字节类型")
        if aad is not None and not isinstance(aad, bytes):
            raise ValueError("附加数据必须是字节类型或None")

        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        if aad:
            cipher.update(aad)
        plaintext = cipher.decrypt_and_verify(encrypted_bytes, tag)
        return plaintext.decode('utf-8')

    except ValueError:
        raise ValueError("解密失败：密文可能已被篡改或 tag 不匹配")
    except Exception as e:
        raise RuntimeError(f"GCM解密过程中发生错误: {e}")








