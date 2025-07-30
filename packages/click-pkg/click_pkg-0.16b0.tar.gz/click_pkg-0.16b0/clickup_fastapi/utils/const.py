

class Action:
    """
    CLICK API uchun harakat (action) konstantalari.
    """
    PREPARE = '0'
    COMPLETE = '1'

    ALLOWED_ACTIONS = [
        PREPARE,
        COMPLETE,
    ]
