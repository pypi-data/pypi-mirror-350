from profiplots import settings


def validate_active_style():
    """
    Checks that the active style is set.
    """
    if settings.active_theme is None:
        raise ValueError("Active style is set to None. Did you forget to call `set_theme`?")
