def str_to_bool(value):
    if value is None:
        return False

    if isinstance(value, bool):
        return value

    value = str(value).strip()
    if not value:
        return False

    ret = bool(value)
    if not ret:
        return False

    value = str(value).lower()
    ret = True if value in ["true", "1", "on", "yes"] else False

    return ret
