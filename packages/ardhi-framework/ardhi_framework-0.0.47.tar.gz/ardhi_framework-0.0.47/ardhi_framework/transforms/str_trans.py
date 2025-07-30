import uuid


def _r(s: str):
    """
    takes a string, and returns a human-readable version of the passed string
    Args:
        s:
    Returns:
        readable string: str
    """
    return s.replace('_', ' ').replace('-', ' ').strip().capitalize()

def is_uuid(val: str or uuid.UUID):
    """
    checks if value is uuid format or can be cast to uuid
    Returns uuid string or false if not possible
    """
    try:
        return uuid.UUID(val)
    except (ValueError, TypeError):
        return None

def to_str(val):
    """
    Accepts any format, casts to string format; even dict or lists
    """
    if isinstance(val, (str, int)):
        return _r(str(val))
    if isinstance(val, list):
        return ', '.join([to_str(inst for inst in val)])
    if isinstance(val, dict):
        # eg {key: val}
        return to_str([to_str(b_key) + ':' + to_str(b_val) for b_key, b_val in val.items()])
    try:
        return _r(str(val))
    except TypeError:
        pass

    return val

