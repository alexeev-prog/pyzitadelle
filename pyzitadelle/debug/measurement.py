from functools import wraps
from time import time
from typing import Callable

from rich import print


def async_debug_measurement(label: str = "measurement") -> Callable:
	def decorator(func):
		@wraps(func)
		async def wrapper(*args, **kwargs):
			start = time()
			result = await func(*args, **kwargs)
			end = time()

			total = round(end - start, 9)

			print(
				"[bold dim]{}[/bold dim] : {}".format(
					f"{func.__name__} | {label}".ljust(len(label) * 2), total
				)
			)

			return result


def debug_measurement(label: str = "measurement"):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			start = time()
			result = func(*args, **kwargs)
			end = time()

			total = round(end - start, 9)

			print(
				"[bold dim]{}[/bold dim] : {}".format(
					f"{func.__name__} | {label}".ljust(len(label) * 2), total
				)
			)

			return result

		return wrapper

	return decorator
