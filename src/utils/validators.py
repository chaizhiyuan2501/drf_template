import re


def is_invalid_email_format(email):
    """電子メールの形式が無効かどうかをチェックする"""
    return not re.match(
        r"^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$",
        email,
    )


def is_invalid_password_format(password):
    """パスワードの形式が無効かどうかをチェックする"""
    return not re.match(
        r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        password,
    )
