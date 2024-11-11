from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import re

MINIMUM_PASSWORD_LENGTH = 8
MINIMUM_USER_ID_LENGTH = 8
class CustomPasswordValidator:
    def __call__(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise ValidationError(str(e))

    def validate(self, password, user=None):
        if len(password) <8:
            raise ValidationError("비밀번호는 8자리 이상이어야 합니다.")
        if not re.search(r"[a-zA-Z]", password):
            raise ValidationError("비밀번호는 하나 이상의 영문이 포함되어야 합니다.")
        if not re.search(r"\d",password):
            raise ValidationError("비밀번호는 하나 이상의 숫자가 포함되어야 합니다.")

        if not re.search(r"[!@#$%^&*()]", password):
            raise ValidationError(
                "비밀번호는 적어도 하나 이상의 특수 문자(!@#$%^&*())가 포함되어야 합니다."
            )

    def get_help_text(self):
        return "비밀번호는 8자리 이상이며 영문, 숫자, 특수문자((!@#$%^&*()))를 포함해야 합니다."


def validate_id(user_id):
    if len(user_id) < MINIMUM_USER_ID_LENGTH:
        raise ValidationError('아이디는 8자 이상 이어야 합니다.')
    if not re.search(r"[a-zA-Z]", user_id):
        raise ValidationError("아이디는 하나 이상의 영문이 포함되어야 합니다.")
    if not re.search(r"\d", user_id):
        raise ValidationError("아이디는 하나 이상의 숫자가 포함되어야 합니다.")

def validate_email(email):
    a = re.compile('^[a-zA-Z0-9-_.]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$')
    b = a.match(email)
    if b is None:
        raise ValidationError("이메일을 다시 입력해주세요!")

def validate_phone(phone):
    pattern = re.compile('^[0]\d{2}\d{3,4}\d{4}$')
    if not pattern.match(phone):
        raise ValidationError("전화번호를 다시 입력해주세요!")
