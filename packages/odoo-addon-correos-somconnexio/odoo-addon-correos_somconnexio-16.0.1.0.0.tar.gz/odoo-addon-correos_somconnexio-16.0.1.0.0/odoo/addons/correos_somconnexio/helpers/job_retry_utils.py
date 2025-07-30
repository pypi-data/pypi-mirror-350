import logging
import time
from functools import wraps

_logger = logging.getLogger(__name__)


def retry_on_error(retries, delay, errors):
    def decorator_retry(func):
        @wraps(func)
        def wrapper_retry(self, *args, **kwargs):
            last_error = None
            for attempt in range(retries + 1):
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    if type(e) not in errors:
                        raise e
                    else:
                        _logger.info(
                            f"Error: {e}. Retry {attempt} in {delay} seconds..."
                        )
                        last_error = e
                        time.sleep(delay)
            _logger.info(f"Max retries ({retries}) exceeded.")
            if last_error:
                raise last_error

        return wrapper_retry

    return decorator_retry
