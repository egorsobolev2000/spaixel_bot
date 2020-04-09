from colors import ColorsPrint


def log_error(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(ColorsPrint('Возникла ошибка', 'err').do_colored(), e)
            raise e

    return inner
