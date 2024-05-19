import phonenumbers


def validate_mobile(v):
    """валидация телефоного номера полизователя"""

    try:
        mobile = phonenumbers.parse(v, None)
        if not phonenumbers.is_valid_number(mobile):
            raise ValueError('неверный формат телефона')
        return v
    except Exception as e:
        raise ValueError('неверный формат телефона')