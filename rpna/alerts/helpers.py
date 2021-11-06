import random
import string


def generate_code(user):
    code = "".join(random.choice(string.digits) for _ in range(6))
    user.set_password(code)
    user.save()
    return code


def send_alerts() -> int:
    return 0
