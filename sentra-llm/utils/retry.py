import time
from functools import wraps
from typing import Callable, Type, Tuple

def retry(
        exceptions: Tuple[Type[BaseException], ...],
        max_retries: int = 3,
        backoff_factor: float = 2.0,
        initial_delay: float = 2.0,
):
    """
    Декоратор для автоматического повтора функции при указанных ошибках.

    Args:
        exceptions: Кортеж исключений, при которых нужно повторить попытку.
        max_retries: Максимальное количество попыток.
        backoff_factor: Множитель увеличения задержки после каждой ошибки.
        initial_delay: Начальная задержка перед первой попыткой.

    Returns:
        Результат работы функции или выбрасывает исключение после max_retries.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"⚠️ Error on attempt {attempt}: {e}")
                    if attempt == max_retries:
                        print("❌ Max retries exceeded. Raising exception.")
                        raise
                    print(f"🔄 Retrying in {delay:.1f} seconds...")
                    time.sleep(delay)
                    delay *= backoff_factor
        return wrapper
    return decorator
