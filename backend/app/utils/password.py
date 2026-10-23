import bcrypt


# 对密码进行加密
def hash_password(password: str):
    return bcrypt.hashpw(
        # 读取方式
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


# 验证密码的有效性
def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )
