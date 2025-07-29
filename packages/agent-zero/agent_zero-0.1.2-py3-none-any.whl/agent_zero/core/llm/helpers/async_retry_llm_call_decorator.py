import asyncio
import openai
import groq


def async_retry_with_pause(
    func,
    max_retries: int = 3,
    errors: tuple = (openai.RateLimitError, groq.RateLimitError),
):
    async def wrapper(*args, **kwargs):
        num_retries = 0
        rate_limit_delay = 30

        while True:
            try:
                return await func(*args, **kwargs)
            except groq.BadRequestError as e:
                num_retries += 1
                print(f"Retrying {num_retries}..... {e}")
                await asyncio.sleep(1)
            except errors as e:
                num_retries += 1
                print(f"Retrying {num_retries}..... {e}")
                await asyncio.sleep(rate_limit_delay)
            finally:
                if num_retries > max_retries:
                    raise Exception(f"Maximum number of retries ({max_retries}) exceeded.")

    return wrapper
