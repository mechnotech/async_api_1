import logging
import time
from functools import wraps


def backoff(
        start_sleep_time=0.05,
        factor=1.5,
        border_sleep_time=5,
        logy=logging
):
    """
        Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
         Использует наивный экспоненциальный рост времени повтора (factor)
            до граничного времени ожидания (border_sleep_time)

        Формула:
            t = start_sleep_time * 2^(n) if t < border_sleep_time
            t = border_sleep_time if t >= border_sleep_time
        :param logy: Экзепляр логгера
        :param start_sleep_time: начальное время повтора
        :param factor: во сколько раз нужно увеличить время ожидания
        :param border_sleep_time: граничное время ожидания
        :return: результат выполнения функции
    """

    def my_decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):
            t = start_sleep_time
            counter = 1
            while True:
                try:
                    time.sleep(t)
                    result = f(*args, **kwargs)
                    break

                except Exception:
                    logy.warning(f'Connection failed, reconnection attempt #{counter}, wait time - {t} sec')
                    if t < border_sleep_time:
                        t = t * 2 ** factor
                    if t >= border_sleep_time:
                        t = border_sleep_time
                    counter += 1

            return result

        return wrapper

    return my_decorator


if __name__ == '__main__':
    pass
